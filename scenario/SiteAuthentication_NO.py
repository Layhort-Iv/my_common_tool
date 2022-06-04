from threading import Thread, current_thread
from logging import getLogger
import json
from stdtest.display import check, log_print, ng
from stdtest.User import User
from stdtest.decorator import scenario, inject
import yaml
from pathlib import Path
from datetime import datetime
from stdtest.csvGenerator import csvGenerator
from utilities.AppManagementAPI.AppFunction import AppFunction
from utilities.AppManagementAPI.DBFunction import DBFunction
from utilities.AppManagementAPI.RecordFunction import RecordFunction
from utilities.SiteManagementAPI.SiteFunction import SiteFunction
from utilities.AccountManagementAPI.ApiAgentFunction import ApiAgentFunction
from utilities.AccountManagementAPI.ApiKeyFunction import ApiKeyFunction
from utilities.SiteManagementAPI.AuthAreaFunction import AuthAreaFunction
from utilities.SiteManagementAPI.LayoutFuntion import LayoutFunction
from utilities.SiteManagementAPI.PageFunction import PageFunction
from utilities.SiteManagementAPI.ReleaseFunction import ReleaseFunction
from utilities.SiteManagementAPI.SiteApiUseGroupFunction import SiteApiUseGroupFunction
from utilities.SiteManagementAPI.SiteAuthenticationFunction import SiteAuthenticationFunction

