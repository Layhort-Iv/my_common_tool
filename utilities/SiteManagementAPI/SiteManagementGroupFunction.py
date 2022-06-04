import json

class SiteManagementGroupFunction():
    def __init__(self) -> None:
        pass

    def get_all_site_management_groups(self, site_id):
        res = self.user.get(f"/sites/{site_id}/manageGroups")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all site management groups | {res.json()}")
        return res


    def create_site_management_group(self, site_id, req_management_group):
        res = self.user.post(f"/sites/{site_id}/manageGroups", body=json.dumps(req_management_group))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create a site management group | {res.json()}")
        return res
    

    def get_site_management_group(self, site_id, management_group_id):
        res = self.user.get(f"/sites/{site_id}/manageGroups/{management_group_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get a site management group | {res.json()}")
        return res


    def update_site_management_group(self, site_id, management_group_id, req_management_group):
        res = self.user.patch(f"/sites/{site_id}/manageGroups/{management_group_id}", body=json.dumps(req_management_group))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update a site management group | {res.json()}")
        return res


    def delete_site_management_group(self, site_id, management_group_id):
        res = self.user.delete(f"/sites/{site_id}/manageGroups/{management_group_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete a site management group | {res.json()}")
        return res