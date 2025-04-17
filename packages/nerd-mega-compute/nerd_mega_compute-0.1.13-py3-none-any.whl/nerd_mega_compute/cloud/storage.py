import os
import requests
import json
import pickle
import base64
import zlib
import time
import traceback
import re

from ..config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ..spinner import Spinner
from ..utils import debug_print, check_job_manually
from ..large_upload import is_large_file, upload_large_file
from ..large_download import fetch_large_file
from .auth import get_api_key

def is_large_data(data_to_upload, threshold_mb=10):
    """
    Determines if data should be treated as large based on size estimation.

    Args:
        data_to_upload: The data to check
        threshold_mb: Size threshold in MB (default: 10MB)

    Returns:
        bool: True if data exceeds the threshold, False otherwise
    """
    # Print detailed information about the data
    debug_print(f"Checking if data is large. Type: {type(data_to_upload).__name__}")

    try:
        # First check: Direct byte size for binary data
        if isinstance(data_to_upload, (bytes, bytearray)):
            size_bytes = len(data_to_upload)
            size_mb = size_bytes / (1024 * 1024)
            is_large = size_bytes > threshold_mb * 1024 * 1024
            debug_print(f"Binary data size: {size_mb:.2f} MB, is_large: {is_large}")
            return is_large

        # Second check: Pickle serialization size
        try:
            serialized = pickle.dumps(data_to_upload)
            size_bytes = len(serialized)
            size_mb = size_bytes / (1024 * 1024)
            is_large = size_bytes > threshold_mb * 1024 * 1024
            debug_print(f"Pickle serialized size: {size_mb:.2f} MB, is_large: {is_large}")
            return is_large
        except:
            # Third check: For string or JSON serializable data
            try:
                if isinstance(data_to_upload, str):
                    size_bytes = len(data_to_upload.encode('utf-8'))
                else:
                    serialized = json.dumps(data_to_upload)
                    size_bytes = len(serialized.encode('utf-8'))
                size_mb = size_bytes / (1024 * 1024)
                is_large = size_bytes > threshold_mb * 1024 * 1024
                debug_print(f"String/JSON size: {size_mb:.2f} MB, is_large: {is_large}")
                return is_large
            except:
                # Last resort: Use object representation
                obj_repr = repr(data_to_upload)
                size_bytes = len(obj_repr.encode('utf-8'))
                size_mb = size_bytes / (1024 * 1024)
                is_large = size_bytes > threshold_mb * 1024 * 1024
                debug_print(f"Object repr size: {size_mb:.2f} MB, is_large: {is_large}")
                return is_large
    except Exception as e:
        debug_print(f"Error estimating data size: {e}, assuming it's large")
        return True

