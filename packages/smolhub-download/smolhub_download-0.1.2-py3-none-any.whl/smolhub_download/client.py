import os
import requests
import torch
from tqdm import tqdm
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

class SmolHubClient:
    def __init__(self, base_url="https://smolhub-flask-server.onrender.com/", token=None):
        self.base_url = base_url.rstrip('/')
        self.token = token
        
    def _get_headers(self):
        """Get headers for API requests, including authentication token if available."""
        headers = {}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def upload_model(self, model_path, markdown_path=None, name=None, description=None):
        """
        Upload a model file to SmolHub with optional markdown documentation.
        
        Args:
            model_path (str): Path to the model file
            markdown_path (str, optional): Path to the markdown documentation file
            name (str, optional): Name of the model (defaults to filename)
            description (str, optional): Short description of the model
            
        Returns:
            dict: Response from the server
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
            
        if markdown_path and not os.path.exists(markdown_path):
            raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

        # Token is required for uploads
        if not self.token:
            raise ValueError("Authentication token is required for uploading models. "
                             "Please provide a token in the client constructor.")

        # If name not provided, use filename
        if name is None:
            name = os.path.basename(model_path)

        # Create the fields dict for the multipart encoder
        fields = {
            'name': name,
            'description': description or '',
            'file': (os.path.basename(model_path), open(model_path, 'rb'))
        }
        
        # Add markdown file if provided
        if markdown_path:
            fields['markdown_file'] = (os.path.basename(markdown_path), open(markdown_path, 'rb'))

        # Create the multipart encoder
        encoder = MultipartEncoder(fields)

        # Create a monitor to track upload progress
        progress = tqdm(desc=f"Uploading {name}", total=encoder.len, unit='iB', unit_scale=True)
        
        def callback(monitor):
            progress.n = monitor.bytes_read
            progress.refresh()

        monitor = MultipartEncoderMonitor(encoder, callback)

        # Combine headers
        headers = self._get_headers()
        headers['Content-Type'] = monitor.content_type

        try:
            response = requests.post(
                f"{self.base_url}/api/models",
                data=monitor,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        finally:
            progress.close()
            # Close the file handles opened by MultipartEncoder
            encoder.fields['file'][1].close()
            if markdown_path:
                encoder.fields['markdown_file'][1].close()

    def list_models(self):
        """Get a list of all available models."""
        response = requests.get(
            f"{self.base_url}/api/models", 
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json().get('models', [])

    def download_model(self, model_name, output_path, download_markdown=False, markdown_path=None):
        """
        Download a model by name.
        
        Args:
            model_name (str): Name of the model to download
            output_path (str): Path to save the downloaded model file
            download_markdown (bool, optional): Whether to download the markdown documentation
            markdown_path (str, optional): Path to save the markdown file (required if download_markdown is True)
            
        Returns:
            str: Path to the downloaded model file
        """
        # Download the model file
        response = requests.get(
            f"{self.base_url}/api/models/download/{model_name}",
            stream=True,
            headers=self._get_headers()
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
                        
        # Download the markdown file if requested
        if download_markdown:
            if not markdown_path:
                raise ValueError("markdown_path must be provided when download_markdown is True")
                
            response = requests.get(
                f"{self.base_url}/api/models/download_markdown/{model_name}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            print(f"Markdown documentation saved to {markdown_path}")

        return output_path
        
    def upload_dataset(self, dataset_path, markdown_path=None, name=None, description=None):
        """
        Upload a dataset file to SmolHub with optional markdown documentation.
        
        Args:
            dataset_path (str): Path to the dataset file
            markdown_path (str, optional): Path to the markdown documentation file
            name (str, optional): Name of the dataset (defaults to filename)
            description (str, optional): Short description of the dataset
            
        Returns:
            dict: Response from the server
        """
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
            
        if markdown_path and not os.path.exists(markdown_path):
            raise FileNotFoundError(f"Markdown file not found: {markdown_path}")

        # Token is required for uploads
        if not self.token:
            raise ValueError("Authentication token is required for uploading datasets. "
                             "Please provide a token in the client constructor.")

        # If name not provided, use filename
        if name is None:
            name = os.path.basename(dataset_path)

        # Create the fields dict for the multipart encoder
        fields = {
            'name': name,
            'description': description or '',
            'file': (os.path.basename(dataset_path), open(dataset_path, 'rb'))
        }
        
        # Add markdown file if provided
        if markdown_path:
            fields['markdown_file'] = (os.path.basename(markdown_path), open(markdown_path, 'rb'))

        # Create the multipart encoder
        encoder = MultipartEncoder(fields)

        # Create a monitor to track upload progress
        progress = tqdm(desc=f"Uploading {name}", total=encoder.len, unit='iB', unit_scale=True)
        
        def callback(monitor):
            progress.n = monitor.bytes_read
            progress.refresh()

        monitor = MultipartEncoderMonitor(encoder, callback)

        # Combine headers
        headers = self._get_headers()
        headers['Content-Type'] = monitor.content_type

        try:
            response = requests.post(
                f"{self.base_url}/api/datasets",
                data=monitor,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        finally:
            progress.close()
            # Close the file handles opened by MultipartEncoder
            encoder.fields['file'][1].close()
            if markdown_path:
                encoder.fields['markdown_file'][1].close()
                
    def list_datasets(self):
        """Get a list of all available datasets."""
        response = requests.get(
            f"{self.base_url}/api/datasets", 
            headers=self._get_headers()
        )
        response.raise_for_status()
        return response.json().get('datasets', [])
        
    def download_dataset(self, dataset_name, output_path, download_markdown=False, markdown_path=None):
        """
        Download a dataset by name.
        
        Args:
            dataset_name (str): Name of the dataset to download
            output_path (str): Path to save the downloaded dataset file
            download_markdown (bool, optional): Whether to download the markdown documentation
            markdown_path (str, optional): Path to save the markdown file (required if download_markdown is True)
            
        Returns:
            str: Path to the downloaded dataset file
        """
        # Download the dataset file
        response = requests.get(
            f"{self.base_url}/api/datasets/download/{dataset_name}",
            stream=True,
            headers=self._get_headers()
        )
        response.raise_for_status()

        # Get total file size for progress bar
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='iB',
                unit_scale=True,
                desc=f"Downloading {dataset_name}"
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        size = f.write(chunk)
                        pbar.update(size)
                        
        # Download the markdown file if requested
        if download_markdown:
            if not markdown_path:
                raise ValueError("markdown_path must be provided when download_markdown is True")
                
            response = requests.get(
                f"{self.base_url}/api/datasets/download_markdown/{dataset_name}",
                headers=self._get_headers()
            )
            response.raise_for_status()
            
            with open(markdown_path, 'w', encoding='utf-8') as f:
                f.write(response.text)
                
            print(f"Markdown documentation saved to {markdown_path}")

        return output_path