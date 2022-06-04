from threading import Thread, current_thread
from logging import getLogger
from stdtest.display import end_test, log_print, start_test
from stdtest.User import User
from stdtest.decorator import scenario, inject
import yaml
from pathlib import Path
from datetime import datetime
from stdtest.testDecorator import testDecorator
from stdtest.csvGenerator import csvGenerator
from utilities.AppManagementAPI.AppFunction import AppFunction
from utilities.AppManagementAPI.DBFunction import DBFunction
from utilities.SiteManagementAPI.SiteFunction import SiteFunction
from utilities.SiteManagementAPI.AuthAreaFunction import AuthAreaFunction
from utilities.SiteManagementAPI.RecordScopeFunction import RecordScopeFunction
from utilities.SiteManagementAPI.FreeContentFormFunction import FreeContentFormFunction


@scenario(name="FreeContentForm", description="Check the operation of Free Content Form Function")
class FreeContentForm(Thread, testDecorator, AppFunction, DBFunction, SiteFunction, AuthAreaFunction, RecordScopeFunction, FreeContentFormFunction):

    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Free Content Form")
        FreeContentFormFunction.__init__(self, "freeContents", "free content form")
        self.writer = csvGenerator(fileName=f'{__name__.split(".")[1]}_{str(datetime.now()).split(" ")[0]}_{(str(datetime.now()).split(" ")[1].split(".")[0]).replace(":","-")}')
        self.user = user()
        self.user.logger = getLogger(__name__)

    def run(self):
        start_test(self.SCENARIO_NAME, "This process can take some time (up to 30 seconds)")
        with Path("request/PrivateAPI/AppManagement/App/app.yml").open(encoding="utf-8") as file:
            req_app = yaml.safe_load(file)
        with Path("request/PrivateAPI/AppManagement/DB/db.yml").open(encoding="utf-8") as file:
            req_db = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Site/site.yml").open(encoding="utf-8") as file:
            req_site = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/AuthArea/authArea.yml").open(encoding="utf-8") as file:
            req_auth_area = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/RecordScope/scope.yml").open(encoding="utf-8") as file:
            req_record_scope = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/FreeContentForm/VisualSetting.yml").open(encoding="utf-8") as file:
            req_form_1 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/FreeContentForm/SourceSetting.yml").open(encoding="utf-8") as file:
            req_form_2 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/FreeContentForm/VisualSettingAuthArea.yml").open(encoding="utf-8") as file:
            req_form_3 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/FreeContentForm/SourceSettingAuthArea.yml").open(encoding="utf-8") as file:
            req_form_4 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/FreeContentForm/VisualSettingUpdate.yml").open(encoding="utf-8") as file:
            req_update_form_1 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/FreeContentForm/SourceSettingUpdate.yml").open(encoding="utf-8") as file:
            req_update_form_2 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/FreeContentForm/VisualAuthAreaUpdate.yml").open(encoding="utf-8") as file:
            req_update_form_3 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/FreeContentForm/SourceAuthAreaUpdate.yml").open(encoding="utf-8") as file:
            req_update_form_4 = yaml.safe_load(file)

        try:
            req_app['displayName'] = "App Auto Test - Free Content Form"
            req_app['name'] = "FreeContentFormApp"
            req_app['description'] = "App Auto Test - Free Content Form"

            log_print(self.SCENARIO_NAME, "Check if the app has already existed")
            app_id = self.check_app(req_app)
            if app_id == None:
                log_print(self.SCENARIO_NAME, "App does not exist")          
            else:
                log_print(self.SCENARIO_NAME, "App has already existed")
                self.delete_app(app_id)
                log_print(self.SCENARIO_NAME, "Successfully delete the app")
                
            app_id = self.create_app(req_app).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create an app")
            db_id = self.create_db(app_id, req_db).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a db")

        except Exception as e:
            if app_id == None:
                return
            self.delete_app(app_id)

        try:
            req_site['displayName'] = "Site Auto Test - Free Content Form"
            req_site['name'] = "freecontentform"
            req_site['description'] = "Site Auto Test - Free Content Form"

            log_print(self.SCENARIO_NAME, "Check if the site has already existed")
            site_id = self.check_site(req_site)
            if site_id == None:
                log_print(self.SCENARIO_NAME, "Site does not exist")
            else:
                log_print(self.SCENARIO_NAME, "Site has already existed")
                self.delete_site(site_id)
                log_print(self.SCENARIO_NAME, "Successfully delete the site")

            site_id = self.create_site(req_site).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a site")

            req_auth_area['dbId'] = db_id
            auth_area_id = self.create_auth_area(site_id, req_auth_area).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create an authentication area")

            req_record_scope['dbId'] = db_id
            self.register_record_scope(site_id, app_id, req_record_scope).json()
            log_print(self.SCENARIO_NAME, "Successfully create a record public scope")


            self.start_test(self.SCENARIO_NAME, "Verify if user can create a free content form using visual setting")
            res_form = self.create_form(site_id, req_form_1)
            form1_id = res_form.json().get('id')
            if form1_id == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to create a free content form using visual setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can create a free content form using source setting")
            res_form = self.create_form(site_id, req_form_2)
            form2_id = res_form.json().get('id')
            if form2_id == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to create a free content form using source setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can create a free content form with authentication area using visual setting")
            req_form_3['authenticationId'] = auth_area_id
            res_form = self.create_form(site_id, req_form_3)
            form3_id = res_form.json().get('id')
            if form3_id == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to create a free content form with authentication area using visual setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can create a free content form with authentication area using source setting")
            req_form_4['authenticationId'] = auth_area_id
            res_form = self.create_form(site_id, req_form_4)
            form4_id = res_form.json().get('id')
            if form4_id == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to create a free content form with authentication area using source setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get all free content forms")
            res_form = self.get_all_forms(site_id)
            total_forms = res_form.json().get('totalCount')
            if total_forms == 0 or total_forms == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get all free content forms | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a block name of free content form that's using visual setting")
            res_form = self.get_form(site_id, form1_id)
            block_name = res_form.json().get('blockName')
            if block_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get a block name of free content form that's using visual setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a block name of free content form that's using source setting")
            res_form = self.get_form(site_id, form2_id)
            block_name = res_form.json().get('blockName')
            if block_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get a block name of free content form that's using source setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a block name of free content form with authentication area that's using visual setting")
            res_form = self.get_form(site_id, form3_id)
            block_name = res_form.json().get('blockName')
            if block_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get a block name of free content form with authentication area that's using visual setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a block name of free content form with authentication area that's using source setting")
            res_form = self.get_form(site_id, form4_id)
            block_name = res_form.json().get('blockName')
            if block_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get a block name of free content form with authentication area that's using source setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can update a free content form that's using visual setting")
            expected_form_name = req_update_form_1['name']
            res_form = self.update_form(site_id, form1_id, req_update_form_1)
            actual_form_name = res_form.json().get('name')
            if actual_form_name == None or actual_form_name != expected_form_name:
                self.put_testResult(res_form)
                raise Exception(f"Failed to update a free content form that's using visual setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can update a free content form that's using source setting")
            expected_form_name = req_update_form_2['name']
            res_form = self.update_form(site_id, form2_id, req_update_form_2)
            actual_form_name = res_form.json().get('name')
            if actual_form_name == None or actual_form_name != expected_form_name:
                self.put_testResult(res_form)
                raise Exception(f"Failed to update a free content form that's using source setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can update a free content form with authentication area that's using visual setting")
            expected_form_name = req_update_form_3['name']
            res_form = self.update_form(site_id, form3_id, req_update_form_3)
            actual_form_name = res_form.json().get('name')
            if actual_form_name == None or actual_form_name != expected_form_name:
                self.put_testResult(res_form)
                raise Exception(f"Failed to update a free content form with authentication area that's using visual setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can update a free content form with authentication area that's using source setting")
            expected_form_name = req_update_form_4['name']
            res_form = self.update_form(site_id, form4_id, req_update_form_4)
            actual_form_name = res_form.json().get('name')
            if actual_form_name == None or actual_form_name != expected_form_name:
                self.put_testResult(res_form)
                raise Exception(f"Failed to update a free content form with authentication area that's using source setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete free content form that's using visual setting")
            res_form = self.delete_form(site_id, form1_id)
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete free content form that's using source setting")
            res_form = self.delete_form(site_id, form2_id)
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete free content form with authentication area that's using visual setting")
            res_form = self.delete_form(site_id, form3_id)
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete free content form with authentication area that's using source setting")
            res_form = self.delete_form(site_id, form4_id)
            self.test_passed(res=res_form)
            

            self.delete_app(app_id)
            self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_app(app_id)
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)