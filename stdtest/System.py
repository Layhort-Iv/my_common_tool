import requests
from logging import getLogger

class System:

    def __init__(self, http_host, http_port, api_key, certificate=False):
        self.http_host = http_host
        self.http_port = http_port
        self.api_key = api_key
        self.certificate = certificate
        self.header = {
            "content-type": "application/json",
            "apikey": "bff_keyauths_key"
        }
        self.logger = getLogger(__name__)
        
    def get(self, path_param, header={}, body={}):
        self.logger.debug("Sending GET {}".format(self.http_host + path_param))
        res = requests.get(
            url=self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header,
            data=body,
            verify=self.certificate
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received GET {} {}".format(res.status_code, self.http_host + path_param))
        else:
            self.logger.warning("Received GET {} {}".format(res.status_code, self.http_host + path_param))
        return res
    
    def post(self, path_param, header={}, body={}):
        self.logger.debug("Sending POST {}".format(self.http_host + path_param))
        res = requests.post(
            url=self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header,
            data=body,
            verify=self.certificate
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received POST {} {}".format(res.status_code, self.http_host + path_param))
        else:
            self.logger.warning("Received POST {} {}".format(res.status_code, self.http_host + path_param))
        return res
    
    def put(self, path_param, header={}, body={}):
        self.logger.debug("Sending PUT {}".format(self.http_host + path_param))
        res = requests.put(
            url=self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header,
            data=body,
            verify=self.certificate
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received PUT {} {}".format(res.status_code, self.http_host + path_param))
        else:
            self.logger.warning("Received PUT {} {}".format(res.status_code, self.http_host + path_param))
        return res
    
    def patch(self, path_param, header={}, body={}):
        self.logger.debug("Sending PATCH {}".format(self.http_host + path_param))
        res = requests.patch(
            url=self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header,
            data=body,
            verify=self.certificate
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received PATCH {} {}".format(res.status_code, self.http_host + path_param))
        else:
            self.logger.warning("Received PATCH {} {}".format(res.status_code, self.http_host + path_param))
        return res
    
    def delete(self, path_param, header={}, body={}):
        self.logger.debug("Sending DELETE {}".format(self.http_host + path_param))
        res = requests.delete(
            url=self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header,
            data=body,
            verify=self.certificate
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received DELETE {} {}".format(res.status_code, self.http_host + path_param))
        else:
            self.logger.warning("Received DELETE {} {}".format(res.status_code, self.http_host + path_param))
        return res
        
