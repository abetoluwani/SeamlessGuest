from datetime import datetime
import random
# import uuid


def get_timestamp():
    # # Get the current datetime in UTC
    # current_time = datetime.utcnow()

    # # Convert datetime to ISO 8601 format (ISO string)
    # iso_timestamp = current_time.isoformat()

    iso_timestamp = datetime.now().isoformat()
    return iso_timestamp

# def create_id():
#     """
#     Function to generate a unique ID with max 10 characters.
#     """
#     return str(uuid.uuid4())[:5]


import random

def create_id():
    """
    Function to generate a unique 5-digit numerical ID.
    """
    return ''.join(random.choices('0123456789', k=5))
