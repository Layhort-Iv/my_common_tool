import json

class LayoutFunction():
    def __init__(self) -> None:
        pass

    def get_all_site_layouts(self, site_id):
        res = self.user.get(f"/sites/{site_id}/layouts")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get site layout | {res.json()}")
        return res


    def create_site_layout(self, site_id, req_layout):
        res = self.user.post(f"/sites/{site_id}/layouts", body=json.dumps(req_layout))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create a site layout | {res.json()}")
        return res
    

    def get_site_layout(self, site_id, layout_id):
        res = self.user.get(f"/sites/{site_id}/layouts/{layout_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get a site layout | {res.json()}")
        return res


    def update_site_layout(self, site_id, layout_id, req_layout):
        res = self.user.patch(f"/sites/{site_id}/layouts/{layout_id}", body=json.dumps(req_layout))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update a site layout | {res.json()}")
        return res


    def delte_site_layout(self, site_id, layout_id):
        res = self.user.delete(f"/sites/{site_id}/layouts/{layout_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to get a site layout | {res.json()}")
        return res