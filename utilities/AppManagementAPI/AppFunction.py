import json

class AppFunction():
    def __init__(self) -> None:
        pass

    def check_app(self, req_app):
        res_app = AppFunction.get_all_apps(self)
        for app in res_app.json().get('items'):
            if app['displayName'] == req_app['displayName']:
                return app.get('id')
        return None

    def create_app(self, req_app):
        res = self.user.post("/apps", body=json.dumps(req_app))
        if res.status_code != 201:
            self.put_testResult(res)
            raise Exception(f"Failed to create app | {res.json()}")
        return res

    def get_all_apps(self):
        res = self.user.get("/apps")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all apps | {res.json()}")
        return res
    
    def get_app(self, app_id):
        res = self.user.get(f"/apps/{app_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get an app | {res.json()}")
        return res

    def update_app(self, app_id, req_app):
        res = self.user.patch(f"/apps/{app_id}", body=json.dumps(req_app))
        if not res.status_code == 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create an app | {res.json()}")
        return res

    def delete_app(self, app_id):
        res = self.user.delete(f"/apps/{app_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete an app | {res.json()}")
        return res
