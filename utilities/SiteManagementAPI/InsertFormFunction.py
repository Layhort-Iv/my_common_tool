from utilities.SiteManagementAPI.FormFunction import FormFunction

class InsertFormFunction(FormFunction):

    def __init__(self, form_path, form_type):
        FormFunction.__init__(self, form_path, form_type)

    def convert_to_source(self, site_id, form_id):
        res = self.user.post(f"/sites/{site_id}/insertForms/{form_id}/convert")
        if res.status_code != 204:
            self.put_testResult(res)
            raise Exception(f"Failed to convert insert form from virtual to source setting | {res.json()}")
        return res