from services.firebase.firebase import db
from google.cloud.firestore_v1.base_query import FieldFilter, And
from utils.index import get_timestamp
from firebase_admin import firestore

class IPropertyService:
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
            'duration': 1,
            'PurchaseCount': 0,
            'available': True,
            'price': 0,
            'image': '',
            'PurchasedBy': '',
            'PurchaseDate': '',
            **(data or {})
        }
        return initial_schema

    def get_by_id(self, id):
        doc_ref = self.model.where(filter=FieldFilter('RoomNumber', '==', id))
        doc_list = doc_ref.get()

        if(len(doc_list) > 0):
            doc = doc_list[0]
            if doc.exists:
                return doc.to_dict()
            else:
                return None
        else:
            return None


# codeeee
    def get_by_id_and_email(self, id, email):
        doc_ref = self.model.where(filter=And(filters=[FieldFilter('RoomNumber', '==', id), FieldFilter('PurchasedBy', '==', email)]))
        doc_list = doc_ref.get()

        if(len(doc_list) > 0):
            doc = doc_list[0]
            if doc.exists:
                return doc.to_dict()
            else:
                return None
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
        doc_ref = self.model.document(initial_data['RoomNumber'])
        doc_ref.set(initial_data)
        return initial_data

# MY EAR!
    def update(self, id, update_data):
        doc_ref = self.model.document(id)
        doc_ref.set(update_data, merge=True)
        return update_data

    def delete(self, id):
        doc_ref = self.model.document(id)
        doc_ref.delete()
        return True

    def purchase(self, id, email):
        property = self.get_by_id(id)
        newProperty = {
            **property,
            'available': False,
            'PurchasedBy': email,
            'PurchaseDate': get_timestamp(),
            'PurchaseCount': firestore.Increment(1)
        }
        self.update(id, newProperty)
        return newProperty

        
    def obscure(self, data):
        # Define the allowed fields to be returned
        allowed_fields = [
            'RoomNumber',
            'BuildingName',
            'RoomLatitude',
            'RoomLongitude',
            'RoomSize',
            'Beds',
            'Individuals',
            'ViewDescription',
            'price',
            'available'
        ]
        # Filter and obscure sensitive properties
        filtered_data = {}
        for field in allowed_fields:
            filtered_data[field] = data.get(field, '[Obscured]')
        return filtered_data


PropertyService = IPropertyService()