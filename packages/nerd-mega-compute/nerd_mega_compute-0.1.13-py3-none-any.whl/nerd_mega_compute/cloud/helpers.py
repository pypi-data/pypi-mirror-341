from ..utils import debug_print

def fetch_nerd_data_reference(data_ref):
    """
    Retrieve data from a cloud storage reference.
    
    This function is intended to be used inside cloud compute functions to retrieve
    large binary data that was automatically uploaded to cloud storage.
    
    Args:
        data_ref (dict): A data reference object containing __nerd_data_reference key
        
    Returns:
        The retrieved data from cloud storage
    """
    # Check if this is a valid data reference
    if not isinstance(data_ref, dict):
        raise ValueError("Data reference must be a dictionary")
        
    # Check for our special reference format
    if "__nerd_data_reference" in data_ref:
        data_id = data_ref["__nerd_data_reference"]
        debug_print(f"Fetching data from cloud storage reference: {data_id}")
        
        # Import locally to avoid circular imports
        from .storage import fetch_nerd_cloud_storage
        return fetch_nerd_cloud_storage(data_id)
        
    # If this is not our reference format, return as-is
    return data_ref