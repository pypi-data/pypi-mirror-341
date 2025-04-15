import os
import requests
from ._config import set_credentials, get_credentials


def init(
    api_key: str = None,
    base_url: str = None,
):
    """
    Initializes the library with credentials to connect to DigitalOcean Spaces.

    If any of these parameters are not provided (or if all are None),
    the library will simply store data locally instead.
    """
    set_credentials(
        api_key=api_key,
        base_url=base_url,
    )


def upload_file(path: str, data: bytes) -> str:
    """
    Uploads the data (bytes) to the location specified by 'path'.
    If valid DigitalOcean Spaces credentials have been initialized with init(),
    it uploads to S3. Otherwise, saves locally under a folder called 'local_uploads'.

    Args:
        path (str): The path (or key) for the file on DO Spaces or local file path.
        data (bytes): The file content in bytes.

    Returns:
        str: A string representing the resource location (URL or local file path).
    """
    creds = get_credentials()
    api_key = creds["api_key"]
    base_url = creds["base_url"]
    # Check if credentials were set
    if api_key and base_url:
        files = {'file': data}
        data = {'path': path}
        headers = {'X-Run-API-Key': api_key}
        response = requests.post(f"{base_url}/v1/file-upload/run/", files=files, data=data, headers=headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to upload file: {response.text}")
        response_data = response.json()
        url = response_data.get("url")
        if not url:
            raise ValueError("No URL returned in the response.")
        return url

    else:
        # No valid credentials, so we store locally
        local_folder = "uploads"
        os.makedirs(local_folder, exist_ok=True)

        # Build full local path
        local_path = os.path.join(local_folder, path)

        # Ensure subdirectories are created if path includes folders
        os.makedirs(os.path.dirname(local_path), exist_ok=True)

        # Write data to local file
        with open(local_path, "wb") as f:
            f.write(data)

        return os.path.abspath(local_path)
