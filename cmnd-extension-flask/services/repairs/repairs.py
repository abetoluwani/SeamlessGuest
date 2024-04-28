from services.firebase.firebase import *
from utils.index import create_id 

class IRepairRequestService:
    def __init__(self):
        self.model = db.collection("repair_requests")

    def get_initial_schema(self, data=None):
        initial_schema = {
            'room_number': "",
            'description': "",
            'status': "pending",
            **(data or {})
        }
        return initial_schema

    def create(self, repair_request_data):
        initial_data = self.get_initial_schema(repair_request_data)
        # print(initial_data, initial_data['id'])
        # self.model.add(document_id=initial_data['id'], document_data=initial_data)
        print(doc)
        doc = self.model.document().set(initial_data)
        return initial_data

    def get_by_id(self, request_id):
        doc_ref = self.model.document(request_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return None

    def update(self, request_id, update_data):
        doc_ref = self.model.document(request_id)
        doc_ref.set(update_data, merge=True)
        return update_data

    def delete(self, request_id):
        doc_ref = self.model.document(request_id)
        doc_ref.delete()
        return True


RepairRequestService = IRepairRequestService()