@scenario(name="SiteAuthentication_NO", description="Check the operation of Site Authentication")
class SiteAuthentication(Thread, AppFunction, DBFunction, SiteFunction, ApiAgentFunction, ApiKeyFunction, AuthAreaFunction, LayoutFunction, ReleaseFunction, PageFunction):

    @inject(user=User)
    def __init__(self, user):
        self.SCENARIO_NAME = "Site Authentication"
        super().__init__(name=current_thread().name + ">" + __name__)
        SiteFunction.__init__(self, self.SCENARIO_NAME)
        self.writer = csvGenerator(fileName=f'{__name__.split(".")[1]}_{str(datetime.now()).split(" ")[0]}_{(str(datetime.now()).split(" ")[1].split(".")[0]).replace(":","-")}')
        self.user = user()
        self.user.logger = getLogger(__name__)

    def run(self):
        with Path("request/PublicAPI/AppManagement/App/app.yml").open(encoding="utf-8") as file:
            req_app = yaml.safe_load(file)
        with Path("request/PublicAPI/AppManagement/DB/db.yml").open(encoding="utf-8") as file:
            req_db = yaml.safe_load(file)
        with Path("request/PublicAPI/CMS/Site/site.yml").open(encoding="utf-8") as file:
            req_site = yaml.safe_load(file)
        with Path("request/PublicAPI/CMS/AuthArea/authArea.yml").open(encoding="utf-8") as file:
            req_auth_area = yaml.safe_load(file)
        with Path("request/PublicAPI/CMS/ApiAgent/apiAgent.yml").open(encoding="utf-8") as file:
            req_api_agent = yaml.safe_load(file)
        with Path("request/PublicAPI/CMS/Group/group.yml").open(encoding="utf-8") as file:
            req_group = yaml.safe_load(file)
        # with Path("request/PublicAPI_1_1/record.yml").open(encoding="utf-8") as file:
        #     req_record = yaml.safe_load(file)
        with Path("request/PublicAPI/CMS/SiteRelease/siteRelease.yml").open(encoding="utf-8") as file:
            req_site_release = yaml.safe_load(file)

        # Devel
        # userId = ["27", "28"]

        # QA
        userId = ["2174", "2175"]

        log_print(self.SCENARIO_NAME, "Setting up ...")
        try:
            req_app['displayName'] = "App Auto Test - Site Authentication"
            req_app['name'] = "SiteAuthentication"
            req_app['description'] = "App Auto Test - Site Authentication"

            log_print(self.SCENARIO_NAME, "Check if the app has already existed")
            app_id = self.check_app(req_app)
            if app_id == None:
                log_print(self.SCENARIO_NAME, "App does not exist")          
            else:
                log_print(self.SCENARIO_NAME, "App has already existed - Deleting the app")
                self.delete_app(app_id)
                log_print(self.SCENARIO_NAME, "Successfully delete app")
                
                
            app_id = self.create_app(req_app).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create an app")
            db_id = self.create_db(app_id, req_db).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create a DB")

        except Exception as e:
            if app_id == None:
                return
            self.delete_app(app_id)

        try:
            req_site['displayName'] = "Site Auto Test - Site Authentication"
            req_site['name'] = "authentication"
            req_site['description'] = "Site Auto Test - Page"

            log_print(self.SCENARIO_NAME, "Check if the site already existed")
            site_id = self.check_site(req_site)
            if site_id == None:
                log_print(self.SCENARIO_NAME, "Site does not exist")
            else:
                log_print(self.SCENARIO_NAME, "Site has already existed. Deleting the site")
                self.delete_site(site_id)

            log_print(self.SCENARIO_NAME, "Check if we can create a site")
            res_site = self.create_site(req_site)
            site_id = res_site.json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create site")

            api_agent_id = self.check_api_agent(req_api_agent)
            if api_agent_id == None:
                log_print(self.SCENARIO_NAME, "API Agent does not exist")
            else:
                log_print(self.SCENARIO_NAME, "API Agent is already existed - Deleting it")
                self.delete_api_agent(api_agent_id)
                log_print(self.SCENARIO_NAME, "Successfully delete API Agent")

            log_print(self.SCENARIO_NAME, "Check if we can create api agent")
            api_agent_id = self.create_api_agent(req_api_agent).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create API Agent")

            req_api_key = {
                "displayName": "API KEY",
                "scopes": ["all"]
            }
            res_api_key = self.create_api_key(api_agent_id, req_api_key).json()
            log_print(self.SCENARIO_NAME, "Successfully create api agent")
            api_key_id = res_api_key.get('id')
            api_agent_key = res_api_key.get('key')

            req_api_key = {
                "enabled": True
            }

            status = self.update_api_key(api_agent_id, api_key_id, req_api_key).json().get('enabled')
            if status != True:
                raise Exception("Failed to activate api agent key")
            log_print(self.SCENARIO_NAME, "Successfully activate api agent key")

            site_group_id = self.check_group(req_group)
            if site_group_id == None:
                log_print(self.SCENARIO_NAME, "Group does not exist - Creating a new one")
                site_group_id = self.create_site_group(req_group).json().get('id')
                log_print(self.SCENARIO_NAME, "Successfully create site group")
            else:
                log_print(self.SCENARIO_NAME, "Group is already existed - Reusing it")

            req_user = {
                "addMemberships": userId
            }
            self.add_memberships(site_group_id, req_user)
            log_print(self.SCENARIO_NAME, "Successfully add user to group")

            req_auth_area["dbId"] = db_id
            auth_area_id = self.create_auth_area(site_id, req_auth_area).json().get('id')
            log_print(self.SCENARIO_NAME, "Successfully create authentication area")

            pages_id = []
            pages_path = []
            blocks_id = []
            layout_id = self.get_all_site_layouts(site_id).json().get('items')[0].get('id')
            res_pages = self.get_all_pages(site_id).json().get('items')

            for page in res_pages:
                pages_id.append(page.get('id'))
                blocks_id.append(page.get('view').get('template').get('content'))
                pages_path.append(page.get('path'))

            req_site_release["layoutIds"] = [f"{layout_id}"]
            req_site_release["pageIds"] = pages_id
            req_site_release["authenticationIds"] = [f"{auth_area_id}"]

            print(blocks_id)

            # release_id = self.release_site(site_id, req_site_release).json().get('id')
            # SEC_TIMEOUT = 30
            # SEC_SLEEP = 1
            # for i in range(SEC_SLEEP, SEC_TIMEOUT):
            #     status = self.get_site_release(site_id, release_id).json().get('status')
            #     if status == "succeeded":
            #         break
            #     elif status == "failed":
            #         raise Exception("Failed to release site")
            #     else:
            #         continue
            # log_print(self.SCENARIO_NAME, "Successfully release the site")

            # req_memberships = {
            #     "groupId": site_group_id,
            #     "authenticationIds": [
            #         auth_area_id
            #     ]
            # }
            # SiteApiUseGroupFunction.create_site_auth_api(self, site_id, req_memberships)
            # log_print(self.SCENARIO_NAME, "Successfully Create Sith Authentication API ")

            # req_agent_memberships = {
            #     "addAgentMemberships": [api_agent_id]
            # }
            # GroupFunction.add_agent_memberships(self, site_group_id, req_agent_memberships)
            # log_print(self.SCENARIO_NAME, "Successfully Add API Agent To Group")

            # header = {
            # "content-type": "application/json",
            # "Authorization": "Bearer {}".format(api_agent_key),
            # "X-Spiral-Api-Version":"1.1",
            # "X-Spiral-App-Authority":"manage",
            # "X-Spiral-App-Role":"_fullAccess"
            # }

        except Exception as e:
            if site_id == None:
                return
            ng(self.SCENARIO_NAME, e)
            self.delete_site(site_id)



    #     try:
    #         req_auth_area["dbId"] = db_id
    #         auth_area_id = AuthAreaFunction.create_auth_area(self, site_id, req_auth_area).json().get('id')
    #         log_print(SCENARIO_NAME, "Successfully Create Authentication Area")

    #         pages_id = []
    #         pages_path = []
    #         layout_id = LayoutFunction.get_all_layouts(self, site_id).json().get('items')[0].get('id')
    #         res_pages = PageFunction.get_all_pages(self, site_id).json().get('items')

    #         for page in res_pages:
    #             pages_id.append(page.get('id'))
    #             pages_path.append(page.get('path'))

    #         req_site_release["layoutIds"] = [f"{layout_id}"]
    #         req_site_release["pageIds"] = [
    #             f"{pages_id[0]}",
    #             f"{pages_id[1]}",
    #             f"{pages_id[2]}",
    #             f"{pages_id[3]}"
    #         ]
    #         req_site_release["authenticationIds"] = [f"{auth_area_id}"]

    #         release_id = SiteReleaseFunction.release_site(self, site_id, req_site_release).json().get('id')
    #         SEC_TIMEOUT = 30
    #         SEC_SLEEP = 1
    #         for i in range(SEC_SLEEP, SEC_TIMEOUT):
    #             status = SiteReleaseFunction.get_site_release(self, site_id, release_id).json().get('status')
    #             if status == "succeeded":
    #                 break
    #             elif status == "failed":
    #                 raise Exception("Failed to release site")
    #             else:
    #                 continue
    #         log_print(SCENARIO_NAME, "Successfully release the site")

    #         req_memberships = {
    #             "groupId": site_group_id,
    #             "authenticationIds": [
    #                 auth_area_id
    #             ]
    #         }
    #         SiteApiUseGroupFunction.create_site_auth_api(self, site_id, req_memberships)
    #         log_print(SCENARIO_NAME, "Successfully Create Sith Authentication API ")

    #         req_agent_memberships = {
    #             "addAgentMemberships": [api_agent_id]
    #         }
    #         GroupFunction.add_agent_memberships(self, site_group_id, req_agent_memberships)
    #         log_print(SCENARIO_NAME, "Successfully Add API Agent To Group")

    #         header = {
    #         "content-type": "application/json",
    #         "Authorization": "Bearer {}".format(api_agent_key),
    #         "X-Spiral-Api-Version":"1.1",
    #         "X-Spiral-App-Authority":"manage",
    #         "X-Spiral-App-Role":"_fullAccess"
    #         }

    #         ok(SCENARIO_NAME, "Finish setting up!")

    #         check(SCENARIO_NAME, "Check if we can login to the authentication area")
    #         auth_area_login_body = {
    #             "id": "test-1@test-av.smp.ne.jp",
    #             "password": "Test@123"
    #         }
    #         res_auth_area_login = SiteAuthenticationFunction.auth_area_login(self, site_id, auth_area_id, auth_area_login_body, header).json()
    #         recordId = res_auth_area_login.get('recordId')
    #         auth_area_token = res_auth_area_login.get('token')
    #         if record_id != recordId or record_id == None or auth_area_token == None:
    #             raise Exception("Failed to perform site authentication login")
    #         log_print(f"API KEY : {api_agent_key}")
    #         log_print(f"Auth Area Token : {auth_area_token}")
    #         ok(SCENARIO_NAME, "Successfully login to the authentication area")

    #         check(SCENARIO_NAME, "Check the validity of authentication area token ")
    #         req_auth_token = {
    #             "token": auth_area_token
    #         }
    #         auth_token_status = SiteAuthenticationFunction.validate_auth_token(self, site_id, auth_area_id, req_auth_token, header).json().get('status')
    #         if auth_token_status == False:
    #             raise Exception(f"Failed to validate authentication area token | Status: {auth_token_status}")
    #         ok(SCENARIO_NAME, f"Successfully validate authentication area token")
            
    #         check(SCENARIO_NAME, "Check if we can issue an one-time for authentication area login")
    #         req_one_time_url_login = {
    #             "token": auth_area_token,
    #             "path": pages_path[0]
    #         }
    #         one_time_url_login = SiteAuthenticationFunction.issue_one_time_url_login(self, site_id, auth_area_id, req_one_time_url_login, header).json().get('url')
    #         if one_time_url_login == None:
    #             raise Exception(f"Failed to issuse an one-time URL for authentication area login | Body: {one_time_url_login}")
    #         ok(SCENARIO_NAME, "Successfully issue an one-time URL for authentication area login")

    #         check(SCENARIO_NAME, "Check if we can logout from authentication area")
    #         auth_token_status_before = SiteAuthenticationFunction.validate_auth_token(self, site_id, auth_area_id, req_auth_token, header).json().get('status')
    #         log_print(SCENARIO_NAME, f"Status before logout: {auth_token_status_before}")
    #         SiteAuthenticationFunction.auth_area_logout(self, site_id, auth_area_id, req_auth_token, header)
    #         auth_token_status_after = SiteAuthenticationFunction.validate_auth_token(self, site_id, auth_area_id, req_auth_token, header).json().get('status')
    #         log_print(SCENARIO_NAME, f"Status after logout: {auth_token_status_after}")
    #         if auth_token_status_after == auth_token_status_before:
    #             raise Exception("Failed to logout from authentication area")
    #         ok(SCENARIO_NAME, "Successfully logout from authentication area")

            
    #     except Exception as e:
    #         AppFunction.delete_app(self, app_id)
    #         SiteFunction.delete_site(self, site_id)
    #         ApiAgentFunction.delete_api_agent(self, api_agent_id)
    #         GroupFunction.delete_site_group(self, site_group_id)
    #         ng(SCENARIO_NAME, e)
    #         return 

    #     AppFunction.delete_app(self, app_id)
    #     log_print(SCENARIO_NAME, "Successfully Deleted the App")
    #     SiteFunction.delete_site(self, site_id)
    #     log_print(SCENARIO_NAME, "Successfully Delete the Site")
    #     ApiAgentFunction.delete_api_agent(self, api_agent_id)
    #     log_print(SCENARIO_NAME, "Successfully Deleted API Agent")
    #     GroupFunction.delete_site_group(self, site_group_id)
    #     log_print(SCENARIO_NAME, "Successfully Delete the Site Group")
    #     ok(SCENARIO_NAME, "Test Success")

    # @process("Login to Authentication Area")
    # def auth_area_login(self, site_id, auth_area_id, auth_area_login_body, header):
    #     res = self.user.post("/sites/{}/authentications/{}/login".format(site_id, auth_area_id), header=header, body = json.dumps(auth_area_login_body), sys_api = False)
    #     if not res.status_code == 200:
    #         raise Exception("Failed to login to authentication area")
    #     return res

    # @process("Validate Authentication Area Token")
    # def validate_auth_token(self, site_id, auth_area_id, req_auth_token, header):
    #     res = self.user.post("/sites/{}/authentications/{}/status".format(site_id, auth_area_id), header=header, body = json.dumps(req_auth_token), sys_api = False)
    #     if not res.status_code == 200:
    #         raise Exception("Failed to validate authentication area token")
    #     return res

    # @process("Issue One-Time URL for Authentication Area Login")
    # def issue_one_time_url_login(self, site_id, auth_area_id, req_one_time_url_login, header):
    #     res = self.user.post("/sites/{}/authentications/{}/oneTimeLogin".format(site_id, auth_area_id), header=header, body = json.dumps(req_one_time_url_login), sys_api = False)
    #     if not res.status_code == 200:
    #         raise Exception("Failed to issue one-time URL for authentication area login")
    #     return res

    # @process("Logout From Authentication Area")
    # def auth_area_logout(self, site_id, auth_area_id, req_auth_token, header):
    #     res = self.user.post("/sites/{}/authentications/{}/logout".format(site_id, auth_area_id), header=header, body = json.dumps(req_auth_token), sys_api = False)
    #     if not res.status_code == 204:
    #         raise Exception("Failed to logout from authentication area")
    #     return res