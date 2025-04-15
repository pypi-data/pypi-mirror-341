from google.cloud import storage
from pathlib import Path
import uuid
import os
from typing import Optional
import logging
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

logger = logging.getLogger(__name__)
console = Console()

class GCSUploader:
    """Handles file uploads to Google Cloud Storage."""
    
    def __init__(self, project_id: str, bucket_name: str):
        """Initialize the GCS uploader.
        
        Args:
            project_id: GCP project ID
            bucket_name: Name of the GCS bucket
        """
        self.project_id = project_id
        self.bucket_name = bucket_name
        self.client = storage.Client(project=project_id)
        self.bucket = self.client.bucket(bucket_name)
    
    def upload_file(self, file_path: str, destination_blob_name: str) -> str:
        """Upload a file to GCS.
        
        Args:
            file_path: Path to the local file
            destination_blob_name: Name to give the file in GCS
            
        Returns:
            The GCS URI of the uploaded file
        """
        try:
            # Create blob
            blob = self.bucket.blob(destination_blob_name)
            
            # Get file size for progress tracking
            file_size = os.path.getsize(file_path)
            
            # Create progress bar
            progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeRemainingColumn(),
                console=console
            )
            
            # Upload with progress tracking
            with progress:
                task = progress.add_task(
                    f"[cyan]Uploading {os.path.basename(file_path)}...",
                    total=file_size
                )
                
                # Upload the file
                with open(file_path, 'rb') as f:
                    blob.upload_from_file(
                        f,
                        content_type='application/octet-stream',
                        size=file_size
                    )
                    # Update progress to 100% when complete
                    progress.update(task, completed=file_size)
            
            # Return the GCS URI
            return f"gs://{self.bucket_name}/{destination_blob_name}"
            
        except Exception as e:
            console.print(f"[red]Error uploading file: {str(e)}[/red]")
            raise
    
    def download_file(self, gcs_path: str, local_path: Path) -> None:
        """Download a file from GCS to local path."""
        # Extract bucket name and blob name from GCS path
        parts = gcs_path.replace("gs://", "").split("/", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid GCS path: {gcs_path}")
            
        bucket_name, blob_name = parts
        logger.info(f"Bucket name: {bucket_name}")
        logger.info(f"Blob name: {blob_name}")
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        try:
            # In Cloud Run, /tmp is the only writable directory
            # Ensure we're using /tmp as the base directory
            if not str(local_path).startswith('/tmp/'):
                local_path = Path('/tmp') / local_path.name
            
            # Create the /tmp directory if it doesn't exist
            tmp_dir = Path('/tmp')
            if not tmp_dir.exists():
                tmp_dir.mkdir(mode=0o777, parents=True, exist_ok=True)
            
            # Download directly to the file
            logger.info(f"Downloading to: {local_path}")
            blob.download_to_filename(str(local_path))
            
            # Verify the download
            if not local_path.exists():
                raise FileNotFoundError(f"File download failed: {local_path} does not exist")
                
            if not local_path.is_file():
                raise ValueError(f"Downloaded path is not a file: {local_path}")
                
            if local_path.stat().st_size == 0:
                raise ValueError(f"Downloaded file is empty: {local_path}")
                
            # Set proper permissions
            local_path.chmod(0o666)
            
            logger.info(f"Successfully downloaded file to {local_path} (size: {local_path.stat().st_size} bytes)")
            
        except Exception as e:
            logger.error(f"Error during download: {str(e)}")
            # Clean up if file was partially downloaded
            if local_path.exists():
                try:
                    local_path.unlink()
                except:
                    pass
            raise
    
    def delete_file(self, gcs_path: str) -> None:
        """Delete a file from GCS."""
        # Extract bucket name and blob name from GCS path
        parts = gcs_path.replace("gs://", "").split("/", 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid GCS path: {gcs_path}")
            
        bucket_name, blob_name = parts
        bucket = self.client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        
        # Delete the file
        blob.delete() 