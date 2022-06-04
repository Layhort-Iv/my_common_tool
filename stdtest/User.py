import requests
from logging import getLogger

from requests.api import head

class User:

    def __init__(self, http_host, http_port, api_key, sys_api_key, certificate=False):
        self.http_host = http_host
        self.http_port = http_port
        self.api_key = api_key
        self.sys_api_key = sys_api_key
        self.certificate = certificate
        self.header = {
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(api_key),
            "X-Spiral-Api-Version":"1.1",
            "X-Spiral-App-Authority":"manage",
            "X-Spiral-App-Role":"_fullAccess"
        }
        self.download_header = {
            "Authorization": "Bearer {}".format(api_key),
            "X-Spiral-Api-Version":"1.1"
        }
        self.sys_header = {
            "content-type": "application/json",
            "apikey": self.sys_api_key,
            "X-Spiral-Api-Version":"1.1"
        }
        self.logger = getLogger(__name__)

    def get(self, path_param, header={}, body={}, sys_api=False):
        self.logger.debug("Sending GET {}".format(self.http_host + "/v1"+ path_param))
        res = requests.get(
            url=self.http_host + "/v1" + path_param if not sys_api else self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header if not sys_api else self.sys_header,
            data=body,
            verify=self.certificate,
            timeout = 60
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received GET {} {}".format(res.status_code, self.http_host + "/v1"+ path_param))
        else:
            self.logger.warning("Received GET {} {} With Body {}".format(res.status_code, self.http_host + "/v1"+ path_param, res._content))
        return res

    def download(self, path_param, header={}, sys_api=False):
        self.logger.debug("Sending Download {}".format(path_param))
        res = requests.get(
            url= path_param,
            headers=self.download_header,
            verify=self.certificate
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received Download {} {}".format(res.status_code, path_param))
        else:
            self.logger.warning("Received Download {} {}".format(res.status_code, path_param))
        return res

    def post(self, path_param, header={}, body={}, sys_api=False):
        self.logger.debug("Sending POST {}".format(self.http_host+ "/v1" + path_param))
        res = requests.post(
            url=self.http_host + "/v1" + path_param if not sys_api else self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header if not sys_api else self.sys_header,
            data=body,
            verify=self.certificate,
            timeout = 60
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received POST {} {}".format(res.status_code, self.http_host + "/v1"+ path_param))
        else:
            self.logger.warning("Received POST {} {}\n{}".format(res.status_code, self.http_host + "/v1" + path_param, res.json()))
        return res

    # ---edited by kashima masaya 20180918---------
    def postFile(self, path_param, file, header={}, body={}, sys_api=False):
        self.logger.debug("Sending POST {}".format(
            self.http_host + "/v1"+ path_param))
        res = requests.post(
            url=self.http_host + "/v1" + path_param if not sys_api else self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header if not sys_api else self.sys_header,
            data=body,
            files=file,
            verify=self.certificate,
            timeout = 60
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received POST {} {}".format(res.status_code, self.http_host + "/v1"+ path_param))
        else:
            self.logger.warning("Received POST {} {}".format(res.status_code, self.http_host + "/v1"+ path_param))
        return res
    # ----------------------------

    def put(self, path_param, header={}, body={}, sys_api=False):
        self.logger.debug("Sending PUT {}".format(self.http_host + "/v1"+ path_param))
        res = requests.put(
            url=self.http_host + "/v1" + path_param if not sys_api else self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header if not sys_api else self.sys_header,
            data=body,
            verify=self.certificate,
            timeout = 60
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received PUT {} {}".format(res.status_code, self.http_host + "/v1"+ path_param))
        else:
            self.logger.warning("Received PUT {} {}".format(res.status_code, self.http_host + "/v1"+ path_param))
        return res

    def patch(self, path_param, header={}, body={}, sys_api=False):
        self.logger.debug("Sending PATCH {}".format(self.http_host + "/v1"+ path_param))
        res = requests.patch(
            url=self.http_host + "/v1" + path_param if not sys_api else self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header if not sys_api else self.sys_header,
            data=body,
            verify=self.certificate,
            timeout = 60
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received PATCH {} {}".format(res.status_code, self.http_host + "/v1"+ path_param))
        else:
            self.logger.warning("Received PATCH {} {} with body {}".format(res.status_code, self.http_host + "/v1"+ path_param,res._content))
        return res

    def delete(self, path_param, header={}, body={}, sys_api=False):
        self.logger.debug("Sending DELETE {}".format(self.http_host + "/v1"+ path_param))
        res = requests.delete(
            url=self.http_host + "/v1" + path_param if not sys_api else self.http_host + "/sys/v1" + path_param,
            headers=header if header else self.header if not sys_api else self.sys_header,
            data=body,
            verify=self.certificate,
            timeout = 60
        )
        if 200 <= res.status_code < 300:
            self.logger.debug("Received DELETE {} {}".format(res.status_code, self.http_host + "/v1"+ path_param))
        else:
            self.logger.warning("Received DELETE {} {} with body: {}".format(res.status_code, self.http_host + "/v1"+ path_param, res._content))
        return res
    
    # def get_oauth(self,body={}):
    #     self.logger.debug("Sending GET {}".format(self.http_host + "/oauth2/token"))
    #     headers = {
    #         'Content-Type': 'application/x-www-form-urlencoded',
    #         "X-Spiral-Api-Version":"1.1"
    #     }
    #     res = requests.post(
    #         url=self.http_host + "/oauth2/token",
    #         headers=headers,
    #         data=body,
    #         verify=self.certificate,
    #         timeout = 10
    #     )
    #     if 200 <= res.status_code < 300:
    #         self.logger.debug("Received GET {} {}".format(res.status_code, self.http_host + "/oauth2/token"))
    #     else:
    #         self.logger.warning("Received GET {} {} With Body {}".format(res.status_code, self.http_host + "/oauth2/token", res.json().get("id")))
    #     return res