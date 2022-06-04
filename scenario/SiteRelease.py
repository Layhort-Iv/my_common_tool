
from threading import Thread, current_thread
from logging import getLogger
from time import sleep
from stdtest.display import end_test, log_print, start_test, ng
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
from utilities.SiteManagementAPI.SiteReleaseFunction import SiteReleaseFunction


@scenario(name="SiteRelease", description="Check the operation of Site Management Group Function")
class SiteRelease(Thread, testDecorator, AppFunction, DBFunction, SiteFunction, LayoutFunction, PageFunction, InsertFormFunction, SiteReleaseFunction):

    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Site Release")
        SiteReleaseFunction.__init__(self)
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
        with Path("request/PrivateAPI/CMS/Page/sourceSettingPage.yml").open(encoding="utf-8") as file:
            req_source_setting_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/SourceSetting.yml").open(encoding="utf-8") as file:
            req_source_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/addBlockToSourceSettingPage.yml").open(encoding="utf-8") as file:
            req_update_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Release/release.yml").open(encoding="utf-8") as file:
            req_site_release = yaml.safe_load(file)
        
        try:
            req_app['displayName'] = "App Auto Test - Site Release"
            req_app['name'] = "SiteReleaseApp"
            req_app['description'] = "App Auto Test - Site Release"

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
            req_site['displayName'] = "Site Auto Test - Site Release"
            req_site['name'] = "siterelease"
            req_site['description'] = "Site Auto Test - Site Release"
            TIME_SEC = 30
            SLEEP_SEC = 1

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

            req_source_form['dbId'] = db_id
            res_form = self.create_form(site_id, req_source_form).json()
            regist_form_id = res_form.get('id')
            regist_block_name = res_form.get('blockName')
            log_print(self.SCENARIO_NAME, "Successfully create an insert form using source setting")


            req_update_page['view']['layoutId'] = layout_id
            req_update_page['view']['template']['content'] = f"<sp:block name=\"{regist_block_name}\"></sp:block>"
            self.update_page(site_id, page_id, req_update_page)
            log_print(self.SCENARIO_NAME, "Successfully attach registration form block to page")


            self.start_test(self.SCENARIO_NAME, "Verify if user can release a site")
            req_site_release['insertFormIds'] = [regist_form_id]
            req_site_release['layoutIds'] = [layout_id]
            req_site_release['pageIds'] = [page_id]
            res_site_release = self.release_site(site_id, req_site_release)
            release_id = res_site_release.json().get('id')
            for i in range(1, TIME_SEC):
                sleep(SLEEP_SEC)
                release_status = self.get_site_release(site_id, release_id).json().get('status')
                if release_status == "succeeded":
                    self.test_passed(res=res_site_release)
                    break
                elif release_status == "failed":
                    self.put_testResult(res_site_release)
                    raise Exception(f"Failed to release a site | {res_site_release.json()}")
                elif i > TIME_SEC:
                    self.put_testResult(res_site_release)
                    raise Exception(f"Release site timeout | {res_site_release.json()}")


            self.start_test(self.SCENARIO_NAME, "Verify if user can get all site releases")
            res_site_release = self.get_all_site_releases(site_id)
            total_site_releases = res_site_release.json().get('totalCount')
            if total_site_releases == 0 or total_site_releases == None:
                self.put_testResult(res_site_release)
                raise Exception(f"Failed to get all site releases | {res_site_release.json()}")
            self.test_passed(res=res_site_release)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a site relase")
            res_site_release = self.get_site_release(site_id, release_id)
            snap_shot_id = res_site_release.json().get('snapshotId')
            if snap_shot_id == None:
                self.put_testResult(res_site_release)
                raise Exception(f"Failed to get a site release | {res_site_release.json()}")
            self.test_passed(res=res_site_release)

            self.delete_app(app_id)
            self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_app(app_id)
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)