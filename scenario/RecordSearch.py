from threading import Thread, current_thread
from logging import getLogger
from stdtest.display import check, end_test, log_print, ok, ng, start_test
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
from utilities.SiteManagementAPI.LayoutFuntion import LayoutFunction
from utilities.SiteManagementAPI.PageFunction import PageFunction
from utilities.SiteManagementAPI.RecordScopeFunction import RecordScopeFunction
from utilities.SiteManagementAPI.RecordListFormFunction import RecordListFormFunction
from utilities.SiteManagementAPI.RecordSearchFormFunction import RecordSearchFormFunction


@scenario(name="RecordSearch", description="Check the operation of Record Search Function")
class RecordSearch(Thread, testDecorator, AppFunction, DBFunction, SiteFunction, LayoutFunction, PageFunction, RecordScopeFunction, RecordListFormFunction, RecordSearchFormFunction):

    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Record Search Form")
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
        with Path("request/PrivateAPI/CMS/Page/sourceSettingPage.yml").open(encoding="utf-8") as file:
            req_source_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/RecordScope/scope.yml").open(encoding="utf-8") as file:
            req_record_scope = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/RecordList/RecordListDescending.yml").open(encoding="utf-8") as file:
            req_record_list = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/RecordSearch/RecordListToPage.yml").open(encoding="utf-8") as file:
            req_record_list_to_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/RecordSearch/RecordSearch.yml").open(encoding="utf-8") as file:
            req_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/RecordSearch/RecordSearchUpdate.yml").open(encoding="utf-8") as file:
            req_update_form = yaml.safe_load(file)


        try:
            req_app['displayName'] = "App Auto Test - Record Search Form"
            req_app['name'] = "RecordSearchApp"
            req_app['description'] = "App Auto Test - Record Search Form"

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
            req_site['displayName'] = "Site Auto Test - Record Search Form"
            req_site['name'] = "recordsearchform"
            req_site['description'] = "Site Auto Test - Record Search Form"

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

            req_source_page['view']['layoutId'] = layout_id
            page_id = self.create_page(site_id, req_source_page).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a source setting page")

            req_record_scope['dbId'] = db_id
            self.register_record_scope(site_id, app_id, req_record_scope).json()
            log_print(self.SCENARIO_NAME, "Successfully register record scope")

            RecordListFormFunction.__init__(self, "recordLists", "record list form")
            req_record_list['dbId'] = db_id
            record_list = self.create_form(site_id, req_record_list)
            record_list_id = record_list.json().get('id')
            block_name = record_list.json().get('blockName')
            log_print(self.SCENARIO_NAME, "Successfully create a record list in descending order")
            
            req_record_list_to_page['view']['layoutId'] = layout_id
            req_record_list_to_page['view']['template']['content'] = f'<sp:block name="{block_name}"></sp:block>'
            self.update_page(site_id, page_id, req_record_list_to_page).json()
            log_print(self.SCENARIO_NAME, "Successfully add record list to page")


            RecordSearchFormFunction.__init__(self, "recordSearchs", "record search form")
            self.start_test(self.SCENARIO_NAME, "Verify if user can create a record search form")
            req_form['dbId'] = db_id
            req_form['recordListId'] = record_list_id
            req_form['pageId'] = page_id
            res_form = self.create_form(site_id, req_form)
            form_id = res_form.json().get('id')
            if form_id == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to create record search form | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get all record search forms")
            res_form = self.get_all_forms(site_id)
            total_forms = res_form.json().get('totalCount')
            if total_forms == 0 or total_forms == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get all record search forms | {res_form.json()}")
            self.test_passed(res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get block name of record search form")
            res_form = self.get_form(site_id, form_id)
            block_name = res_form.json().get('blockName')
            if block_name == None:
                self.put_testResult(res_form)
                raise Exception(f"Failed to get block name of record search form | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can update a record search form")
            expected_form_name = req_update_form['name']
            res_form = self.update_form(site_id, form_id, req_update_form)
            actual_form_name = res_form.json().get('name')
            if actual_form_name == None or actual_form_name != expected_form_name:
                self.put_testResult(res_form)
                raise Exception(f"Failed to update a record search form | {res_form.json()}")
            self.test_passed(res=res_form)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete a record search form")
            res_form = self.delete_form(site_id, form_id)
            self.test_passed(res_form)


            self.delete_app(app_id)
            self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_app(app_id)
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)