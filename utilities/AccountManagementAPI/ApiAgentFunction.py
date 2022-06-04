import json

class ApiAgentFunction():
    def __init__(self) -> None:
        pass

    def check_api_agent(self, req_api_agent):
        res_api_agent = self.get_all_api_agents()
        for agent in res_api_agent.json().get('items'):
            if agent['displayName'] == req_api_agent['displayName']:
                return agent.get('id')
        return None


    def create_api_agent(self, req_api_agent):
        res = self.user.post("/bots", body = json.dumps(req_api_agent))
        if res.status_code != 201:
            self.put_testResult(res)
            raise Exception(f"Failed to create an api agent | {res.json()}")
        return res
        

    def get_all_api_agents(self):
        res = self.user.get("/bots")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all api agents | {res.json()}")
        return res


    def delete_api_agent(self, api_agent_id):
        res = self.user.delete("/bots/{}".format(api_agent_id))
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete an api agent | {res.json()}")
        return res
