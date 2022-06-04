
from re import L
from threading import Thread, current_thread
from logging import getLogger
from stdtest.display import end_test, log_print, start_test, ng
from stdtest.User import User
from stdtest.decorator import scenario, inject
import yaml
from pathlib import Path
from datetime import datetime
from stdtest.csvGenerator import csvGenerator
from stdtest.testDecorator import testDecorator
from utilities.SiteManagementAPI.SiteFunction import SiteFunction
from utilities.SiteManagementAPI.SiteManagementGroupFunction import SiteManagementGroupFunction
from utilities.AccountManagementAPI.AccountGroupFunction import AccountGroupFunction

@scenario(name="SiteManagementGroup", description="Check the operation of Site Management Group Function")
class SiteManagementGroup(Thread, testDecorator, SiteFunction, AccountGroupFunction, SiteManagementGroupFunction):

    @inject(user=User)
    def __init__(self, user):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Site Management Group")
        SiteManagementGroupFunction.__init__(self)
        self.writer = csvGenerator(fileName=f'{__name__.split(".")[1]}_{str(datetime.now()).split(" ")[0]}_{(str(datetime.now()).split(" ")[1].split(".")[0]).replace(":","-")}')
        self.user = user()
        self.user.logger = getLogger(__name__)
        

    def run(self):
        start_test(self.SCENARIO_NAME, "This process can take some time (up to 30 seconds)")
        with Path("request/PrivateAPI/CMS/Site/site.yml").open(encoding="utf-8") as file:
            req_site = yaml.safe_load(file)
        with Path("request/PrivateAPI/AccountManagement/Group/group.yml").open(encoding="utf-8") as file:
            req_account_group = yaml.safe_load(file)
        with Path("request/PrivateAPI/AccountManagement/Group/reqMemberships.yml").open(encoding="utf-8") as file:
            req_user = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteManagementGroup/group1.yml").open(encoding="utf-8") as file:
            req_group1 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteManagementGroup/group2.yml").open(encoding="utf-8") as file:
            req_group2 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteManagementGroup/group3.yml").open(encoding="utf-8") as file:
            req_group3 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteManagementGroup/group4.yml").open(encoding="utf-8") as file:
            req_group4 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteManagementGroup/group5.yml").open(encoding="utf-8") as file:
            req_group5 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteManagementGroup/group6.yml").open(encoding="utf-8") as file:
            req_group6 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteManagementGroup/req_update_group1.yml").open(encoding="utf-8") as file:
            req_update_group1 = yaml.safe_load(file)
        with Path("request/PrivateAPI/CMS/SiteManagementGroup/req_update_group6.yml").open(encoding="utf-8") as file:
            req_update_group6 = yaml.safe_load(file)
        

        try:
            req_site['displayName'] = "Site Auto Test - Site Management Group"
            req_site['name'] = "sitemanagement"
            req_site['description'] = "Site Auto Test - Site Management Group"

            NUM_GROUPS = 6
            site_management_group_ids = []
            account_group_ids = []
            req_site_management_groups = [req_group1, req_group2, req_group3, req_group4, req_group5, req_group6]
            site_management_roles = ["setting authority", "use test site authority", "release authority", "security authority", "full one part authority", "full admin authority"]
            req_update_groups = [req_update_group1, req_update_group6]

            log_print(self.SCENARIO_NAME, "Check if the site already existed")
            site_id = self.check_site(req_site)
            if site_id == None:
                log_print(self.SCENARIO_NAME, "Site does not exist")
            else:
                log_print(self.SCENARIO_NAME, "Site has already existed. Deleting the site.")
                SiteFunction.delete_site(self, site_id)

            site_id = self.create_site(req_site).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create site")

            for i in range(NUM_GROUPS):
                req_account_group['displayName'] = f"Group {i+1}"
                req_account_group['name'] = f"Group{i+1}"
                account_group_name = req_account_group['name']
                account_group_id = self.check_account_group(req_account_group)
                if account_group_id == None:
                    log_print(self.SCENARIO_NAME, f"{account_group_name} does not exist.")
                else:
                    log_print(self.SCENARIO_NAME, f"{account_group_name} is already existed. Deleting account group.")
                    self.delete_account_group(account_group_id)

                account_group_id = self.create_account_group(req_account_group).json().get('id')
                log_print(self.SCENARIO_NAME, f"Successfully create account group with this name {account_group_name}")
                account_group_ids.append(account_group_id)
                self.add_memberships(account_group_ids[i], req_user)

            log_print(self.SCENARIO_NAME, "Successfully create all required account group and added user to group")
                
            for i in range(NUM_GROUPS):
                self.start_test(self.SCENARIO_NAME, f"Verify if user can create site management group with {site_management_roles[i]}")
                req_site_management_groups[i]['groupId'] = account_group_ids[i]
                res_site_management_group = self.create_site_management_group(site_id, req_site_management_groups[i])
                site_management_group_id = res_site_management_group.json().get('group').get('id')
                if site_management_group_id == None:
                    raise Exception(f"Failed to create site management group with {site_management_roles[i]} | {res_site_management_group.json()}")
                site_management_group_ids.append(site_management_group_id)
                self.test_passed(res=res_site_management_group)


                self.start_test(self.SCENARIO_NAME, f"Verify if user can get a site management group with {site_management_roles[i]}")
                res_site_management_group = self.get_site_management_group(site_id, site_management_group_id)
                site_management_group_name = res_site_management_group.json().get('group').get('name')
                if site_management_group_name == None:
                    raise Exception(f"Failed to get a site management group with {site_management_roles[i]} | {res_site_management_group.json()}")
                self.test_passed(res=res_site_management_group)

                if i == 0:
                    self.start_test(self.SCENARIO_NAME, "Verify if user can update site management group from one part authority to admin")
                    res_site_management_group = self.update_site_management_group(site_id, site_management_group_ids[0], req_update_groups[0])
                    updated_role = res_site_management_group.json().get('group').get('isAdmin')
                    if updated_role == False:
                        raise Exception(f"Failed to update site management group from one part authority to admin | {res_site_management_group.json()}")
                    self.test_passed(res=res_site_management_group)

                
                if i == 5:
                    self.start_test(self.SCENARIO_NAME, "Verify if user can update site management group from admin to one part authority")
                    res_site_management_group = self.update_site_management_group(site_id, site_management_group_ids[5], req_update_groups[1])
                    updated_role = res_site_management_group.json().get('group').get('isAdmin')
                    if updated_role == True:
                        raise Exception(f"Failed to update site management group from admin to one part authority | {res_site_management_group.json()}")
                    self.test_passed(res=res_site_management_group)
            

                self.start_test(self.SCENARIO_NAME, f"Verify if user can delete site management group with {site_management_roles[i]}")
                res_site_management_group = self.delete_site_management_group(site_id, site_management_group_ids[i])
                self.test_passed(res=res_site_management_group)
            

            self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)