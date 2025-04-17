import functools
import inspect
import pickle
import base64
import zlib
import json
import time
import uuid
import requests
import traceback
import sys

from ..config import NERD_COMPUTE_ENDPOINT, DEBUG_MODE
from ..spinner import Spinner
from ..utils import debug_print, check_job_manually
from .import_utils import extract_imports, _extract_used_names, _filter_imports_by_usage, _get_stdlib_modules
from .job import _active_jobs
from .auth import get_api_key
from .storage import is_large_data, upload_nerd_cloud_storage

def cloud_compute(cores=8, timeout=1800):
    """
    A special function decorator that sends your computation to a powerful cloud server.

    Args:
        cores (int): Number of CPU cores to request (default: 8)
        timeout (int): Maximum time to wait for results in seconds (default: 1800)

    Returns:
        A decorated function that will run in the cloud instead of locally
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check if API_KEY is set before proceeding
            api_key = get_api_key()
            if not api_key:
                raise ValueError(
                    "API_KEY is not set. Please set it using:\n"
                    "1. Create a .env file with API_KEY=your_key_here\n"
                    "2. Or call set_nerd_compute_api_key('your_key_here')"
                )

            print(f"🚀 Running {func.__name__} on cloud server with {cores} cores...")

            # Handle large binary files by using the default endpoint that doesn't require special permissions
            # Skip the _send_compute_job approach since it's causing 403 errors
            debug_print("Using standard cloud compute approach for all data")

            # Step 1: Get the actual code of your function
            source = inspect.getsource(func)

            # Remove the decorator line (first line with @cloud_compute)
            source_lines = source.splitlines()
            if any(line.strip().startswith('@cloud_compute') for line in source_lines):
                cleaned_lines = [line for line in source_lines if not line.strip().startswith('@cloud_compute')]
                source = '\n'.join(cleaned_lines)

            debug_print(f"Extracted function source code:\n{source[:200]}...")

            # Extract all names used in the function code to determine which imports are needed
            used_names = _extract_used_names(source)
            debug_print(f"Names used in function: {used_names}")

            # Extract imports from the function code itself - these are always included
            function_imports = extract_imports(source)
            debug_print(f"Imports from function: {function_imports}")

            # Extract imports from the current module and other modules in the stack
            module_imports = []

            # Collect imports from the caller's module
            try:
                caller_frame = inspect.getouterframes(inspect.currentframe())[1].frame
                caller_globals = caller_frame.f_globals

                # Get the module's source code if possible
                caller_module = inspect.getmodule(caller_frame)
                if caller_module:
                    try:
                        module_source = inspect.getsource(caller_module)
                        all_module_imports = extract_imports(module_source)
                        # Filter module imports to only include those that are used in the function
                        module_imports = _filter_imports_by_usage(all_module_imports, used_names)
                        debug_print(f"Filtered imports from module: {module_imports}")
                    except (IOError, TypeError):
                        for name, val in caller_globals.items():
                            if inspect.ismodule(val) and name in used_names:
                                module_name = val.__name__
                                if module_name not in _get_stdlib_modules() and not module_name.startswith('_'):
                                    module_imports.append(f"import {module_name}")
            finally:
                del caller_frame  # Avoid reference cycles

            # Include commonly needed modules for scientific computing, but only if referenced
            common_scientific_modules = [
                ("import numpy as np", ["np", "numpy"]),
                ("import pandas as pd", ["pd", "pandas"]),
                ("from scipy import signal", ["signal"]),
                ("import matplotlib.pyplot as plt", ["plt", "matplotlib"]),
                ("from astropy.io import fits", ["fits"]),
                ("from astropy.table import Table", ["Table"]),
                ("from astropy.wcs import WCS", ["WCS"]),
                ("from astropy.coordinates import SkyCoord", ["SkyCoord"]),
                ("from astropy import units as u", ["u"])
            ]

            # Combine all imports, removing duplicates
            all_imports = list(set(function_imports) | set(module_imports))

            # Add scientific modules only if they're used in the function
            for module_import, module_names in common_scientific_modules:
                if any(name in used_names for name in module_names) and module_import not in all_imports:
                    all_imports.append(module_import)

            # Generate import code block for cloud execution
            import_block = "\n".join(all_imports)
            debug_print(f"Generated import block:\n{import_block}")

            # Add a fallback universal import for edge cases
            universal_imports = """
