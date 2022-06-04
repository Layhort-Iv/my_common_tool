import json

class AuthAreaFunction():
    def __init__(self) -> None:
        pass

    def create_auth_area(self, site_id, req_auth_area):
        res = self.user.post(f"/sites/{site_id}/authentications", body = json.dumps(req_auth_area))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create an authentication area | {res.json()}")
        return res


    def delete_auth_area(self, site_id, auth_area_id):
        res = self.user.delete(f"/sites/{site_id}/authentications/{auth_area_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete an authentication area | {res.json()}")
        return res
