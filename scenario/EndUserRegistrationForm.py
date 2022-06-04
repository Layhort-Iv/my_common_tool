
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
from utilities.SiteManagementAPI.InsertFormFunction import InsertFormFunction
from utilities.SiteManagementAPI.LayoutFuntion import LayoutFunction
from utilities.SiteManagementAPI.PageFunction import PageFunction


@scenario(name="EndUserRegistrationForm", description="Check the operation of Single Record Mail Action Function")
class EndUserRegistrationForm(Thread, testDecorator, AppFunction, DBFunction, SiteFunction, LayoutFunction, PageFunction, InsertFormFunction, SingleRecordMailActionFunction):

    @inject(user=User, option=Option)
    def __init__(self, user, option):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "End User Registration Form")
        InsertFormFunction.__init__(self, "insertForms", "insert form")
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
        with Path("request/PrivateAPI/CMS/Page/sourceSettingPage.yml").open(encoding="utf-8") as file:
            req_source_setting_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/addBlockToSourceSettingPage.yml").open(encoding="utf-8") as file:
            req_update_source_setting_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/SourceSetting.yml").open(encoding="utf-8") as file:
            req_insert_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/NoConfirmationInput.yml").open(encoding="utf-8") as file:
            req_no_confirmation_input_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/AddMailActionToForm.yml").open(encoding="utf-8") as file:
            req_add_mail_action_to_form = yaml.safe_load(file)
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

            layout_id = self.get_all_site_layouts(site_id).json().get('items')[0].get('id')
            log_print(self.SCENARIO_NAME, "Successfully get site layout")

            req_source_setting_page['view']['layoutId'] = layout_id
            page_id = self.create_page(site_id, req_source_setting_page).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a source setting page")

            req_insert_form['dbId'] = db_id
            res_insert_form = self.create_form(site_id, req_insert_form).json()
            insert_form_block_name = res_insert_form.get('blockName')
            insert_form_id = res_insert_form.get('id')
            log_print(self.SCENARIO_NAME, "Successfully create an insert form using source setting")

            self.update_form(site_id, insert_form_id, req_no_confirmation_input_form)
            log_print(self.SCENARIO_NAME, "No confirmation input form")

            req_update_source_setting_page['view']['layoutId'] = layout_id
            req_update_source_setting_page['view']['template']['content'] = f'<sp:block name=\"{insert_form_block_name}\"></sp:block>'
            self.update_page(site_id, page_id, req_update_source_setting_page)
            log_print(self.SCENARIO_NAME, "Successfully add insert form to source setting page")


            req_mail_action['dbId'] = db_id
            req_mail_action['appId'] = app_id
            req_mail_action['from']['emailFromDomainId'] = emailFromDomainId
            mail_action_id = self.create_mail_action(req_mail_action).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a single record mail action")


            req_add_mail_action_to_form['onCompletion']['handlers'][0]['ids'][0] = mail_action_id
            self.update_form(site_id, insert_form_id, req_add_mail_action_to_form).json()
            log_print(self.SCENARIO_NAME, "Successfully attach mail action to insert form")


            self.update_mail_action(mail_action_id, req_update_mail_action)
            log_print(self.SCENARIO_NAME, "Successfully activate single record mail action")






            # self.delete_app(app_id)
            # self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            # self.delete_app(app_id)
            # self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)