# Fallback imports for common libraries
try:
    import numpy as np
except ImportError:
    pass
try:
    import pandas as pd
except ImportError:
    pass
try:
    import matplotlib.pyplot as plt
except ImportError:
    pass
"""
            import_block = universal_imports + import_block

            # Step 2: Package up all the data your function needs
            spinner = Spinner("Packaging function and data for cloud execution...")
            spinner.start()

            def serialize_with_chunking(obj):
                try:
                    # Special handling for large binary data
                    if isinstance(obj, bytes) and len(obj) > 10 * 1024 * 1024:  # > 10MB
                        size_mb = len(obj) / (1024 * 1024)
                        debug_print(f"Large binary data detected: {size_mb:.2f} MB")
                        # Upload to cloud storage
                        upload_result = upload_nerd_cloud_storage(obj)
                        debug_print(f"Uploaded large binary data: {upload_result['dataId']}")
                        # Return a reference that can be recognized on the cloud side
                        return {
                            'type': 'bytes_reference',
                            'value': {
                                'data_reference': upload_result['dataId'],
                                's3Uri': upload_result.get('s3Uri', ''),
                                'sizeMB': upload_result.get('sizeMB', size_mb)
                            }
                        }

                    # Regular serialization for normal-sized data
                    pickled = pickle.dumps(obj)
                    compressed = zlib.compress(pickled)
                    encoded = base64.b64encode(compressed).decode('utf-8')
                    return {'type': 'data', 'value': encoded}
                except Exception as e:
                    spinner.stop()
                    print(f"⚠️ Warning: Could not package object: {e}")
                    spinner.start()
                    return {'type': 'string', 'value': str(obj)}

            serialized_args = []
            for arg in args:
                serialized_args.append(serialize_with_chunking(arg))

            serialized_kwargs = {}
            for key, value in kwargs.items():
                serialized_kwargs[key] = serialize_with_chunking(value)

            cloud_code = """
import pickle
import base64
import zlib
import json
import time
import os
import traceback
import sys

# This function unpacks the data we sent
def deserialize_arg(arg_data):
    if arg_data['type'] == 'data':
        try:
            return pickle.loads(zlib.decompress(base64.b64decode(arg_data['value'])))
        except Exception as e:
            print(f"Error deserializing: {e}")
            return arg_data['value']
    else:
        return arg_data['value']

# Debug function to get environment variables
def debug_env():
    env_vars = {}
    for key in os.environ:
        env_vars[key] = os.environ.get(key, 'NOT_SET')
    return env_vars

print(f"Cloud environment: {json.dumps(debug_env())}")

# Auto-imported modules extracted from function code
""" + import_block + """

# Your original function is copied below (without the decorator)
""" + source + """

# Unpack all the arguments
args = []
for arg_data in """ + str(serialized_args) + """:
    args.append(deserialize_arg(arg_data))

# Unpack all the keyword arguments
kwargs = {}
for key, arg_data in """ + str(serialized_kwargs) + """.items():
    kwargs[key] = deserialize_arg(arg_data)

