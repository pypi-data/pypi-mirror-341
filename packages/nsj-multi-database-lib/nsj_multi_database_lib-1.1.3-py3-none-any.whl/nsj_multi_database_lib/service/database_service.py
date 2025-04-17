import requests

class DatabaseValidationException(Exception):
    pass

class DatabaseUnknowException(Exception):
    pass

class DatabaseService():

    _SRE_URL = "https://api.sre.nasajon.com.br/erp/credentials"

    def get_by_tenant(self, tenant, token):

        headers = { "Authorization": token }

        body = { "tenant" : tenant }

        response = requests.post(self._SRE_URL, json=body, headers=headers, timeout=10)

        if response.status_code == 200:
            return response.json()
        elif response.status_code >= 400 and response.status_code <= 499:
            data = response.json()
            raise DatabaseValidationException(response.status_code, data["detail"] if "detail" in data else response.text)
        else:
            data = response.json()
            raise DatabaseUnknowException(data["detail"] if "detail" in data else response.text)
