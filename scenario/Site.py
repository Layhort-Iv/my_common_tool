
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
from utilities.SiteManagementAPI.SiteFunction import SiteFunction

@scenario(name="Site", description="Check the operation of Site Function")
class Site(Thread, testDecorator, SiteFunction):

    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Site")
        SiteFunction.__init__(self)
        self.writer = csvGenerator(fileName=f'{__name__.split(".")[1]}_{str(datetime.now()).split(" ")[0]}_{(str(datetime.now()).split(" ")[1].split(".")[0]).replace(":","-")}')
        self.user = user()
        self.user.logger = getLogger(__name__)
        

    def run(self):
        start_test(self.SCENARIO_NAME, "This process can take some time (up to 30 seconds)")
        with Path("request/PrivateAPI/CMS/Site/site.yml").open(encoding="utf-8") as file:
            req_site = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/Site/siteUpdate.yml").open(encoding="utf-8") as file:
            req_update_site = yaml.safe_load(file)

        try:
            req_site['displayName'] = "Site Auto Test - Site"
            req_site['name'] = "site"
            req_site['description'] = "Site Auto Test - Site"

            log_print(self.SCENARIO_NAME, "Check if the site has already existed")
            site_id = self.check_site(req_site)
            if site_id == None:
                log_print(self.SCENARIO_NAME, "Site does not exist")
            else:
                log_print(self.SCENARIO_NAME, "Site is already existed")
                self.delete_site(site_id)
                log_print(self.SCENARIO_NAME, "Successfully delete the site")

            self.start_test(self.SCENARIO_NAME, "Verify if user can create a site")
            res_site = self.create_site(req_site)
            site_id = res_site.json().get('id')
            if site_id == None:
                self.put_testResult(res_site)
                raise Exception(f"Site ID is {site_id} | {res_site.json()}")
            self.test_passed(res=res_site)


            self.start_test(self.SCENARIO_NAME, "Verify if user can sort site correctly")
            sort_types = ["id:asc", "id:desc", "name:asc", "name:desc", "displayName:asc", "displayName:desc", "createdAt:asc", "createdAt:desc", "updatedAt:asc", "updatedAt:desc"]
            for sort_type in sort_types:
                field, order = sort_type.split(':')
                self.start_test(self.SCENARIO_NAME, f"Sorting {field.capitalize()} in {'Ascending' if order=='asc' else 'Descending'} Order")
                sort_res = self.sort(field, order)
                validation_res = self.validate_sort_result(sort_res, field, order)
                if validation_res == False:
                    self.test_failed(f"Failed to sort site on Field: {field} and Order:{order} | {sort_res.json()}")
                self.test_passed(res=sort_res)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a site limit")
            req_limit = 1
            res_site = self.get_site_limit(req_limit)
            actual_limit = len(res_site.json().get('items'))
            if actual_limit != req_limit:
                self.put_testResult(res_site)
                raise Exception(f"EXPECTED: {req_limit} BUT GOT {actual_limit} | {res_site.json()}")
            self.test_passed(res=res_site)


            self.start_test(self.SCENARIO_NAME, "Verify if user can get a site")
            res_site = self.get_site(site_id)
            site_name = res_site.json().get('name')
            if site_name == None:
                self.put_testResult(res_site)
                raise Exception(f"Site name is {site_name} | {res_site.json()}")
            self.test_passed(res=res_site)


            self.start_test(self.SCENARIO_NAME, "Verify if user can enable site usage")
            res_site = self.enable_usage(site_id)
            expected_status = True
            isEnabled = res_site.json().get('enabled')
            if isEnabled == False:
                self.put_testResult(res_site)
                raise Exception(f"EXPECTED: {expected_status} BUT GOT {isEnabled} | {res_site.json()}")
            self.test_passed(res=res_site)


            self.start_test(self.SCENARIO_NAME, "Verify if user can update site")
            res_site = self.update_site(site_id, req_update_site)
            req_update_name = req_update_site['name']
            res_site_name = res_site.json().get('name')
            if res_site_name != req_update_name:
                self.put_testResult(res_site)
                raise Exception(f"EXPECTED: {req_update_name} BUT GOT {res_site_name} | {res_site.json()}")
            self.test_passed(res=res_site)


            self.start_test(self.SCENARIO_NAME, "Verify if user get robot.txt")
            res_site = self.get_robots_txt(site_id)
            robot_txt = res_site.json().get('text')
            if robot_txt == None:
                self.put_testResult(res_site)
                raise Exception(f"Robot.txt content is {robot_txt} | {res_site.json()}")
            self.test_passed(res=res_site)


            self.start_test(self.SCENARIO_NAME, "Verify if user update robot.txt")
            # block google bot on all pages
            req_robots_txt = {
                "text": "User-agent: Googlebot\nDisallow: /\n"
            }
            res_site = self.update_robots_txt(site_id, req_robots_txt)
            updated_robots_txt = res_site.json().get('text')
            if updated_robots_txt == robot_txt:
                self.put_testResult(res_site)
                raise Exception(f"EXPECTED: {req_robots_txt} BUT GOT {updated_robots_txt} | {res_site.json()}")
            self.test_passed(res=res_site)


            self.start_test(self.SCENARIO_NAME, "Verify if user can delete site")
            res_site = self.delete_site(site_id)
            self.test_passed(res=res_site)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)