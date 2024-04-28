
from services.properties.properties import PropertyService
from tools import make_payment


# print(make_payment("1", 'priscykellyr@gmail.com'))

# Create a new room
# room_data = {
#     'RoomNumber': "1",
#     'BuildingName': 'Main Building',
#     'RoomLatitude': 37.7749,
#     'RoomLongitude': -122.4194,
#     'RoomSize': 180,
#     'Beds': 1,
#     'Individuals': 2,
#     'ViewDescription': 'City View',
#     'price': 500000,
# }

# # print(PropertyService.get_by_id("200"))

# PropertyService.create(room_data)

# Read all rooms
# all_rooms = PropertyService.get_all()
# print("All Rooms:")
# for room in all_rooms:
#     print(room)

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
# PropertyService.update("301", update_data)

# Delete a room
# PropertyService.delete("301")