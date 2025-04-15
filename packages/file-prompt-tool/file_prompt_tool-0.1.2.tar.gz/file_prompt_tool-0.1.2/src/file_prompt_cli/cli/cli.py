import typer
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress
import glob
import os
import threading
from queue import Queue, Empty
import uuid
import time

from file_prompt_cli.gcp.gcs_uploader import GCSUploader
from file_prompt_cli.gcp.pubsub_client import PubSubClient
from file_prompt_cli.gcp.result_listener import ResultListener

# Initialize Typer app
app = typer.Typer(
    name="file-prompt",
    help="Dispatch files to GCP Pub/Sub and listen for results",
    add_completion=False
)

# Initialize console for rich output
console = Console()

def validate_file_paths(file_paths: List[str]) -> List[Path]:
    """Validate and convert file paths to Path objects."""
    valid_paths = []
    for path in file_paths:
        path_obj = Path(path)
        if not path_obj.exists():
            console.print(f"[red]Error: File not found: {path}[/red]")
            continue
        valid_paths.append(path_obj)
    return valid_paths

def dispatch_job_thread(
    files: List[Path],
    prompt: str,
    project_id: str,
    bucket_name: str,
    topic_name: str,
    progress_queue: Queue
):
    """Thread function for dispatching jobs."""
    try:
        start_time = time.time()
        console.print("[yellow]Initializing GCP clients...[/yellow]")
        
        # Initialize components
        uploader = GCSUploader(project_id, bucket_name)
        pubsub_client = PubSubClient(project_id, topic_name)
        
        init_time = time.time() - start_time
        console.print(f"[yellow]GCP clients initialized in {init_time:.2f} seconds[/yellow]")
        
        # Process files
        for file_path in files:
            try:
                file_start = time.time()
                console.print(f"[yellow]Processing {file_path.name}...[/yellow]")
                
                # Upload file to GCS
                gcs_path = uploader.upload_file(str(file_path), f"uploads/{file_path.name}")
                
                # Create job data in the format expected by the processor
                job_data = {
                    "file_path": f"{bucket_name}/uploads/{file_path.name}",  # Include bucket name in path
                    "prompt": prompt,  # Optional prompt for analysis
                    "job_id": str(uuid.uuid4())  # Unique identifier for tracking
                }
                
                # Dispatch job to processing topic
                pubsub_client.publish_job(job_data)
                console.print(f"[green]Dispatched: {file_path.name} (took {time.time() - file_start:.2f} seconds)[/green]")
                progress_queue.put(("dispatched", str(file_path)))
                
            except Exception as e:
                console.print(f"[red]Error in dispatch thread: {str(e)}[/red]")
                continue
        
    except Exception as e:
        console.print(f"[red]Dispatch thread error: {str(e)}[/red]")

@app.command()
def process(
    files: List[str] = typer.Argument(..., help="File paths or glob patterns to process"),
    prompt: str = typer.Option(..., "--prompt", "-p", help="Prompt to use for processing"),
    project_id: str = typer.Option(..., "--project-id", help="GCP project ID"),
    bucket_name: str = typer.Option(..., "--bucket", help="GCS bucket name"),
    processing_topic: str = typer.Option(..., "--processing-topic", help="Pub/Sub topic for processing jobs"),
    results_subscription: str = typer.Option(..., "--results-subscription", help="Pub/Sub subscription for results"),
):
    """Dispatch files to GCP Pub/Sub and listen for results."""
    try:
        start_time = time.time()
        
        # Expand glob patterns and validate files
        console.print("[yellow]Validating files...[/yellow]")
        expanded_files = []
        for pattern in files:
            matches = glob.glob(pattern)
            expanded_files.extend(matches)
        
        if not expanded_files:
            console.print("[red]Error: No valid files found[/red]")
            raise typer.Exit(1)
        
        valid_files = validate_file_paths(expanded_files)
        if not valid_files:
            console.print("[red]Error: No valid files to process[/red]")
            raise typer.Exit(1)
        
        console.print(f"[yellow]Found {len(valid_files)} valid files to process[/yellow]")
        
        # Create a queue for thread communication
        progress_queue = Queue()
        
        # Start dispatch thread
        dispatch_thread = threading.Thread(
            target=dispatch_job_thread,
            args=(valid_files, prompt, project_id, bucket_name, processing_topic, progress_queue)
        )
        dispatch_thread.start()
        
        # Initialize result listener
        console.print("[yellow]Initializing result listener...[/yellow]")
        result_listener = ResultListener(project_id=project_id, subscription_id=results_subscription)
        results = []
        
        # Process results
        for result in result_listener.listen():
            # Only process results with /tmp/ in the file path
            file_path = result.get('file_path', '')
            if '/tmp/' not in file_path:
                continue
                
            results.append(result)
            console.print("\n[green]Received result:[/green]")
            console.print(f"[cyan]File:[/cyan] {result.get('file_path', 'unknown')}")
            console.print(f"[cyan]Job ID:[/cyan] {result.get('job_id', 'unknown')}")
            console.print(f"[cyan]Content:[/cyan] {result.get('content', 'No content provided')}")
            console.print("-" * 50)
            
            if len(results) == len(valid_files):
                break
        
        # Wait for dispatch thread to complete
        dispatch_thread.join()
        
        total_time = time.time() - start_time
        console.print(f"\n[green]Process completed in {total_time:.2f} seconds[/green]")
        console.print(f"[green]Dispatched {len(valid_files)} jobs and received {len(results)} results[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app() 