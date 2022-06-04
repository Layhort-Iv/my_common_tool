import json

class PageFunction():
    def __init__(self) -> None:
        pass

    def get_all_pages(self, site_id):
        res = self.user.get(f"/sites/{site_id}/pages")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all pages | {res.json()}")
        return res


    def get_page(self, site_id, page_id):
        res = self.user.get(f"/sites/{site_id}/pages/{page_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get a page | {res.json()}")
        return res


    def delete_page(self, site_id, page_id):
        res = self.user.delete(f"/sites/{site_id}/pages/{page_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete a page | {res.json()}")
        return res


    def create_page(self, site_id, req_page):
        res = self.user.post(f"/sites/{site_id}/pages", body = json.dumps(req_page))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create a page | {res.json()}")
        return res


    def update_page(self, site_id, page_id, req_page):
        res = self.user.patch(f"/sites/{site_id}/pages/{page_id}", body = json.dumps(req_page))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update a page | {res.json()}")
        return res


    def validate_page_template(self, site_id, req_page_template):
        res = self.user.post(f"/sites/{site_id}/pages/inspect", body=json.dumps(req_page_template))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to validate a page template | {res.json()}")
        return res
    

    def preview_new_page(self, site_id, req_preview_page):
        res = self.user.post(f"/sites/{site_id}/pages/preview", body=json.dumps(req_preview_page))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to preview a new page | {res.json()}")
        return res


    def preview_existing_page(self, site_id, page_id):
        res = self.user.post(f"/sites/{site_id}/pages/{page_id}/preview", body=None)
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to preview an existing page | {res.json()}")
        return res


    def preview_existing_snapshot_page(self, site_id, snapshot_id, page_id):
        res = self.user.post(f"sites/{site_id}/snapshots/{snapshot_id}/pages/{page_id}/preview")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to preview existing snapshot page | {res.json()}")
            

    def get_all_child_pages(self, site_id, page_id):
        res = self.user.get(f"/sites/{site_id}/pages/{page_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all child pages | {res.json()}")
        return res
