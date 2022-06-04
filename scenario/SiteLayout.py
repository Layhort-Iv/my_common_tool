
from threading import Thread, current_thread
from logging import getLogger
from stdtest.display import end_test, log_print, start_test
from stdtest.User import User
from stdtest.decorator import scenario, inject
import yaml
from pathlib import Path
from datetime import datetime
from stdtest.csvGenerator import csvGenerator
from stdtest.testDecorator import testDecorator
from utilities.SiteManagementAPI.SiteFunction import SiteFunction
from utilities.SiteManagementAPI.LayoutFuntion import LayoutFunction

@scenario(name="SiteLayout", description="Check the operation of Site Layout Function")
class SiteLayout(Thread, testDecorator, SiteFunction, LayoutFunction):

    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Site Layout")
        LayoutFunction.__init__(self)
        self.writer = csvGenerator(fileName=f'{__name__.split(".")[1]}_{str(datetime.now()).split(" ")[0]}_{(str(datetime.now()).split(" ")[1].split(".")[0]).replace(":","-")}')
        self.user = user()
        self.user.logger = getLogger(__name__)
        

    def run(self):
        start_test(self.SCENARIO_NAME, "This process can take some time (up to 30 seconds)")
        with Path("request/PrivateAPI/CMS/Site/site.yml").open(encoding="utf-8") as file:
            req_site = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteLayout/siteLayout.yml").open(encoding="utf-8") as file:
            req_site_layout = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteLayout/siteLayoutUpdate.yml").open(encoding="utf-8") as file:
            req_site_layout_update = yaml.safe_load(file)

        try:
            req_site['displayName'] = "Site Auto Test - Site Layout"
            req_site['name'] = "sitelayout"
            req_site['description'] = "Site Auto Test - Site Layout"

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


            self.start_test(self.SCENARIO_NAME, "Verify if user can create site layout")
            res_layout = self.create_site_layout(site_id, req_site_layout)
            layout_id = res_layout.json().get('id')
            if layout_id == None:
                self.put_testResult(res_layout)
                raise Exception(f"Site Layout ID is {layout_id} | {res_layout.json()}")
            self.test_passed(res=res_layout)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get all site layout")
            res_layout = self.get_all_site_layouts(site_id)
            total_layout = res_layout.json().get('totalCount')
            if total_layout == None or total_layout == 0:
                self.put_testResult(res_layout)
                raise Exception(f"Total layout is {total_layout} | {res_layout.json()}")
            self.test_passed(res=res_layout)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a site layout")
            res_layout = self.get_site_layout(site_id, layout_id)
            layout_name = res_layout.json().get('name')
            if layout_name == None:
                self.put_testResult(res_layout)
                raise Exception(f"Site name is {layout_name} | {res_layout.json()}")
            self.test_passed(res=res_layout)


            self.start_test(self.SCENARIO_NAME, "Verify if user can update a site layout")
            expected_layout_name = req_site_layout_update['name']
            res_layout = self.update_site_layout(site_id, layout_id, req_site_layout_update)
            actual_layout_name = res_layout.json().get('name')
            if actual_layout_name != expected_layout_name or actual_layout_name == None:
                self.put_testResult(res_layout)
                raise Exception(f"EXPECTED NAME {expected_layout_name} BUT GOT {actual_layout_name} | {res_layout.json()}")
            self.test_passed(res=res_layout)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete site layout")
            res_delete = self.delte_site_layout(site_id, layout_id)
            self.test_passed(res=res_delete)

            self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)