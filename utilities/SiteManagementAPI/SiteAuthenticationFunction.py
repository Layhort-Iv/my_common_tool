import json

class SiteAuthenticationFunction():
    def __init__(self) -> None:
        pass

    def auth_area_login(self, site_id, auth_area_id, auth_area_login_body, header):
        res = self.user.post(f"/sites/{site_id}/authentications/{auth_area_id}/login", header=header, body = json.dumps(auth_area_login_body))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to login to authentication area | {res.json()}")
        return res


    def validate_auth_token(self, site_id, auth_area_id, req_auth_token, header):
        res = self.user.post(f"/sites/{site_id}/authentications/{auth_area_id}/status", header=header, body = json.dumps(req_auth_token))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to validate authentication area token | {res.json()}")
        return res


    def issue_one_time_url_login(self, site_id, auth_area_id, req_one_time_url_login, header):
        res = self.user.post(f"/sites/{site_id}/authentications/{auth_area_id}/oneTimeLogin", header=header, body = json.dumps(req_one_time_url_login))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to issue one-time URL for authentication area login | {res.json()}")
        return res


    def auth_area_logout(self, site_id, auth_area_id, req_auth_token, header):
        res = self.user.post(f"/sites/{site_id}/authentications/{auth_area_id}/logout", header=header, body = json.dumps(req_auth_token))
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to logout from authentication area | {res.json()}")
        return res
