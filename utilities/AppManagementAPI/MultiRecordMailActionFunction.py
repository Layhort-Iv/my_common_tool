from utilities.AppManagementAPI.MailActionFunction import MailActionFunction

class MultiRecordMailActionFunction(MailActionFunction):
    
    def __init__(self, mail_action_path, mail_action_type):
        MailActionFunction.__init__(self, mail_action_path, mail_action_type)