import requests
import logging


class MicroserviceAPIClient:

    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self._token = auth_token
        self._auth_headers = {"Authorization": "token " + auth_token}


    def _adjust_header(self, headers):
            if not headers:
                return self._auth_headers
            else:
                headers["Authorization"] = self._auth_headers.get("Authorization")
            return headers
    

    def _create_request(self, method, endpoint, headers={}, payload={}, params={}, files=[], return_response=False):
        url = self.base_url + endpoint
        headers=self._adjust_header(headers)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=payload,
                params=params,
                files=files
            )
            response.raise_for_status()
            logging.info(f"{method}: {response.status_code} {endpoint}: ")
        except requests.exceptions.HTTPError as error:
            logging.error(f'{method}: {endpoint}: failed, text:: {response.text}, Error: {error}')
            return None
        if return_response:
            return response
        return response.json()
    

    

class AthenaProxyClient(MicroserviceAPIClient):
    
    
    def __init__(self, base_url, auth_token, is_preview=True):
        super().__init__(base_url, auth_token)
        self.is_preview = is_preview


    def get_token(self):
        # This token is for direct AthenaClient only
        token = self._create_request(
            method='GET',
            endpoint="/token"
        ).get('token')
        return token
        
        
    def patient_check(self, firstname, lastname, dob):
        payload = {
            'firstname': firstname,
            'lastname': lastname,
            'dob': dob
        }
      
    
        response = self._create_requests(
            method='POST',
            endpoint='/patient_check',
            payload=payload,
        )

        if patient_id := response.get('patient_id'):
            print('Patient found in Athena')
            return patient_id
        print('Patient not found in Athena')
            
        
    def patient_details(self, patient_id):
        payload = {
           'patient_id': patient_id
        }
     
        response = self._create_requests(
            method='GET',
            endpoint='/patientg/patient/details',
            payload=payload,
        )
        
        return response


        
            
    



class AthenaClient(MicroserviceAPIClient):
    '''
    AthenaProxy has to be instanited first to get a token for this Athena client 
    '''
    def __init__(self, base_url, auth_token, is_preview=True):
        super().__init__(base_url, auth_token)
        self._token = auth_token
        print(self._token)
        self._auth_headers = {"Authorization": "Bearer " + auth_token}
        self.is_preview = is_preview
        
        
    def _adjust_header(self, headers):
            if not headers:
                return self._auth_headers
            else:
                headers["Authorization"] = self._auth_headers.get("Authorization")
            return headers
            
            
    def _create_request(self, method, endpoint, headers={}, payload={}, params={}, files=[], return_response=False):
        url = self.base_url + endpoint
        headers=self._adjust_header(headers)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=payload,
                params=params,
                files=files
            )
            response.raise_for_status()
            logging.info(f"{method}: {response.status_code} {endpoint}: ")
        except requests.exceptions.HTTPError as error:
            logging.error(f'{method}: {endpoint}: failed, text:: {response.text}, Error: {error}')
            return None
        if return_response:
            return response
        return response.json()
    
        
    def upload_clinical_document(self, payload):
        # Not using internal create request method, two diferent auth tokens
        try:
            file = open(payload.get('dir_path') + payload.get('file_name'), 'rb')
        except FileNotFoundError as error:
            logging.critical(error)

        files = [
            ('attachmentcontents', (payload.get('file_name'), file, 'application/pdf'))
        ]
        
        headers = {
            'Content-Type': 'multipart/form-data',
            'Content-Disposition': 'attachment; filename="' + payload.get('file_name') + '"',
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + str(self._token)
        }
        response = self._create_request(
            method="POST",
            endpoint=f"/patients/{payload.get('data').get('patient_id')}/documents/clinicaldocument",
            headers=headers,
            payload=payload.get('data'),
            files=files
        )
        
        print(response)
        if 'success' in response:
            return True 
        else:
           return False

            
            
    