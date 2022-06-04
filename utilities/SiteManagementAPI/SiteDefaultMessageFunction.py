import json

class SiteDefaultMessageFunction():
    def __init__(self) -> None:
        pass

    def get_all_default_messages(self, site_id):
        res = self.user.get(f"/sites/{site_id}/defaultMessages")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all site default messages | {res.json()}")
        return res


    def create_default_message(self, site_id, req_default_message):
        res = self.user.post(f"/sites/{site_id}/defaultMessages", body=json.dumps(req_default_message))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create a site default message | {res.json()}")
        return res
    

    def get_default_message(self, site_id, default_message_id):
        res = self.user.get(f"/sites/{site_id}/defaultMessages/{default_message_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get a site default message | {res.json()}")
        return res


    def update_default_message(self, site_id, default_message_id, req_default_message):
        res = self.user.patch(f"/sites/{site_id}/defaultMessages/{default_message_id}", body=json.dumps(req_default_message))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update a site default message | {res.json()}")
        return res


    def delte_default_message(self, site_id, default_message_id):
        res = self.user.delete(f"/sites/{site_id}/defaultMessages/{default_message_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete a site default message | {res.json()}")
        return res