from .aurora import DischargeSummary, AuroraStore
from clients.athena import AthenaClient

class DischargeRepo:
    
    def __init__(self, client=None, store=None):
        self.client = client
        self.store = store
    
    def create(self, data, payload):
        submission_model = DischargeSummary(**data)
        upload = self.client.upload_clinical_document(payload)
        record = self.store.create(submission_model)
        if upload and record:
            return True 
        

        