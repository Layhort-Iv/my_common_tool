
from threading import Thread, current_thread
from logging import getLogger
from stdtest.display import end_test, log_print, start_test
from stdtest.User import User
from stdtest.decorator import scenario, inject
import yaml
from pathlib import Path
from datetime import datetime
from stdtest.Option import Option
from stdtest.csvGenerator import csvGenerator
from stdtest.testDecorator import testDecorator
from utilities.AppManagementAPI.AppFunction import AppFunction
from utilities.AppManagementAPI.DBFunction import DBFunction
from utilities.AppManagementAPI.SingleRecordMailActionFunction import SingleRecordMailActionFunction
from utilities.SiteManagementAPI.SiteFunction import SiteFunction


@scenario(name="SingleRecordMailAction", description="Check the operation of Single Record Mail Action Function")
class SingleRecordMailAction(Thread, testDecorator, AppFunction, DBFunction, SiteFunction, SingleRecordMailActionFunction):

    @inject(user=User, option=Option)
    def __init__(self, user, option):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Single Record Mail Action")
        SingleRecordMailActionFunction.__init__(self, "singleRecordMailActions", "single record mail action")
        self.writer = csvGenerator(fileName=f'{__name__.split(".")[1]}_{str(datetime.now()).split(" ")[0]}_{(str(datetime.now()).split(" ")[1].split(".")[0]).replace(":","-")}')
        self.user = user()
        self.option = option()
        self.user.logger = getLogger(__name__)
        

    def run(self):
        start_test(self.SCENARIO_NAME, "This process can take some time (up to 30 seconds)")
        with Path("request/PrivateAPI/AppManagement/App/app.yml").open(encoding="utf-8") as file:
            req_app = yaml.safe_load(file)
        with Path("request/PrivateAPI/AppManagement/DB/db.yml").open(encoding="utf-8") as file:
            req_db = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Site/site.yml").open(encoding="utf-8") as file:
            req_site = yaml.safe_load(file)
        with Path("request/PrivateAPI/AppManagement/MailAction/SingleRecordMailAction.yml").open(encoding="utf-8") as file:
            req_mail_action = yaml.safe_load(file)
        with Path("request/PrivateAPI/AppManagement/MailAction/SingleRecordMailActionUpdate.yml").open(encoding="utf-8") as file:
            req_update_mail_action = yaml.safe_load(file)

        
        try:
            req_app['displayName'] = "App Auto Test - Single Record Mail Action"
            req_app['name'] = "SingleRecordMailActionApp"
            req_app['description'] = "App Auto Test - Single Record Mail Action"

            log_print(self.SCENARIO_NAME, "Check if the app has already existed")
            app_id = self.check_app(req_app)
            if app_id == None:
                log_print(self.SCENARIO_NAME, "App does not exist")          
            else:
                log_print(self.SCENARIO_NAME, "App has already existed")
                self.delete_app(app_id)
                log_print(self.SCENARIO_NAME, "Successfully deleted the app")
                
            app_id = self.create_app(req_app).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create an app")
            db_id = self.create_db(app_id, req_db).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a db")

        except Exception as e:
            if app_id == None:
                return
            self.delete_app(app_id)

        try:
            req_site['displayName'] = "Site Auto Test - Single Record Mail Action"
            req_site['name'] = "singlerecord"
            req_site['description'] = "Site Auto Test - Single Record Mail Action"
            emailFromDomainId = self.option.mailDomainId

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


            self.start_test(self.SCENARIO_NAME, "Verify if user can create a single record mail action")
            req_mail_action['dbId'] = db_id
            req_mail_action['appId'] = app_id
            req_mail_action['from']['emailFromDomainId'] = emailFromDomainId
            res_mail_action = self.create_mail_action(req_mail_action)
            mail_action_id = res_mail_action.json().get('id')
            if mail_action_id == None:
                self.put_testResult(res_mail_action)
                raise Exception(f"Failed to create a single record mail action | {res_mail_action.json()}")
            self.test_passed(res=res_mail_action)

            
            self.start_test(self.SCENARIO_NAME, "Verify if user can get all single record mail actions")
            res_mail_action = self.get_all_mail_actions(query_params=app_id)
            total_mail_actions = res_mail_action.json().get('totalCount')
            if total_mail_actions == 0 or total_mail_actions == None:
                self.put_testResult(res_mail_action)
                raise Exception(f"Failed to get all single record mail actions | {res_mail_action.json()}")
            self.test_passed(res=res_mail_action)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a single record mail action")
            res_mail_action = self.get_mail_action(mail_action_id)
            mail_action_name = res_mail_action.json().get('name')
            if mail_action_name == None:
                self.put_testResult(res_mail_action)
                raise Exception(f"Failed to get a single record mail action | {res_mail_action.json()}")
            self.test_passed(res=res_mail_action)


            self.start_test(self.SCENARIO_NAME, "Verify if user can activate a single record mail action")
            expected_mail_action_status = req_update_mail_action['status']
            res_mail_action = self.update_mail_action(mail_action_id, req_update_mail_action)
            actual_mail_action_status = res_mail_action.json().get('status')
            if actual_mail_action_status == None or actual_mail_action_status != expected_mail_action_status:
                self.put_testResult(res_mail_action)
                raise Exception(f"Failed to activate single record mail action | {res_mail_action.json()}")
            self.test_passed(res=res_mail_action)


            self.start_test(self.SCENARIO_NAME, "Verify if user can deactivate a single record mail action")
            req_update_mail_action['status'] = "setting"
            expected_mail_action_status = req_update_mail_action['status']
            res_mail_action = self.update_mail_action(mail_action_id, req_update_mail_action)
            actual_mail_action_status = res_mail_action.json().get('status')
            if actual_mail_action_status == None or actual_mail_action_status != expected_mail_action_status:
                self.put_testResult(res_mail_action)
                raise Exception(f"Failed to deactivate single record mail action | {res_mail_action.json()}")
            self.test_passed(res=res_mail_action)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete a single record mail action")
            res_mail_action = self.delete_mail_action(mail_action_id)
            self.test_passed(res=res_mail_action)


            self.delete_app(app_id)
            self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_app(app_id)
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)