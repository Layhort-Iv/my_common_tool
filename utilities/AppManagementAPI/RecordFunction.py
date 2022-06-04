import json
from stdtest.testDecorator import testDecorator

class RecordFunction(testDecorator):
    def __init__(self, SCENARIO_NAME):
        super().__init__(SCENARIO_NAME)

    def insert_record(self, app_id, db_id, req_record):
        res = self.user.post(f"/apps/{app_id}/dbs/{db_id}/records", body=json.dumps(req_record))
        if res.status_code != 201:
            self.put_testResult(res)
            raise Exception(f"Failed to insert record | {res.json()}")
        return res
