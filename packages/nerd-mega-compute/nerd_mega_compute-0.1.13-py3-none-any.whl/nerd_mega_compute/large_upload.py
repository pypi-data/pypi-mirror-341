import os
import requests
import json
from .utils import debug_print
from .spinner import Spinner

# Size threshold for using large file API (50MB)
LARGE_FILE_THRESHOLD = 50 * 1024 * 1024  # 50MB in bytes

def is_large_file(data):
    """
    Determine if the data should be treated as a large file

    Args:
        data: Data to check

    Returns:
        bool: True if the data exceeds the large file threshold
    """
    if isinstance(data, bytes):
        return len(data) >= LARGE_FILE_THRESHOLD
    elif isinstance(data, (str, list, dict)):
        # For non-binary data, estimate the size after JSON serialization
        try:
            # Sample-based size estimation for very large objects
            if isinstance(data, (list, dict)) and hasattr(data, "__len__") and len(data) > 1000:
                # Take a sample of the data to estimate total size
                sample_size = min(1000, len(data) // 10)
                if isinstance(data, list):
                    sample = data[:sample_size]
                else:  # dict
                    sample = {k: data[k] for k in list(data.keys())[:sample_size]}

                json_sample = json.dumps(sample).encode('utf-8')
                estimated_size = len(json_sample) * (len(data) / sample_size)
                return estimated_size >= LARGE_FILE_THRESHOLD
            else:
                # For smaller objects, just serialize directly
                serialized = json.dumps(data).encode('utf-8')
                return len(serialized) >= LARGE_FILE_THRESHOLD
        except (TypeError, OverflowError):
            # If it can't be JSON serialized, we'll need to use str() which may be large
            try:
                sample_str = str(data)[:1000]
                estimated_size = len(sample_str) * (len(str(data)) / len(sample_str))
                return estimated_size >= LARGE_FILE_THRESHOLD
            except:
                # If we can't estimate, assume it's not large
                return False
    else:
        # For other types, try to make a conservative guess
        try:
            import sys
            size = sys.getsizeof(data)
            return size >= LARGE_FILE_THRESHOLD
        except:
            return False

def upload_large_file(data_to_upload, api_key, storage_format=None):
    """
    Handle upload of large files to the cloud storage

    Args:
        data_to_upload: The data to upload
        api_key: The API key for authentication
        storage_format: Format to store data (binary or json)

    Returns:
        dict: Information about the uploaded data
    """
    # Determine storage format if not specified
    if storage_format is None:
        storage_format = 'binary' if isinstance(data_to_upload, bytes) else 'json'

    # Set up the request
    spinner = Spinner("Getting presigned URL for large file upload...")
    spinner.start()

    try:
        # First, get the presigned URL for upload
        headers = {
            'x-api-key': api_key
        }

        response = requests.post(
            'https://lbmoem9mdg.execute-api.us-west-1.amazonaws.com/prod/nerd-mega-compute/data/large',
            headers=headers
        )

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Failed to get presigned URL for large file upload: {response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

        upload_info = response.json()

        # Now prepare to upload the binary data directly to the presigned URL
        upload_url = upload_info['presignedUrl']

        # Convert data to binary if needed
        binary_data = data_to_upload
        if storage_format == 'json' and not isinstance(data_to_upload, bytes):
            try:
                binary_data = json.dumps(data_to_upload).encode('utf-8')
            except (TypeError, OverflowError):
                # If not JSON serializable, convert to string representation
                binary_data = str(data_to_upload).encode('utf-8')

        # Get data size for progress reporting
        data_size = len(binary_data)
        data_size_mb = data_size / (1024 * 1024)

        # Update spinner message
        spinner.update_message(f"Uploading {data_size_mb:.2f}MB to presigned URL...")

        # Upload using PUT method with the correct content-type
        upload_response = requests.put(
            upload_url,
            data=binary_data,
            headers={
                'Content-Type': 'application/octet-stream'
            }
        )

        if upload_response.status_code not in [200, 201, 204]:
            spinner.stop()
            error_msg = f"Failed to upload data to presigned URL: {upload_response.text}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)

        spinner.stop()
        print(f"✅ Large file uploaded successfully! Size: {data_size_mb:.2f}MB")
        print(f"📋 Data ID: {upload_info['dataId']}")
        print(f"🔗 S3 URI: {upload_info['s3Uri']}")

        # Return a response in the same format as the standard upload API
        return {
            'dataId': upload_info['dataId'],
            's3Uri': upload_info['s3Uri'],
            'storageFormat': storage_format,
            'sizeMB': f"{data_size_mb:.2f}"
        }

    except Exception as e:
        spinner.stop()
        print(f"❌ Error during large file upload: {e}")
        raise
    finally:
        spinner.stop()