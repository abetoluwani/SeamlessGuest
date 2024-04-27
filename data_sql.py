import pymysql

# Database connection
db = pymysql.connect(
    host='localhost',
    user='root',
    password='Vondabaic2020',
    database='RoomDatabase'
)

def create_room(room_data):
  
    # Create a new room record in the database.
   
   
    cursor = db.cursor()
    sql = "INSERT INTO Rooms (RoomNumber, BuildingName, RoomLatitude, RoomLongitude, RoomSize, Beds, Individuals, ViewDescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (
        room_data['RoomNumber'],
        room_data['BuildingName'],
        room_data['RoomLatitude'],
        room_data['RoomLongitude'],
        room_data['RoomSize'],
        room_data['Beds'],
        room_data['Individuals'],
        room_data['ViewDescription']
    )
    cursor.execute(sql, values)
    db.commit()

def read_rooms():
   
    # List of room records.
   
    cursor = db.cursor()
    sql = "SELECT * FROM Rooms"
    cursor.execute(sql)
    return cursor.fetchall()

def update_room(room_number, new_data):
   
    #  Room number of the room to be updated.
    
    cursor = db.cursor()
    sql = "UPDATE Rooms SET BuildingName = %s, RoomLatitude = %s, RoomLongitude = %s, RoomSize = %s, Beds = %s, Individuals = %s, ViewDescription = %s WHERE RoomNumber = %s"
    values = (
        new_data['BuildingName'],
        new_data['RoomLatitude'],
        new_data['RoomLongitude'],
        new_data['RoomSize'],
        new_data['Beds'],
        new_data['Individuals'],
        new_data['ViewDescription'],
        room_number
    )
    cursor.execute(sql, values)
    db.commit()

def delete_room(room_number):

    # Delete a room record from the database.
    
    cursor = db.cursor()
    sql = "DELETE FROM Rooms WHERE RoomNumber = %s"
    cursor.execute(sql, (room_number,))
    db.commit()

# Example a new room
room_data = {
    'RoomNumber': 301,
    'BuildingName': 'Main Building',
    'RoomLatitude': 37.7749,
    'RoomLongitude': -122.4194,
    'RoomSize': 180,
    'Beds': 1,
    'Individuals': 1,
    'ViewDescription': 'City View'
}
create_room(room_data)

# Read all rooms
all_rooms = read_rooms()
print("All Rooms:")
for room in all_rooms:
    print(room)

# Update a room
update_data = {
    'BuildingName': 'New Building',
    'RoomLatitude': 37.7749,
    'RoomLongitude': -122.4194,
    'RoomSize': 180,
    'Beds': 1,
    'Individuals': 1,
    'ViewDescription': 'City View'
}
update_room(301, update_data)

# Delete a room
delete_room(301)
