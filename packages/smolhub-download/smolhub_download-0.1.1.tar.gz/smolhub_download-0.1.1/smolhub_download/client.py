import os
import requests
import torch
from tqdm import tqdm
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

class SmolHubClient:
    def __init__(self, base_url="https://smolhub-flask-server.onrender.com/"):
        self.base_url = base_url.rstrip('/')

    def upload_model(self, model_path, name=None, description=None):
        """Upload a model file to SmolHub."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        # If name not provided, use filename
        if name is None:
            name = os.path.basename(model_path)

        # Create the multipart encoder
        encoder = MultipartEncoder({
            'name': name,
            'description': description or '',
            'file': (os.path.basename(model_path), open(model_path, 'rb'))
        })

        # Create a monitor to track upload progress
        progress = tqdm(desc=f"Uploading {name}", total=encoder.len, unit='iB', unit_scale=True)
        
        def callback(monitor):
            progress.n = monitor.bytes_read
            progress.refresh()

        monitor = MultipartEncoderMonitor(encoder, callback)

        try:
            response = requests.post(
                f"{self.base_url}/api/models",
                data=monitor,
                headers={'Content-Type': monitor.content_type}
            )
            response.raise_for_status()
            return response.json()
        finally:
            progress.close()
            # Close the file handle opened by MultipartEncoder
            encoder.fields['file'][1].close()

    def list_models(self):
        """Get a list of all available models."""
        response = requests.get(f"{self.base_url}/api/models")
        response.raise_for_status()
        return response.json().get('models', [])

    def download_model(self, model_name, output_path):
        """Download a model by name."""
        response = requests.get(
            f"{self.base_url}/api/models/download/{model_name}",
            stream=True
        )
        response.raise_for_status()

        # Get total file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='iB',
                unit_scale=True,
                desc=f"Downloading {model_name}"
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        size = f.write(chunk)
                        pbar.update(size)

        return output_path