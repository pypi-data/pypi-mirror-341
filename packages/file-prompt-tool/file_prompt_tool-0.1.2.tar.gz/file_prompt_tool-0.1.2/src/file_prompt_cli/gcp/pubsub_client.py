from google.cloud import pubsub_v1
import json
import uuid
import os
from typing import Dict, Any
from rich.console import Console
from datetime import datetime

console = Console()

class PubSubClient:
    """Client for interacting with GCP Pub/Sub."""
    
    def __init__(self, project_id: str, processing_topic_id: str):
        """Initialize the Pub/Sub client.
        
        Args:
            project_id: GCP project ID
            processing_topic_id: ID of the processing topic
        """
        try:
            self.project_id = project_id
            self.processing_topic_id = processing_topic_id
            self.publisher = pubsub_v1.PublisherClient()
            
            # Set up processing topic path
            self.processing_topic_path = self.publisher.topic_path(project_id, processing_topic_id)
            
            # Set up results topic path (fixed name)
            self.results_topic_id = "file-processing-results-topic"
            self.results_topic_path = self.publisher.topic_path(project_id, self.results_topic_id)
            
            console.print(f"[yellow]Processing topic: {self.processing_topic_path}[/yellow]")
            console.print(f"[yellow]Results topic: {self.results_topic_path}[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error initializing PubSubClient: {str(e)}[/red]")
            raise
    
    def publish_job(self, job_data: Dict[str, Any]) -> str:
        """Publish a job to the processing topic."""
        try:
            # Extract the bucket and path from the GCS URI if present
            if 'file_path' in job_data and job_data['file_path'].startswith('gs://'):
                # Remove gs:// prefix but keep bucket name
                job_data['file_path'] = job_data['file_path'].replace('gs://', '')
            
            # Add timestamp to job data
            job_data['timestamp'] = datetime.now().isoformat()
            
            # Encode job data
            encoded_data = json.dumps(job_data).encode('utf-8')
            
            # Publish the message to processing topic
            future = self.publisher.publish(
                self.processing_topic_path,
                encoded_data,
                job_id=job_data.get('job_id', 'unknown')
            )
            message_id = future.result()
            
            return message_id
            
        except Exception as e:
            console.print(f"[red]Error publishing job: {str(e)}[/red]")
            raise
    
    def create_subscription(self, subscription_id: str) -> None:
        """Create a subscription for receiving job results."""
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(
            self.project_id, subscription_id
        )
        
        # Create the subscription
        subscriber.create_subscription(
            request={
                "name": subscription_path,
                "topic": self.processing_topic_path,
            }
        )
    
    def delete_subscription(self, subscription_id: str) -> None:
        """Delete a subscription."""
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(
            self.project_id, subscription_id
        )
        
        # Delete the subscription
        subscriber.delete_subscription(request={"subscription": subscription_path})
    
    def verify_topic_and_subscription(self, subscription_id: str) -> None:
        """Verify that the topics and subscription exist and are connected."""
        try:
            # Verify processing topic exists
            self.publisher.get_topic(topic=self.processing_topic_path)
            console.print(f"[green]Verified processing topic exists[/green]")
            
            # Verify results topic exists
            self.publisher.get_topic(topic=self.results_topic_path)
            console.print(f"[green]Verified results topic exists[/green]")
            
            # Verify subscription exists and is connected to the results topic
            subscriber = pubsub_v1.SubscriberClient()
            subscription_path = subscriber.subscription_path(self.project_id, subscription_id)
            
            try:
                subscription = subscriber.get_subscription(subscription=subscription_path)
                if subscription.topic != self.results_topic_path:
                    console.print(f"[red]Warning: Subscription {subscription_id} is not connected to the results topic![/red]")
                    console.print(f"[red]Expected: {self.results_topic_path}[/red]")
                    console.print(f"[red]Actual: {subscription.topic}[/red]")
                    raise ValueError(f"Subscription {subscription_id} is not connected to the results topic")
                console.print(f"[green]Verified subscription is connected to results topic[/green]")
            except Exception as e:
                console.print(f"[red]Error verifying subscription: {str(e)}[/red]")
                raise
            
        except Exception as e:
            console.print(f"[red]Error verifying topics: {str(e)}[/red]")
            raise 