def upload_nerd_cloud_storage(data_to_upload, storage_format=None, metadata=None):
    """
    Upload data to Nerd Cloud Storage for later retrieval or sharing.

    Args:
        data_to_upload (any): Data to upload. Can be any JSON-serializable object, or binary data.
        storage_format (str, optional): Format to store the data. Options: 'json' or 'binary'.
                                      If not specified, will be determined automatically.
        metadata (dict, optional): Additional metadata to store with the data.

    Returns:
        dict: Information about the uploaded data including S3 URL and dataId for future retrieval.

    Raises:
        ValueError: If API key is not set or upload fails.
    """
    # Check if API_KEY is set before proceeding
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API_KEY is not set. Please set it using:\n"
            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
            "2. Or call set_nerd_compute_api_key('your_key_here')"
        )

    # Automatically determine storage format if not specified
    if storage_format is None:
        storage_format = 'binary' if isinstance(data_to_upload, bytes) else 'json'

    # Enhanced size detection - check if this is large data
    if is_large_data(data_to_upload):
        debug_print("Detected large data, using large file upload API")
        return upload_large_file(data_to_upload, api_key, storage_format)

    spinner = Spinner("Uploading data to Nerd Cloud Storage...")
    spinner.start()

    try:
        data_type = 'application/octet-stream' if storage_format == 'binary' else 'application/json'

        request_payload = {
            'data': None,
            'storageFormat': storage_format,
            'dataType': data_type
        }

        if storage_format == 'json':
            try:
                json.dumps(data_to_upload)
                request_payload['data'] = data_to_upload
            except (TypeError, OverflowError):
                debug_print("Data is not JSON serializable, converting to string")
                request_payload['data'] = str(data_to_upload)

        elif storage_format == 'binary':
            try:
                if isinstance(data_to_upload, bytes):
                    binary_data = data_to_upload
                else:
                    binary_data = pickle.dumps(data_to_upload)
                encoded_data = base64.b64encode(binary_data).decode('utf-8')
                request_payload['data'] = encoded_data
            except Exception as e:
                spinner.stop()
                error_msg = f"Failed to serialize binary data: {e}"
                print(f"❌ {error_msg}")
                raise ValueError(error_msg)
        else:
            spinner.stop()
            error_msg = f"Unsupported storage format: {storage_format}"
            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        if metadata:
            request_payload['metadata'] = metadata

        headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key,
        }

        endpoint = f"{NERD_COMPUTE_ENDPOINT}/data"

        debug_print(f"Sending data upload request to {endpoint}")
        debug_print(f"Payload type: {type(request_payload)}")
        debug_print(f"Storage format: {storage_format}")

        response = requests.post(
            endpoint,
            headers=headers,
            json=request_payload,
            timeout=30
        )

        debug_print(f"Upload response status: {response.status_code}")

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Upload failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_details = error_data.get("error", "") or error_data.get("details", "")
                if error_details:
                    error_msg += f": {error_details}"
            except Exception:
                error_msg += f": {response.text}"

            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        result = response.json()
        spinner.stop()
        size_mb = result.get('sizeMB', '?')
        print(f"✅ Data uploaded successfully! Size: {size_mb}MB")
        print(f"📋 Data ID: {result.get('dataId', '?')}")
        print(f"🔗 S3 URI: {result.get('s3Uri', '?')}")

        return result

    except Exception as e:
        spinner.stop()
        print(f"❌ Error uploading to cloud storage: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()

def fetch_nerd_cloud_storage(data_id_or_response):
    """
    Fetch data from NERD cloud storage

    Args:
        data_id_or_response: Either the dataId string or the complete upload response object

    Returns:
        The data from cloud storage, automatically decoded if it's binary data
    """
    if isinstance(data_id_or_response, dict) and 'dataId' in data_id_or_response:
        data_id = data_id_or_response['dataId']
        if data_id_or_response.get('sizeMB'):
            try:
                size_mb = float(data_id_or_response.get('sizeMB', '0'))
                if size_mb >= 50:
                    debug_print(f"Detected large file (size: {size_mb}MB), using large file fetch API")
                    api_key = get_api_key()
                    if not api_key:
                        raise ValueError(
                            "API_KEY is not set. Please set it using:\n"
                            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
                            "2. Or call set_nerd_compute_api_key('your_key_here')"
                        )
                    return fetch_large_file(data_id, api_key)
            except (ValueError, TypeError):
                pass
    else:
        data_id = data_id_or_response

    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API_KEY is not set. Please set it using:\n"
            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
            "2. Or call set_nerd_compute_api_key('your_key_here')"
        )

    if not data_id:
        raise ValueError("Either data_id or s3_uri must be provided to fetch data")

    params = {}
    if data_id:
        params["dataId"] = data_id

    spinner = Spinner("Fetching data from Nerd Cloud Storage...")
    spinner.start()

    try:
        endpoint = f"{NERD_COMPUTE_ENDPOINT}/data"
        headers = {
            "x-api-key": api_key
        }

        debug_print(f"Sending data fetch request to {endpoint} with params {params}")
        response = requests.get(
            endpoint,
            headers=headers,
            params=params,
            timeout=30
        )

        debug_print(f"Fetch response status: {response.status_code}")

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Fetch failed with status {response.status_code}"
            try:
                error_data = response.json()
                error_details = error_data.get("error", "") or error_data.get("details", "")
                if error_details:
                    error_msg += f": {error_details}"
            except Exception:
                error_msg += f": {response.text}"

            print(f"❌ {error_msg}")
            raise ValueError(error_msg)

        result = response.json()

        if "contentLength" in result and "presignedUrl" in result:
            debug_print("Detected large file metadata in response, using large file fetch API")
            spinner.stop()
            return fetch_large_file(data_id, api_key)

        if "data" in result:
            data = result["data"]
            storage_format = result.get("storageFormat", "json")

            if storage_format == "binary":
                if isinstance(data, str) and _is_likely_base64(data):
                    try:
                        debug_print("Detected base64 encoded binary data, decoding automatically")
                        binary_data = base64.b64decode(data)
                        try:
                            data = pickle.loads(binary_data)
                        except Exception:
                            data = binary_data
                    except Exception as e:
                        debug_print(f"Error decoding base64 data: {e}")

            spinner.stop()

            if "metadata" in result:
                metadata = result["metadata"]
                content_type = metadata.get("content-type", "unknown")
                size_mb = metadata.get("size-mb", "?")
                print(f"✅ Data fetched successfully! Size: {size_mb}MB, Type: {content_type}")
            else:
                print(f"✅ Data fetched successfully!")

            return data
        else:
            spinner.stop()
            print(f"❓ Unexpected response format. No data found in the response.")
            return result

    except Exception as e:
        spinner.stop()
        print(f"❌ Error fetching from cloud storage: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        raise
    finally:
        spinner.stop()

def _is_likely_base64(s):
    """
    Check if a string is likely a base64 encoded value.

    Args:
        s (str): String to check

    Returns:
        bool: True if string is likely base64 encoded
    """
    if not isinstance(s, str):
        return False

    import re
    if not re.match(r'^[A-Za-z0-9+/]+={0,2}$', s):
        return False

    if len(s) % 4 != 0:
        return False

    try:
        base64.b64decode(s[:20] + '=' * (4 - len(s[:20]) % 4))
        return True
    except Exception:
        return False
