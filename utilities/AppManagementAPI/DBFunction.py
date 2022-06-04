import json

class DBFunction():
    def __init__(self) -> None:
        pass

    def create_db(self, app_id, req_db):
        res = self.user.post(f"/apps/{app_id}/dbs", body=json.dumps(req_db))
        if res.status_code != 201:
            self.put_testResult(res)
            raise Exception(f"Failed to create DB | {res.json()}")
        return res

    def get_all_dbs(self, app_id):
        res = self.user.get(f"/apps/{app_id}/dbs")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all dbs | {res.json()}")
        return res

    def get_db(self, app_id, db_id):
        res = self.user.get(f"/apps/{app_id}/dbs/{db_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get a db | {res.json()}")
        return res

    def update_db(self, app_id, db_id, req_db):
        res = self.user.patch(f"/apps/{app_id}/dbs/{db_id}", body=json.dumps(req_db))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update a db | {res.json()}")

    def delete_db(self, app_id, db_id):
        res = self.user.delete(f"/apps/{app_id}/dbs/{db_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception("Failed to delete db | {res.json()}")
        return res