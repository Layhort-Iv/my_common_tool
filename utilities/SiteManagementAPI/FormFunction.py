import json

class FormFunction():

    def __init__(self, form_path, form_type):
        self.form_path = form_path
        self.form_type = form_type

    def create_form(self, site_id, req_form):
        res = self.user.post(f"/sites/{site_id}/{self.form_path}", body=json.dumps(req_form))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create {self.form_type} | {res.json()}")
        return res


    def get_all_forms(self, site_id):
        res = self.user.get(f"/sites/{site_id}/{self.form_path}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all {self.form_type}s | {res.json()}")
        return res


    def get_form(self, site_id, form_id):
        res = self.user.get(f"/sites/{site_id}/{self.form_path}/{form_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get {self.form_type} | {res.json()}")
        return res


    def update_form(self, site_id, form_id, req_form):
        res = self.user.patch(f"/sites/{site_id}/{self.form_path}/{form_id}", body=json.dumps(req_form))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update {self.form_type} | {res.json()}")
        return res


    def delete_form(self, site_id, form_id):
        res = self.user.delete(f"/sites/{site_id}/{self.form_path}/{form_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete {self.form_type} | {res.json()}")
        return res