try:
    print(f"Starting cloud execution of """ + func.__name__ + """...")
    result = """ + func.__name__ + """(*args, **kwargs)
    print(f"Function execution completed successfully")

    try:
        print("Packaging results to send back...")
        result_pickled = pickle.dumps(result)
        result_compressed = zlib.compress(result_pickled)
        result_encoded = base64.b64encode(result_compressed).decode('utf-8')
        print(f"Results packaged (size: {len(result_encoded)} characters)")

        print("RESULT_MARKER_BEGIN")
        print(f'{{"result_size": {len(result_encoded)}, "result": "{result_encoded}"}}')
        print("RESULT_MARKER_END")

        with open('/tmp/result.json', 'w') as f:
            f.write(f'{{"result_size": {len(result_encoded)}, "result": "{result_encoded}"}}')
        print("Saved result to /tmp/result.json")

        try:
            alternative_paths = ['/mnt/data/result.json', './result.json']
            for alt_path in alternative_paths:
                try:
                    with open(alt_path, 'w') as f:
                        f.write(f'{{"result_size": {len(result_encoded)}, "result": "{result_encoded}"}}')
                    print(f"Also saved result to {alt_path}")
                except:
                    pass
        except Exception as e:
            print(f"Error saving to alternative paths: {e}")

        sys.stdout.flush()
        time.sleep(5)
    except Exception as e:
        print(f"Error packaging results: {e}")
        print(traceback.format_exc())
        raise
except Exception as e:
    print(f"EXECUTION ERROR: {e}")
    print(traceback.format_exc())
    raise
"""
            job_id = str(uuid.uuid4())
            debug_print(f"Job ID: {job_id}")

            spinner.update_message(f"Sending {func.__name__} to cloud server...")

            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key
            }

            try:
                debug_print(f"Sending to API with job ID: {job_id}")

                payload = {"code": cloud_code, "cores": cores, "jobId": job_id}

                debug_print(f"Payload keys: {list(payload.keys())}")
                debug_print(f"Code length: {len(cloud_code)}")

                response = requests.post(
                    NERD_COMPUTE_ENDPOINT,
                    json=payload,
                    headers=headers,
                    timeout=30
                )

                debug_print(f"POST response status: {response.status_code}")
                if response.status_code != 200:
                    debug_print(f"Error response body: {response.text[:500]}...")

                if response.status_code != 200:
                    spinner.stop()
                    print(f"❌ Failed to send job: {response.status_code}")
                    if DEBUG_MODE:
                        print(f"Response: {response.text}")
                        check_job_manually(job_id)

                    if response.status_code == 500:
                        try:
                            error_data = response.json()
                            error_message = error_data.get("error", "Unknown error")
                            error_details = error_data.get("details", "")
                            print(f"Error: {error_message}")
                            if error_details:
                                print(f"Details: {error_details}")
                        except Exception as e:
                            print(f"Server error: {response.text[:500]}")

                    return None

                data = response.json()
                job_id = data.get("jobId", job_id)
                batch_job_id = data.get("batchJobId")

                _active_jobs[job_id] = {
                    "function_name": func.__name__,
                    "batch_job_id": batch_job_id,
                    "start_time": time.time()
                }

                if batch_job_id:
                    debug_print(f"AWS Batch job ID: {batch_job_id}")

            except Exception as e:
                spinner.stop()
                print(f"❌ Error sending job to cloud: {e}")
                if DEBUG_MODE:
                    traceback.print_exc()
                return None

            spinner.update_message(f"Running {func.__name__} in the cloud...")
            start_time = time.time()
            result = None
            check_count = 0

            try:
                while True:
                    elapsed = time.time() - start_time
                    check_count += 1

                    if elapsed > timeout:
                        spinner.stop()
                        print(f"❌ Function timed out after {timeout} seconds")
                        _active_jobs.pop(job_id, None)
                        return None

                    try:
                        result_response = requests.get(
                            NERD_COMPUTE_ENDPOINT,
                            headers=headers,
                            params={"jobId": job_id, "debug": "true"},
                            timeout=10
                        )

                        if check_count % 10 == 0 or DEBUG_MODE:
                            debug_print(f"GET response status: {result_response.status_code}")
                            try:
                                debug_print(f"GET response text: {result_response.text[:200]}...")
                            except Exception:
                                debug_print("Could not display response text")

                        if result_response.status_code != 200:
                            if result_response.status_code == 202:
                                try:
                                    status_data = result_response.json()
                                    status_message = status_data.get('status', 'Unknown status')
                                    if len(status_message) > 50:
                                        status_message = status_message[:47] + "..."
                                    spinner.update_message(f"Job: {status_message} ({int(elapsed)}s)")
                                except Exception:
                                    spinner.update_message(f"Job processing... ({int(elapsed)}s)")

                                if elapsed > timeout:
                                    spinner.stop()
                                    print(f"\n❌ Job timed out after {int(elapsed)} seconds")
                                    _active_jobs.pop(job_id, None)
                                    return None

                                time.sleep(2)
                                continue
                            elif result_response.status_code == 500:
                                try:
                                    error_data = result_response.json()
                                    _active_jobs.pop(job_id, None)
                                    return process_error_response(error_data, spinner, elapsed)
                                except Exception as e:
                                    debug_print(f"Error parsing failure response: {e}")
                                    spinner.stop()
                                    print(f"\n❌ Request failed with status {result_response.status_code}")
                                    _active_jobs.pop(job_id, None)
                                    return None

                            if check_count >= 30:
                                spinner.stop()
                                print(f"\n❌ Job failed with unexpected status code: {result_response.status_code}")
                                try:
                                    print(f"Response: {result_response.text[:500]}")
                                except:
                                    pass
                                _active_jobs.pop(job_id, None)
                                return None

                            if check_count % 10 == 0:
                                debug_print(f"Unexpected status code: {result_response.status_code}")
                            time.sleep(2)
                            continue

                        try:
                            result_data = result_response.json()
                            debug_print(f"Result data: {json.dumps(result_data)[:200]}...")

                            if "body" in result_data and isinstance(result_data["body"], str):
                                try:
                                    body_data = json.loads(result_data["body"])
                                    if isinstance(body_data, dict):
                                        result_data = body_data
                                        debug_print("Extracted result from body field")
                                except Exception as e:
                                    debug_print(f"Error parsing body JSON: {e}")

                            if "error" in result_data or ("status" in result_data and result_data.get("status") == "FAILED"):
                                _active_jobs.pop(job_id, None)
                                return process_error_response(result_data, spinner, elapsed)

                            if "result" in result_data:
                                output_text = result_data["result"]
                                debug_print(f"Raw result: {output_text[:200]}")

                                try:
                                    direct_json = json.loads(output_text)
                                    spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                    spinner.stop()
                                    print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                    _active_jobs.pop(job_id, None)
                                    return direct_json
                                except json.JSONDecodeError:
                                    debug_print("Output is not direct JSON, looking for markers")

                                if "RESULT_MARKER_BEGIN" in output_text and "RESULT_MARKER_END" in output_text:
                                    try:
                                        start_marker = output_text.index("RESULT_MARKER_BEGIN") + len("RESULT_MARKER_BEGIN")
                                        end_marker = output_text.index("RESULT_MARKER_END")
                                        result_json_str = output_text[start_marker:end_marker].strip()
                                        debug_print(f"Extracted from markers: {result_json_str}")

                                        try:
                                            result_json = json.loads(result_json_str)

                                            if "error" in result_json:
                                                _active_jobs.pop(job_id, None)
                                                return process_error_response(result_json, spinner, elapsed)

                                            if "result" in result_json and "result_size" in result_json:
                                                try:
                                                    encoded_result = result_json["result"]
                                                    decoded_result = pickle.loads(zlib.decompress(base64.b64decode(encoded_result)))
                                                    spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                                    spinner.stop()
                                                    print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                                    _active_jobs.pop(job_id, None)
                                                    return decoded_result
                                                except Exception as e:
                                                    debug_print(f"Error decoding result: {e}")

                                            spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                            spinner.stop()
                                            print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                            _active_jobs.pop(job_id, None)
                                            return result_json
                                        except json.JSONDecodeError:
                                            debug_print("Result between markers is not JSON")
                                            try:
                                                result_value = eval(result_json_str)
                                                spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                                spinner.stop()
                                                print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                                _active_jobs.pop(job_id, None)
                                                return result_value
                                            except:
                                                spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                                spinner.stop()
                                                print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                                _active_jobs.pop(job_id, None)
                                                return result_json_str
                                    except Exception as e:
                                        debug_print(f"Error processing markers: {e}")

                                for line in output_text.split('\n'):
                                    if line.strip().startswith("{") and line.strip().endswith("}"):
                                        try:
                                            line_json = json.loads(line)
                                            if isinstance(line_json, dict) and "error" not in line_json:
                                                spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                                spinner.stop()
                                                print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                                _active_jobs.pop(job_id, None)
                                                return line_json
                                        except:
                                            pass

                                clean_output = output_text
                                if "RESULT_MARKER_BEGIN" in clean_output and "RESULT_MARKER_END" in clean_output:
                                    try:
                                        start_marker = clean_output.index("RESULT_MARKER_BEGIN")
                                        end_marker = clean_output.index("RESULT_MARKER_END") + len("RESULT_MARKER_END")
                                        marker_content = clean_output[start_marker + len("RESULT_MARKER_BEGIN"):clean_output.index("RESULT_MARKER_END")].strip()
                                        try:
                                            result_value = eval(marker_content)
                                            spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                            spinner.stop()
                                            print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                            _active_jobs.pop(job_id, None)
                                            return result_value
                                        except:
                                            spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                            spinner.stop()
                                            print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                            _active_jobs.pop(job_id, None)
                                            return marker_content
                                    except Exception as e:
                                        debug_print(f"Error cleaning markers: {e}")

                                spinner.update_message(f"Cloud computation completed in {int(elapsed)}s")
                                spinner.stop()
                                print(f"✅ {func.__name__} completed in {int(elapsed)}s")
                                _active_jobs.pop(job_id, None)
                                return clean_output

                        except Exception as e:
                            debug_print(f"Error processing response: {e}")
                            if DEBUG_MODE:
                                traceback.print_exc()

                        if elapsed > timeout - 30:
                            spinner.stop()
                            print(f"\n❌ Job timed out after {int(elapsed)} seconds")
                            _active_jobs.pop(job_id, None)
                            return None

                    except Exception as e:
                        debug_print(f"Error in job status check: {e}")
                        if DEBUG_MODE:
                            traceback.print_exc()

                    time.sleep(2)
            finally:
                _active_jobs.pop(job_id, None)

        return wrapper
    return decorator

