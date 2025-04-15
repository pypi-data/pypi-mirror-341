import os
from bloomyai import init, upload_file

def test_local_upload():
    # Reset or ensure no credentials are set
    init()  # No credentials => local mode

    # The file data
    file_data = b"Hello BloomyAI"

    # Upload file
    local_path = upload_file("test_folder/test_file.txt", file_data)

    # Check if file exists
    assert os.path.exists(local_path), "Local file was not created"

    # Clean up
    os.remove(local_path)  # Remove test file
    # Remove folder if empty
    try:
        os.removedirs(os.path.dirname(local_path))
    except OSError:
        pass

# @pytest.mark.skip(reason="Requires valid DigitalOcean Spaces credentials")
def test_s3_upload():
    # Initialize with valid credentials (Fill in your real credentials below)
    init(
        api_key="xxx",
        base_url="http://localhost:8000"
    )

    # The file data
    file_data = b"Hello BloomyAI (S3)"

    # Upload file
    uploaded_url = upload_file("test_folder/test_s3_file.txt", file_data)

    assert "https://local-bloomy.fra1.digitaloceanspaces.com" in uploaded_url
