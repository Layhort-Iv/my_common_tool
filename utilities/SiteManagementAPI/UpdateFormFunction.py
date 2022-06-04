from utilities.SiteManagementAPI.FormFunction import FormFunction

class UpdateFormFunction(FormFunction):
    def __init__(self, form_path, form_type):
        FormFunction.__init__(self, form_path, form_type)