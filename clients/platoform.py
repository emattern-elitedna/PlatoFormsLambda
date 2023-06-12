import requests
import logging

class PlatoFormsClient:
    
    def __init__(self, token):
        self._token = token
        self.headers = {
            'Authorization': f'token {self._token}'
        }
        
        
    def download_pdf(self, sub_id, pdf_id, file_name, path):
        url = f"https://api.platoforms.com/v4/download/submission/pdf/{sub_id}/{pdf_id}/"
        payload={}
        try:
            response = requests.request("GET", url, headers=self.headers, data=payload)
            response.raise_for_status()
            with open(path + file_name, 'wb') as file:
                file.write(response.content)
            return True
        except requests.exceptions.HTTPError as error:
            logging.error(f"Failed to download PDF. ERROR: {error}. Text: {response.text}")
            return False


