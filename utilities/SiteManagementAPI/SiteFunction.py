import json

class SiteFunction():
    def __init__(self) -> None:
        pass

    def get_all_sites(self):
        res = self.user.get("/sites")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get all sites | {res.json()}")
        return res


    def sort(self, field, order):
        res = self.user.get(f"/sites/?sort={field}:{order}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to sort a site | {res.json()}")
        return res
            

    def validate_sort_result(self, res, field, order):
        sort_res = []
        for item in res.json().get('items'):
            sort_res.append(item.get(field))
        if order == "asc":
            if field == "id":
                return sort_res == sorted(sort_res, key=int)
            else:
                return sort_res == sorted(sort_res)
        else:
            if field == "id":
                return sort_res == sorted(sort_res, key=int, reverse=True)
            else:
                return sort_res == sorted(sort_res, reverse=True)
    

    def offset(self, offset):
        res = self.user.get(f"/sites?offset={offset}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get offset | {res.json()}")
        print(res.json())


    def get_site_limit(self, limit):
        res = self.user.get(f"/sites?limit={limit}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get site limit | {res.json()}")
        return res


    def get_site(self, site_id):
        res = self.user.get(f"/sites/{site_id}")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get a site | {res.json()}")
        return res


    def enable_usage(self, site_id):
        res = self.user.get(f"/sites/{site_id}?enableUsage=True")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to enable site usage | {res.json()}")
        return res


    def delete_site(self, site_id):
        res = self.user.delete(f"/sites/{site_id}")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to delete site | {res.json()}")
        return res


    def create_site(self, req_site):
        res = self.user.post("/sites", body=json.dumps(req_site))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to create site | {res.json()}")
        return res


    def update_site(self, site_id, req_site):
        res = self.user.patch(f"/sites/{site_id}", body = json.dumps(req_site), sys_api = False)
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update site | {res.json()}")
        return res


    def check_site(self, req_site):
        res_site = self.get_all_sites()
        for site in res_site.json().get('items'):
            if site['displayName'] == req_site['displayName']:
                return site.get('id')
        return None


    def get_robots_txt(self, site_id):
        res = self.user.get(f"/sites/{site_id}/robotstxt")
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to get robots.txt | {res.json()}")
        return res


    def update_robots_txt(self, site_id, req_robots_txt):
        res = self.user.put(f"/sites/{site_id}/robotstxt", body = json.dumps(req_robots_txt))
        if res.status_code != 200:
            self.put_testResult(res)
            raise Exception(f"Failed to update robots.txt | {res.json()}")
        return res
