from ..firebase import db

class PropertyService:
    def __init__(self):
        self.model = db.collection("rooms")

    def get_initial_schema(self, data=None):
        initial_schema = {
            'RoomNumber': "",
            'BuildingName': "",
            'RoomLatitude': "",
            'RoomLongitude': "",
            'RoomSize': "",
            'Beds': "",
            'Individuals': "",
            'ViewDescription': "",
            'price': 0,
            **(data or {})
        }
        return initial_schema

    def get_by_id(self, id):
        doc_ref = self.model.where('RoomNumber', '==', id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def get_all(self):
        rooms = []
        docs = self.model.stream()
        for doc in docs:
            rooms.append(doc.to_dict())
        return rooms

    def create(self, room_data):
        initial_data = self.get_initial_schema(room_data)
        doc_ref = self.model.document()
        doc_ref.set(initial_data)
        return initial_data

    def update(self, id, update_data):
        doc_ref = self.model.document(id)
        doc_ref.update(update_data)
        return update_data

    def delete(self, id):
        doc_ref = self.model.document(id)
        doc_ref.delete()
        return True

# Example usage:
property_service = PropertyService()

# Create a new room
room_data = {
    'RoomNumber': "301",
    'BuildingName': 'Main Building',
    'RoomLatitude': 37.7749,
    'RoomLongitude': -122.4194,
    'RoomSize': 180,
    'Beds': 1,
    'Individuals': 1,
    'ViewDescription': 'City View',
    'price': 500
}
property_service.create(room_data)

# Read all rooms
all_rooms = property_service.get_all()
print("All Rooms:")
for room in all_rooms:
    print(room)

# # Update a room
# update_data = {
#     'BuildingName': 'New Building',
#     'RoomLatitude': 37.7749,
#     'RoomLongitude': -122.4194,
#     'RoomSize': 180,
#     'Beds': 1,
#     'Individuals': 1,
#     'ViewDescription': 'City View'
# }
# property_service.update("301", update_data)

# Delete a room
# property_service.delete("301")
