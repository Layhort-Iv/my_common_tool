import json

class MailActionFunction():

    def __init__(self, mail_action_path, mail_action_type):
        self.mail_action_path = mail_action_path
        self.mail_action_type = mail_action_type

    def create_mail_action(self, req_mail_action):
        res = self.user.post(f"/{self.mail_action_path}", body=json.dumps(req_mail_action))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create {self.mail_action_type} | {res.json()}")
        return res

    def get_all_mail_actions(self, query_params):
        res = self.user.get(f"/{self.mail_action_path}?apps={query_params}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all {self.mail_action_type} | {res.json()}")
        return res


    def get_mail_action(self, mail_action_id):
        res = self.user.get(f"/{self.mail_action_path}/{mail_action_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get a {self.mail_action_type} | {res.json()}")
        return res


    def update_mail_action(self, mail_action_id, req_update_mail_action):
        res = self.user.patch(f"/{self.mail_action_path}/{mail_action_id}", body=json.dumps(req_update_mail_action))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update a {self.mail_action_type} | {res.json()}")
        return res

    
    def delete_mail_action(self, mail_action_id):
        res = self.user.delete(f"/{self.mail_action_path}/{mail_action_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete a {self.mail_action_type} | {res.json()}")
        return res