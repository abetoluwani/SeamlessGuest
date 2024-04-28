from datetime import datetime

def get_timestamp():
    # # Get the current datetime in UTC
    # current_time = datetime.utcnow()

    # # Convert datetime to ISO 8601 format (ISO string)
    # iso_timestamp = current_time.isoformat()

    iso_timestamp = datetime.now().isoformat()
    return iso_timestamp
