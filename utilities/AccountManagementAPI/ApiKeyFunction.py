import json

class ApiKeyFunction():
    def __init__(self) -> None:
        pass
    
    def create_api_key(self, api_agent_id, req_api_key):
        res = self.user.post(f"/bots/{api_agent_id}/apiKeys", body = json.dumps(req_api_key))
        if res.status_code != 201:
            self.put_testResult(res)
            raise Exception(f"Failed to create an api agent key | {res.json()}")
        return res


    def update_api_key(self, api_agent_id, api_key_id, req_api_key):
        res = self.user.patch(f"/bots/{api_agent_id}/apiKeys/{api_key_id}", body = json.dumps(req_api_key))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create an api agent key | {res.json()}")
        return res
