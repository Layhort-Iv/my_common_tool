import json

class SiteApiUseGroupFunction():
    def __init__(self) -> None:
        pass

    def create_site_auth_api(self, site_id, req_memberships):
        res = self.user.post(f"/sites/{site_id}/siteApiUseGroups", body = json.dumps(req_memberships))
        if not res.status_code == 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create a site authentication api | {res.json()}")
        return res