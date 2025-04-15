from google.cloud import pubsub_v1
import json
from typing import Generator, Dict, Any
from queue import Queue, Empty
import threading
from rich.console import Console
import time

console = Console()

class ResultListener:
    """Listens for results from a Pub/Sub subscription."""
    
    def __init__(self, project_id: str, subscription_id: str):
        """Initialize the result listener.
        
        Args:
            project_id: GCP project ID
            subscription_id: ID of the subscription to listen on
        """
        if not project_id or not subscription_id:
            raise ValueError("Project ID and subscription ID are required")
            
        self.project_id = project_id
        self.subscription_id = subscription_id
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_id)
        self.message_queue = Queue()
        self.stop_event = threading.Event()
        self.last_heartbeat = time.time()
        
        # Configure flow control for better performance
        self.flow_control = pubsub_v1.types.FlowControl(
            max_messages=100,
            max_bytes=100 * 1024 * 1024,
            max_lease_duration=60
        )
    
    def _message_callback(self, message: pubsub_v1.subscriber.message.Message) -> None:
        """Process a received message."""
        try:
            # Decode and process the message
            data = json.loads(message.data.decode('utf-8'))
            job_id = data.get('job_id', 'unknown')
            console.print(f"[green]Received result for job {job_id}[/green]")
            
            # Put the message in the queue
            self.message_queue.put(data)
            
            # Acknowledge the message
            message.ack()
            
        except Exception as e:
            console.print(f"[red]Error processing message: {str(e)}[/red]")
            message.nack()
    
    def listen(self) -> Generator[Dict[str, Any], None, None]:
        """Listen for results from the subscription."""
        try:
            # Start the streaming pull
            streaming_pull_future = self.subscriber.subscribe(
                self.subscription_path,
                callback=self._message_callback,
                flow_control=self.flow_control
            )
            
            try:
                # Process messages until interrupted
                while not self.stop_event.is_set():
                    try:
                        # Show heartbeat every 5 seconds
                        current_time = time.time()
                        if current_time - self.last_heartbeat >= 5:
                            console.print("[yellow]Listening for results...[/yellow]")
                            self.last_heartbeat = current_time
                        
                        # Get message from queue with short timeout
                        result = self.message_queue.get(timeout=0.5)
                        yield result
                    except Empty:
                        continue
                    except Exception as e:
                        console.print(f"[red]Error in listen loop: {str(e)}[/red]")
                        raise
            except KeyboardInterrupt:
                self.stop_event.set()
            finally:
                streaming_pull_future.cancel()
                try:
                    streaming_pull_future.result(timeout=5.0)  # Add timeout to prevent blocking
                except Exception:
                    pass  # Ignore timeout errors during shutdown
                
        except Exception as e:
            console.print(f"[red]Error in result listener: {str(e)}[/red]")
            raise
    
    def stop(self):
        """Stop the listener."""
        self.stop_event.set() 