from bson import ObjectId

# Utility function to convert ObjectId to string recursively
def convert_object_id_to_str(data):
    if isinstance(data, list):
        return [convert_object_id_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_object_id_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data