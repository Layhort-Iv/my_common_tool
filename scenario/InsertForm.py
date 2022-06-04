from threading import Thread, current_thread
from logging import getLogger
from stdtest.display import log_print, start_test, end_test
from stdtest.User import User
from stdtest.decorator import scenario, inject
import yaml
from pathlib import Path
from datetime import datetime
from stdtest.csvGenerator import csvGenerator
from stdtest.testDecorator import testDecorator
from utilities.AppManagementAPI.AppFunction import AppFunction
from utilities.AppManagementAPI.DBFunction import DBFunction
from utilities.SiteManagementAPI.SiteFunction import SiteFunction
from utilities.SiteManagementAPI.LayoutFuntion import LayoutFunction
from utilities.SiteManagementAPI.PageFunction import PageFunction
from utilities.SiteManagementAPI.InsertFormFunction import InsertFormFunction
from utilities.SiteManagementAPI.AuthAreaFunction import AuthAreaFunction

@scenario(name="InsertForm", description="Check the operation of Insert Form Function")
class InsertForm(Thread, testDecorator, AppFunction, DBFunction, SiteFunction, LayoutFunction, InsertFormFunction, AuthAreaFunction, PageFunction):

    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Insert Form")
        InsertFormFunction.__init__(self, "insertForms", "insert form")
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
        with Path("request/PrivateAPI/CMS/Block/InsertForm/VisualSetting.yml").open(encoding="utf-8") as file:
            req_visual_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/SourceSetting.yml").open(encoding="utf-8") as file:
            req_source_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/SourceSettingWithAuthArea.yml").open(encoding="utf-8") as file:
            req_source_form_auth_area = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/VisualSettingUpdate.yml").open(encoding="utf-8") as file:
            req_update_visual_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/SourceSettingUpdate.yml").open(encoding="utf-8") as file:
            req_update_source_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/SourceSettingAuthUpdate.yml").open(encoding="utf-8") as file:
            req_updated_source_form_auth_area = yaml.safe_load(file)

        try:
            req_app['displayName'] = "App Auto Test - Insert Form"
            req_app['name'] = "InsertFormApp"
            req_app['description'] = "App Auto Test - Insert Form"

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
            req_site['displayName'] = "Site Auto Test - Insert Form"
            req_site['name'] = "insertform"
            req_site['description'] = "Site Auto Test - Insert Form"

            log_print(self.SCENARIO_NAME, "Check if the site has already existed")
            site_id = self.check_site(req_site)
            if site_id == None:
                log_print(self.SCENARIO_NAME, "Site does not exist")
            else:
                log_print(self.SCENARIO_NAME, "Site has already existed")
                self.delete_site(site_id)
                log_print(self.SCENARIO_NAME, "Successfully deleted the site")

            site_id = self.create_site(req_site).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a site")

            req_auth_area['dbId'] = db_id
            auth_area_id = self.create_auth_area(site_id, req_auth_area).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create an authentication area")

            
            self.start_test(self.SCENARIO_NAME, "Check if user can create an insert form using visual setting")   
            req_visual_form['dbId'] = db_id
            res_form = self.create_form(site_id, req_visual_form)
            visual_form_id = res_form.json().get('id')
            if visual_form_id == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to create an insert form using visual setting | {res_form.json()}")
            self.test_passed(res=res_form)
            

            self.start_test(self.SCENARIO_NAME, "Check if user can create an insert form using source setting")
            req_source_form['dbId'] = db_id
            res_form = self.create_form(site_id, req_source_form)
            source_form_id = res_form.json().get('id')
            if source_form_id == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to create an insert form using source setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can create an insert form with authentication area using source setting")
            req_source_form_auth_area['dbId'] = db_id
            req_source_form_auth_area['authenticationId'] = auth_area_id
            res_form = self.create_form(site_id, req_source_form_auth_area)
            source_form_auth_area_id = res_form.json().get('id')
            if source_form_auth_area_id == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to create an insert form with authentication area using source setting | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can get all insert forms")
            res_form = self.get_all_forms(site_id)
            total_forms = res_form.json().get('totalCount')
            if total_forms == 0 or total_forms == None:
                self.put_testResult(res=res_form)
                raise Exception(f"Failed to get all insert forms | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can get block name of visual setting form")
            res_form = self.get_form(site_id, visual_form_id)
            block_name = res_form.json().get('blockName')
            if block_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get block name of visual setting form | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can get block name of source setting form")
            res_form = self.get_form(site_id, source_form_id)
            block_name = res_form.json().get('blockName')
            if block_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get block name of source setting form | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can get block name of source setting form that created with authentication area")
            res_form = self.get_form(site_id, source_form_auth_area_id)
            block_name = res_form.json().get('blockName')
            if block_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get block name of source setting form that created with authentication area | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can update visual setting form")
            expected_form_name = req_update_visual_form['name']
            res_form = self.update_form(site_id, visual_form_id, req_update_visual_form)
            actual_form_name = res_form.json().get('name')
            if actual_form_name != expected_form_name or actual_form_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to update visual setting form | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can update source setting form")
            expected_form_name = req_update_source_form['name']
            res_form = self.update_form(site_id, source_form_id, req_update_source_form)
            actual_form_name = res_form.json().get('name')
            if actual_form_name != expected_form_name or actual_form_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to update source setting form | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can update source setting form with authentication area")
            expected_form_name = req_updated_source_form_auth_area['name']
            res_form = self.update_form(site_id, source_form_auth_area_id, req_updated_source_form_auth_area)
            actual_form_name = res_form.json().get('name')
            if actual_form_name != expected_form_name or actual_form_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to update source setting form with authentication area | {res_form.json()}")
            self.test_passed(res=res_form)
            

            self.start_test(self.SCENARIO_NAME, "Check if user can switch form setting from visual to source")
            res_form = self.convert_to_source(site_id, visual_form_id)
            setting_after_switch = self.get_form(site_id, visual_form_id).json().get('view').get('design')
            if setting_after_switch != "source":
                self.put_testResult(res=res_form)
                raise Exception(f"Failed to switch form setting from visual to source | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Check if user can delete visual setting form")
            res_form = self.delete_form(site_id, visual_form_id)
            self.test_passed(res=res_form)

            self.start_test(self.SCENARIO_NAME, "Check if user can delete source setting form")
            res_form = self.delete_form(site_id, source_form_id)
            self.test_passed(res=res_form)

            self.start_test(self.SCENARIO_NAME, "Check if user can delete source setting form with authentication area")
            res_form = self.delete_form(site_id, source_form_auth_area_id)
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