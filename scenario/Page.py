from threading import Thread, current_thread
from logging import getLogger
from stdtest.display import end_test, log_print, start_test
from stdtest.User import User
from stdtest.decorator import scenario, inject
import yaml
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from stdtest.testDecorator import testDecorator
from stdtest.csvGenerator import csvGenerator
from utilities.SiteManagementAPI.SiteFunction import SiteFunction
from utilities.SiteManagementAPI.PageFunction import PageFunction
from utilities.SiteManagementAPI.LayoutFuntion import LayoutFunction
from utilities.AppManagementAPI.AppFunction import AppFunction
from utilities.AppManagementAPI.DBFunction import DBFunction
from utilities.SiteManagementAPI.ReleaseFunction import ReleaseFunction
from utilities.SiteManagementAPI.InsertFormFunction import InsertFormFunction


@scenario(name="Page", description="Check the operation of Page Function")
class Page(Thread, testDecorator, SiteFunction, PageFunction, LayoutFunction, AppFunction, DBFunction, InsertFormFunction, ReleaseFunction):
    
    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Page")
        PageFunction.__init__(self)
        InsertFormFunction.__init__(self, "insertForms", "insert form")
        self.writer = csvGenerator(fileName=f'{__name__.split(".")[1]}_{str(datetime.now()).split(" ")[0]}_{(str(datetime.now()).split(" ")[1].split(".")[0]).replace(":","-")}')
        self.user = user()
        self.user.logger = getLogger(__name__)

    def run(self):
        start_test(self.SCENARIO_NAME, "This process can take some time (up to 30 seconds)")
        with Path("request/PrivateAPI/CMS/Site/site.yml").open(encoding="utf-8") as file:
            req_site = yaml.safe_load(file)
        with Path("request/PrivateAPI/AppManagement/App/app.yml").open(encoding="utf-8") as file:
            req_app = yaml.safe_load(file)
        with Path("request/PrivateAPI/AppManagement/DB/db.yml").open(encoding="utf-8") as file:
            req_db = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Block/InsertForm/FormForPage.yml").open(encoding="utf-8") as file:
            req_insert_form = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/visualPageTemplate.yml").open(encoding="utf-8") as file:
            req_visual_template = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/sourcePageTemplate.yml").open(encoding="utf-8") as file:
            req_source_template = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/visualSettingPage.yml").open(encoding="utf-8") as file:
            req_visual_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/sourceSettingPage.yml").open(encoding="utf-8") as file:
            req_source_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/visualSettingPageUpdate.yml").open(encoding="utf-8") as file:
            req_update_visual_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/sourceSettingPageUpdate.yml").open(encoding="utf-8") as file:
            req_update_source_page = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Page/childPage.yml").open(encoding="utf-8") as file:
            req_child_page = yaml.safe_load(file)

        try:
            req_app['displayName'] = "App Auto Test - Page"
            req_app['name'] = "PageApp"
            req_app['description'] = "App Auto Test - Page"

            log_print(self.SCENARIO_NAME, "Check if the app has already existed")
            app_id = self.check_app(req_app)
            if app_id == None:
                log_print(self.SCENARIO_NAME, "App does not exist")          
            else:
                log_print(self.SCENARIO_NAME, "App has already existed")
                self.delete_app(app_id)
                log_print(self.SCENARIO_NAME, "Successfully deleted the app")
                
            app_id = self.create_app(req_app).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create an app.")
            db_id = self.create_db(app_id, req_db).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a db.")

        except Exception as e:
            if app_id == None or db_id == None:
                return
            self.delete_app(app_id)

        try:
            req_site['displayName'] = "Site Auto Test - Page"
            req_site['name'] = "page"
            req_site['description'] = "Site Auto Test - Page"
            page_ids = []

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

            req_insert_form['dbId'] = db_id
            block_name = self.create_form(site_id, req_insert_form).json().get('blockName')
            log_print(self.SCENARIO_NAME, "Succssfully create an insert form")


            self.start_test(self.SCENARIO_NAME, "Check if we can create visual setting page")
            req_visual_page['view']['layoutId'] = layout_id
            res_page = self.create_page(site_id, req_visual_page)
            visual_page_id = res_page.json().get('id')
            if visual_page_id == None:
                self.put_testResult(res_page)
                raise Exception(f"Visual page ID is {visual_page_id} | {res_page.json()}")
            page_ids.append(visual_page_id)
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Check if we can create source setting page")
            req_source_page['view']['layoutId'] = layout_id
            res_page = self.create_page(site_id, req_source_page)
            source_page_id = res_page.json().get('id')
            if source_page_id == None:
                self.put_testResult(res_page)
                raise Exception(f"Source page ID is {source_page_id} | {res_page.json()}")
            page_ids.append(source_page_id)
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if a visual page template is valid")
            req_visual_template["payload"]["view"]["layoutId"] = layout_id
            req_visual_template["payload"]["view"]["template"]["blockNames"] = [f"{block_name}"]
            res_page = self.validate_page_template(site_id, req_visual_template)
            metadata_code = res_page.json().get('metadata').get('code')
            content_code = res_page.json().get('content').get('code')
            if metadata_code != 'ValidTemplate' or metadata_code == None or content_code != 'ValidTemplate' or content_code == None:
                self.put_testResult(res_page)
                raise Exception(f"Metadata Code is {metadata_code} and Content Code is {content_code} | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if a source page template is valid")
            req_source_template["payload"]["view"]["layoutId"] = layout_id
            res_page = self.validate_page_template(site_id, req_source_template)
            metadata_code = res_page.json().get('metadata').get('code')
            content_code = res_page.json().get('content').get('code')
            if metadata_code != 'ValidTemplate' or metadata_code == None or content_code != 'ValidTemplate' or content_code == None:
                self.put_testResult(res_page)
                raise Exception(f"Metadata Code is {metadata_code} and Content Code is {content_code} | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if user can preview visual page template")
            req_visual_template["payload"]["view"]["layoutId"] = layout_id
            req_visual_template["payload"]["view"]["template"]["blockNames"] = [f"{block_name}"]
            expected_title = str(req_visual_template["payload"]["view"]["template"]["metadata"])
            res_page = self.preview_new_page(site_id, req_visual_template)
            soup = BeautifulSoup(res_page.content, "html.parser")
            actual_title = str(soup.find("title"))
            if expected_title != actual_title:
                self.put_testResult(res_page)
                raise Exception(f"EXPECTED TITLE {expected_title} BUT GOT {actual_title}  | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if user can preview source page template")
            req_source_template["payload"]["view"]["layoutId"] = layout_id
            expected_title = str(req_source_template["payload"]["view"]["template"]["metadata"])
            res_page = self.preview_new_page(site_id, req_source_template)
            soup = BeautifulSoup(res_page.content, "html.parser")
            actual_title = str(soup.find("title"))
            if expected_title != actual_title:
                self.put_testResult(res_page)
                raise Exception(f"EXPECTED TITLE {expected_title} BUT GOT {actual_title}  | {res_page.json()}")
            self.test_passed(res=res_page)
            

            self.start_test(self.SCENARIO_NAME, "Verify if user can get all pages")
            res_page = self.get_all_pages(site_id)
            total_pages = res_page.json().get('totalCount')
            if total_pages == None:
                self.put_testResult(res_page)
                raise Exception(f"Total pages is {total_pages} | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, f"Verify if user can get visual page path")
            res_page = self.get_page(site_id, visual_page_id)
            page_path = res_page.json().get('path')
            if page_path == None:
                self.put_testResult(res_page)
                raise Exception(f"Page path is {page_path} | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, f"Verify if user can get source page path")
            res_page = self.get_page(site_id, source_page_id)
            page_path = res_page.json().get('path')
            if page_path == None:
                self.put_testResult(res_page)
                raise Exception(f"Page path is {page_path} | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, f"Verify if user can update visual page")
            req_update_visual_page['view']['layoutId'] = layout_id
            req_update_visual_page['view']['template']['blockNames'] = [f'{block_name}']
            expected_block_name = req_update_visual_page['view']['template']['blockNames'][0]
            res_page = self.update_page(site_id, visual_page_id, req_update_visual_page)
            actual_block_name = res_page.json().get('view').get('template').get('blockNames')[0]
            if expected_block_name != actual_block_name:
                self.put_testResult(res_page)
                raise Exception(f"EXPECTED BLOCK NAME {expected_block_name} BUT GOT {actual_block_name} | {res_page.json()}")
            self.test_passed(res=res_page)

            
            self.start_test(self.SCENARIO_NAME, f"Verify if user can update source page")
            req_update_source_page['view']['layoutId'] = layout_id
            req_update_source_page['view']['template']['content'] = f'<sp:block name=\"{block_name}\"></sp:block>'
            expected_content = req_update_source_page['view']['template']['content']
            res_page = self.update_page(site_id, source_page_id, req_update_source_page)
            actual_content = res_page.json().get('view').get('template').get('content')
            if expected_content != actual_content:
                self.put_testResult(res_page)
                raise Exception(f"EXPECTED CONTENT {expected_content} BUT GOT {actual_content} | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if user can preview existing visual page")
            expected_block_display_name = str(req_insert_form['displayName'])
            res_page = self.preview_existing_page(site_id, visual_page_id)
            soup = BeautifulSoup(res_page.content, "html.parser")
            actual_block_display_name = str(soup.find("div", class_="sp-form-item sp-form-html").text)
            if expected_block_display_name != actual_block_display_name:
                self.put_testResult(res_page)
                raise Exception(f"EXPECTED BLOCK DISPLAY NAME {expected_block_display_name} BUT GOT {actual_block_display_name} | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if user can preview existing source page")
            expected_block_display_name = str(req_insert_form['displayName'])
            res_page = self.preview_existing_page(site_id, source_page_id)
            soup = BeautifulSoup(res_page.content, "html.parser")
            actual_block_display_name = str(soup.find("div", class_="sp-form-item sp-form-html").text)
            if expected_block_display_name != actual_block_display_name:
                self.put_testResult(res_page)
                raise Exception(f"EXPECTED BLOCK DISPLAY NAME {expected_block_display_name} BUT GOT {actual_block_display_name} | {res_page.json()}")
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if user can create child page")
            req_child_page['parentId'] = visual_page_id
            req_child_page['view']['layoutId'] = layout_id
            res_page = self.create_page(site_id, req_child_page)
            child_page_id = res_page.json().get('id')
            if child_page_id == None:
                self.put_testResult(res_page)
                raise Exception(f"Child page ID is {child_page_id} | {res_page.json()}")
            page_ids.append(child_page_id)
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if user can view parent page")
            res_page = self.get_all_child_pages(site_id, child_page_id)
            actual_parent_id = res_page.json().get('parents')[0].get('id')
            if actual_parent_id != visual_page_id:
                self.put_testResult(res_page)
                raise Exception(f"Actual Parent ID is {actual_parent_id} | {res_page.json()}")
            self.test_passed(res=res_page)

            self.start_test(self.SCENARIO_NAME, "Verify if user can delete child page")
            res_page = self.delete_page(site_id, child_page_id)
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete visual setting page")
            res_page = self.delete_page(site_id, visual_page_id)
            self.test_passed(res=res_page)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete source setting page")
            res_page = self.delete_page(site_id, source_page_id)
            self.test_passed(res=res_page)

            self.delete_app(app_id)
            self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_app(app_id)
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)