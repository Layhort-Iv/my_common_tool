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
from utilities.AppManagementAPI.MultiRecordMailActionFunction import MultiRecordMailActionFunction
from utilities.SiteManagementAPI.SiteFunction import SiteFunction
from utilities.SiteManagementAPI.InsertFormFunction import InsertFormFunction


@scenario(name="MultiRecordMailAction", description="Check the operation of Single Record Mail Action Function")
class MultiRecordMailAction(Thread, testDecorator, AppFunction, DBFunction, SiteFunction, MultiRecordMailActionFunction):

    @inject(user=User, option=Option)
    def __init__(self, user, option):
        super().__init__(name=current_thread().name + ">" + __name__)
        testDecorator.__init__(self, "Multi Record Mail Action")
        MultiRecordMailActionFunction.__init__(self, "multiRecordMailActions", "multi record mail action")
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

        
        try:
            req_app['displayName'] = "App Auto Test - Multi Record Mail Action"
            req_app['name'] = "MultiRecordMailActionApp"
            req_app['description'] = "App Auto Test - Multi Record Mail Action"

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
            req_site['displayName'] = "Site Auto Test - Multi Record Mail Action"
            req_site['name'] = "multirecord"
            req_site['description'] = "Site Auto Test - Multi Record Mail Action"
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


            # self.delete_app(app_id)
            # self.delete_site(site_id)

        except Exception as e:
            self.test_failed(e)
            if site_id == None:
                return
            # self.delete_app(app_id)
            # self.delete_site(site_id)

        end_test(self.SCENARIO_NAME)