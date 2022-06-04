import json

class ReleaseFunction():
    def __init__(self) -> None:
        pass

    def get_all_site_releases(self, site_id):
        res = self.user.get(f"/sites/{site_id}/releases")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all site releases | {res.json()}")
        return res


    def release_site(self, site_id, req_release):
        res = self.user.post(f"/sites/{site_id}/releases", body=json.dumps(req_release))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to release a site | {res.json()}")
        return res


    def get_site_release(self, site_id, release_id):
        res = self.user.get(f"/sites/{site_id}/releases/{release_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get a site release | {res.json()}")
        return res