def process_error_response(response_data, spinner, elapsed_time):
    """Process an error response and display meaningful messages to the user."""
    spinner.stop()

    error_msg = "Unknown error occurred"
    details = ""

    try:
        if isinstance(response_data, dict):
            error_msg = response_data.get('error', error_msg)
            details = response_data.get('details', '')

            if 'body' in response_data and isinstance(response_data['body'], str):
                try:
                    body_data = json.loads(response_data['body'])
                    if isinstance(body_data, dict):
                        error_msg = body_data.get('error', error_msg)
                        details = body_data.get('details', details)
                except:
                    pass
    except:
        pass

    print(f"\n❌ Cloud job failed after {int(elapsed_time)}s: {error_msg}")
    if details:
        print(f"Error details:\n{details}")

    return None

def _send_compute_job(function_info, args, kwargs, timeout=3600):
    """
    Send a compute job to the NERD compute service.

    Args:
        function_info: Information about the function to execute
        args: Positional arguments for the function
        kwargs: Keyword arguments for the function
        timeout: Maximum time to wait for the job to complete (default: 1 hour)

    Returns:
        The result of the computation
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "API_KEY is not set. Please set it using:\n"
            "1. Create a .env file with NERD_COMPUTE_API_KEY=your_key_here\n"
            "2. Or call set_nerd_compute_api_key('your_key_here')"
        )

    # Check if any argument is too large for direct request and use cloud storage
    large_args = []
    large_kwargs = {}

    # Debug logging for argument sizes
    debug_print(f"Checking argument sizes for function: {function_info['name']}")
    for i, arg in enumerate(args):
        debug_print(f"Arg {i} type: {type(arg).__name__}")
        if isinstance(arg, bytes):
            debug_print(f"Arg {i} size: {len(arg) / (1024 * 1024):.2f} MB")

    # Process positional arguments
    serialized_args = []
    for i, arg in enumerate(args):
        # Force large file handling for binary data > 10MB regardless of is_large_data result
        if isinstance(arg, bytes) and len(arg) > 10 * 1024 * 1024:
            debug_print(f"Forcing large file handling for binary arg {i}")
            large_args.append(i)
            upload_result = upload_nerd_cloud_storage(arg)
            serialized_args.append({
                "data_reference": {
                    "type": "cloud_storage",
                    "dataId": upload_result["dataId"]
                }
            })
        elif is_large_data(arg):
            large_args.append(i)
            upload_result = upload_nerd_cloud_storage(arg)
            serialized_args.append({
                "data_reference": {
                    "type": "cloud_storage",
                    "dataId": upload_result["dataId"]
                }
            })
        else:
            serialized_args.append(arg)

    # Process keyword arguments
    serialized_kwargs = {}
    for key, value in kwargs.items():
        # Force large file handling for binary data > 10MB
        if isinstance(value, bytes) and len(value) > 10 * 1024 * 1024:
            debug_print(f"Forcing large file handling for binary kwarg {key}")
            large_kwargs[key] = value
            upload_result = upload_nerd_cloud_storage(value)
            serialized_kwargs[key] = {
                "data_reference": {
                    "type": "cloud_storage",
                    "dataId": upload_result["dataId"]
                }
            }
        elif is_large_data(value):
            large_kwargs[key] = value
            upload_result = upload_nerd_cloud_storage(value)
            serialized_kwargs[key] = {
                "data_reference": {
                    "type": "cloud_storage",
                    "dataId": upload_result["dataId"]
                }
            }
        else:
            serialized_kwargs[key] = value

    # Prepare the request for submission
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    endpoint = f"{NERD_COMPUTE_ENDPOINT}/compute"

    job_id = str(uuid.uuid4())
    request_payload = {
        "function": function_info,
        "args": serialized_args,
        "kwargs": serialized_kwargs,
        "jobId": job_id,
        "largeArgs": large_args,
        "largeKwargs": list(large_kwargs.keys())
    }

    spinner = Spinner("Sending job to cloud compute service...")
    spinner.start()

    try:
        debug_print(f"Sending compute job to {endpoint}")
        debug_print(f"Job ID: {job_id}")
        debug_print(f"Large args: {large_args}")
        debug_print(f"Large kwargs: {list(large_kwargs.keys())}")

        response = requests.post(
            endpoint,
            headers=headers,
            json=request_payload,
            timeout=30
        )

        debug_print(f"Response status: {response.status_code}")

        if response.status_code != 200:
            spinner.stop()
            error_msg = f"Failed to send job: {response.status_code}"
            print(f"❌ {error_msg}")
            if DEBUG_MODE:
                try:
                    debug_print(f"Response body: {response.text}")
                except:
                    pass
            return None

        result = response.json()
        job_id = result.get("jobId", job_id)
        debug_print(f"Job submitted successfully. Job ID: {job_id}")

    except Exception as e:
        spinner.stop()
        print(f"❌ Error sending job: {e}")
        if DEBUG_MODE:
            traceback.print_exc()
        return None

    spinner.update_message("Waiting for job to complete...")
    start_time = time.time()

    # Wait for the job to complete
    while True:
        elapsed = time.time() - start_time
        if elapsed > timeout:
            spinner.stop()
            print(f"❌ Job timed out after {int(elapsed)}s")
            return None

        try:
            status_response = requests.get(
                endpoint,
                headers=headers,
                params={"jobId": job_id},
                timeout=30
            )

            if status_response.status_code == 200:
                result = status_response.json()
                if "status" in result and result["status"] == "COMPLETED":
                    spinner.stop()
                    print(f"✅ Job completed in {int(elapsed)}s")
                    return result["result"]
                elif "status" in result and result["status"] == "FAILED":
                    spinner.stop()
                    error_msg = result.get("error", "Unknown error")
                    print(f"❌ Job failed: {error_msg}")
                    if "details" in result:
                        print(f"Details: {result['details']}")
                    return None
                else:
                    status = result.get("status", "UNKNOWN")
                    spinner.update_message(f"Job status: {status} ({int(elapsed)}s elapsed)")
            elif status_response.status_code == 404:
                spinner.stop()
                print(f"❌ Job not found: {job_id}")
                return None
            else:
                debug_print(f"Unexpected status code: {status_response.status_code}")

        except Exception as e:
            debug_print(f"Error checking job status: {e}")
            if DEBUG_MODE:
                traceback.print_exc()

        time.sleep(2)
