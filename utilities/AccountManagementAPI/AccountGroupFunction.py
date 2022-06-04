import json

class AccountGroupFunction():
    def __init__(self) -> None:
        pass

    def check_account_group(self, req_group):
        res_account_group = self.get_all_account_groups()
        for group in res_account_group.json().get('items'):
            if group['displayName'] == req_group['displayName']:
                return group.get('id')
        return None


    def get_all_account_groups(self):
        res = self.user.get("/groups")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all account groups | {res.json()}")
        return res


    def create_account_group(self, req_group):
        res = self.user.post("/groups", body=json.dumps(req_group))
        if res.status_code != 201:
            self.put_testResult(res)
            raise Exception(f"Failed to create a account group | {res.json()}")
        return res


    def add_memberships(self, group_id, req_user):
        res = self.user.patch(f"/groups/{group_id}/memberships", body=json.dumps(req_user))
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to add user to account group | {res.json()}")
        return res


    def add_agent_memberships(self, group_id, req_agent_memberships):
        res = self.user.patch(f"/groups/{group_id}/agentMemberships", body=json.dumps(req_agent_memberships))
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to add api agent to account group | {res.json()}")
        return res


    def delete_account_group(self, group_id):
        res = self.user.delete(f"/groups/{group_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception("Failed to delete an account group")
        return res
