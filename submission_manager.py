from dataclasses import dataclass
from clients import platoform_client
from repos import discharge_repo_client
from fuzzywuzzy import process
from utilities.parsers import parse_name


@dataclass
class PlatoFormSubmission:
    submission_id: str
    submit_revision: int
    submit_date: str
    form_id: str
    pdf_id: str
    file_name: str
    submit_data: dict
    

class DisChargeSubmissionManager:
    
    def __init__(self, model):
        self.model = model
        self.submission_obj = None
        # athena clioent
    
    def process_submission(self, data, path):
        self.submission_obj = self._load_submission(data)
#         self._download_submission_pdf(path)
        patient_info = self.extract_submit_data(["Chart Number", "PT Name", "Date of Birth"])
        patient_id = validate_patient(patient_info)
        payload = self._create_pdf_payload(patient_id, path)
        if patient_id:
            submission_record = self._create_submission_record()
#         created = discharge_repo_client.create(data=submission_record, payload=payload)
            return True
        # if created:
        #     return True
    
    
    def _load_submission(self, dictionary):
        if dictionary:
            curr = dictionary[0]
            submission_obj = self.model(
                file_name=curr.get("pdf")[0].get('display_name'),
                submission_id=curr.get("id"),
                submit_revision=curr.get('submit_revision'),
                submit_date=curr.get('submit_date'),
                form_id=curr.get('form').get('id'),
                pdf_id = curr.get('pdf')[0].get('id'),
                submit_data=curr.get("submit_data")
            )
            
            return submission_obj
        

    def _create_submission_record(self):
        extra_data = self.extract_submit_data(['Provider Name', 'Chart Number', 'Discharge Date', 'Admission Date'])
        return {
            'submission_id': self.submission_obj.submission_id, 
            'submit_revision': self.submission_obj.submit_revision,
            'submit_date': self.submission_obj.submit_date, 
            'form_id': self.submission_obj.form_id,
            'pdf_id': self.submission_obj.pdf_id, 
            'provider_name': extra_data.get('Provider Name'), 
            'chart_number': extra_data.get('Chart Number'), 
            'discharge_date': extra_data.get('Discharge Date'),
            'admission_date': extra_data.get('Admission Date')
        }
        
    
    def extract_submit_data(self, fields):
        if not fields or not isinstance(fields, list):
            raise ValueError("Must pass a list of strings for desired fields")
        
        pt_info = {
            field.get('label', ''): field.get('value', '')
            for field in self.submission_obj.submit_data
            if field.get('label', '') in fields
        }
        return pt_info
    
    
    def _download_submission_pdf(self, path):
        platoform_client.download_pdf(
            self.submission_obj.submission_id,
            self.submission_obj.pdf_id,
            self.submission_obj.file_name,
            path
        )
        return True
    

    def _create_pdf_payload(self, patient_id, path):
        payload = {
            'file_name': self.submission_obj.file_name,
            'dir_path': path,
            'data': {
                'documentsubclass': 'CLINICALDOCUMENT',
                'departmentid': '1',
                'attachmenttype': 'PDF',
                'documenttypeid': 341373, # ID for Discharge Summary
                'patient_id': patient_id,
                'internalnote': 'Discharge Summary'
            }
        }
        return payload

#-------------------------
'''
Manager needs to take in athena proxy client or just call it within these functions
'''


def _get_patient_details(chartnumber):
    # This will return false if a patient id doesnt exsist, at that point we double check with pt_check
    pt_details = patient_details(chartnumber)
    if pt_details and 'error' in pt_details:
        return False
    elif pt_details:
        pt_info = {
            'firstname': pt_details[0]['firstname'],
            'lastname': pt_details[0]['lastname'],
            'dob': pt_details[0]['dob'],
            'patient_id': pt_details[0]['patientid']
        }
        return pt_info


def validate_patient(pt_info):
    '''
        This function attempts to match the patient ID from the submission data with a patient in Athena.
        If a match is found, the corresponding patient ID is returned. If a patient does not
        match in Athena due to a data input error, this function retrieves patient details based on the 
        submission's chart number. It then uses fuzzy matching to compare the patient's name from the 
        submission with the name returned by the patient details API. If a match is found, 
        the function returns the patient ID.
    '''
    firstname, lastname = parse_name(pt_info['PT Name'])
    patient_id = patient_check(
        firstname,
        lastname,
        pt_info['Date of Birth']
    )
    if patient_id:
        return patient_id
  
    pt_details = _get_patient_details(pt_info['Chart Number'])
    if not pt_details:
        return
    
    valid_name = _validate_patient_name(pt_info, pt_details)
    if not valid_name:
        return
    
    return pt_details['patient_id']
   

def _validate_patient_name(patient_info, patient_details):
    patient_name = f"{patient_details['firstname']} {patient_details['lastname']}"
    if _match_name(patient_info['PT Name'], [patient_name]):
        return True


def _match_name(query: str, keys: list, threshold: int=80, processor=None) -> str:
    result = process.extractOne(query, keys, processor=processor)
    if not result:
        return
    key, confidence = result
    if confidence >= threshold:
        return key
  
