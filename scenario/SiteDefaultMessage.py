
from threading import Thread, current_thread
from logging import getLogger
from stdtest.display import end_test, log_print
from stdtest.User import User
from stdtest.decorator import scenario, inject
import yaml
from pathlib import Path
from datetime import datetime
from stdtest.testDecorator import testDecorator
from stdtest.csvGenerator import csvGenerator
from utilities.SiteManagementAPI.SiteFunction import SiteFunction
from utilities.SiteManagementAPI.SiteDefaultMessageFunction import SiteDefaultMessageFunction


@scenario(name="SiteDefaultMessage", description="Check the operation of Site Default Message Function")
class SiteDefaultMessage(Thread, testDecorator, SiteFunction, SiteDefaultMessageFunction):

    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Site Default Message")
        SiteDefaultMessageFunction.__init__(self)
        self.writer = csvGenerator(fileName=f'{__name__.split(".")[1]}_{str(datetime.now()).split(" ")[0]}_{(str(datetime.now()).split(" ")[1].split(".")[0]).replace(":","-")}')
        self.user = user()
        self.user.logger = getLogger(__name__)
        

    def run(self):
        with Path("request/PrivateAPI/CMS/Site/site.yml").open(encoding="utf-8") as file:
            req_site = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteDefaultMessage/defaultMessage.yml").open(encoding="utf-8") as file:
            req_default_message = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteDefaultMessage/defaultMessageUpdate.yml").open(encoding="utf-8") as file:
            req_default_message_update = yaml.safe_load(file)

        try:
            req_site['displayName'] = "Site Auto Test - Site Default Message"
            req_site['name'] = "defaultmessage"
            req_site['description'] = "Site Auto Test - Site Default Message"

            log_print(self.SCENARIO_NAME, "Check if the site has already existed")
            site_id = self.check_site(req_site)
            if site_id == None:
                log_print(self.SCENARIO_NAME, "Site does not exist")
            else:
                log_print(self.SCENARIO_NAME, "Site has already existed")
                self.delete_site(site_id)
                log_print(self.SCENARIO_NAME, "Successfully deleted the site")

            site_id = self.create_site(req_site).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create site")


            self.start_test(self.SCENARIO_NAME, "Verify if user can create a site default message")
            res_default_message = self.create_default_message(site_id, req_default_message)
            default_message_id = res_default_message.json().get('id')
            if default_message_id == None:
                self.put_testResult(res_default_message)
                raise Exception(f"Failed to create a site default message | {res_default_message.json()}")
            self.test_passed(res=res_default_message)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get all site default messages")
            res_default_message = self.get_all_default_messages(site_id)
            total_default_message = res_default_message.json().get('totalCount')
            if total_default_message == None:
                self.put_testResult(res_default_message)
                raise Exception(f"Failed to get all site default messages | {res_default_message.json()}")
            self.test_passed(res=res_default_message)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a site default message name")
            res_default_message = self.get_default_message(site_id, default_message_id)
            default_message_display_name = res_default_message.json().get('displayName')
            if default_message_display_name == None:
                self.put_testResult(res_default_message)
                raise Exception(f"Failed to get a site default message display name | {res_default_message.json()}")
            self.test_passed(res=res_default_message)


            self.start_test(self.SCENARIO_NAME, "Verify if user can update a site default message")
            expected_required_error_message = req_default_message_update['crudForm']['requiredErrorMessage']
            res_default_message = self.update_default_message(site_id, default_message_id, req_default_message_update)
            actual_required_error_message = res_default_message.json().get('crudForm').get('requiredErrorMessage')
            if actual_required_error_message != expected_required_error_message:
                self.put_testResult(res_default_message)
                raise Exception(f"EXPECTED REQUIRED ERROR MESSAGE {expected_required_error_message} BUT GOT {actual_required_error_message}| {res_default_message.json()}")
            self.test_passed(res=res_default_message)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete site default message")
            res_default_message = self.delte_default_message(site_id, default_message_id)
            self.test_passed(res=res_default_message)

            self.delete_site(site_id)


        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)