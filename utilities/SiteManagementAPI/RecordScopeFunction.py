import json

class RecordScopeFunction():
    def __init__(self) -> None:
        pass

    def register_record_scope(self, site_id, app_id, req_scope):
        res = self.user.post(f"/sites/{site_id}/recordScope/{app_id}", body=json.dumps(req_scope))
        if res.status_code != 200:
            raise Exception(f"Failed to register record scope | {res.json()}")
        return res