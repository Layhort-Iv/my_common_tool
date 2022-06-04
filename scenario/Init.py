from requests import api
from stdtest.decorator import inject
from stdtest.User import User
from logging import getLogger
from datetime import datetime, timedelta, timezone
import dateutil.parser
from stdtest.display import check, ok, ng
from queue import Queue
import yaml
from pathlib import Path

class Init:

    @inject(user=User)
    def __init__(self, user):
        self.user = user()
        self.user.logger = getLogger(__name__)
        self.error_queue = Queue()
    def start(self):
        SCENARIO_NAME = "init"
        check(SCENARIO_NAME)
        if(self.error_queue.empty()):
            ok(SCENARIO_NAME)
        else:
            while not self.error_queue.empty():
                ng(SCENARIO_NAME, self.error_queue.get())
    
    def delete_apps(self):
        try:
            res_r = self.user.get("/apps?query=stdtest")
            if not res_r.status_code == 200:
                self.error_queue.put(Exception("過去作成されたアプリの削除に失敗しました。手動でアプリを削除してください"))
            for app in res_r.json().get("items"):
                if dateutil.parser.parse(app["updatedAt"]).astimezone(timezone.utc) + timedelta(minutes=5) < datetime.now(timezone.utc):
                    res_d = self.user.delete("/apps/{}".format(app.get("id")))
                    if not res_d.status_code == 204:
                        self.error_queue.put(Exception("過去作成されたアプリの削除に失敗しました。手動でアプリを削除してください"))
        except Exception as e:
            self.error_queue.put(e)
                
    def delete_device_collections(self):
        try:
            res_r = self.user.get("/deviceCollections?query=stdtest")
            if not res_r.status_code == 200:
                self.error_queue.put(Exception("過去作成されたデバイスコレクションの削除に失敗しました。手動でデバイスコレクションを削除してください"))
            for device_collection in res_r.json().get("items"):
                if dateutil.parser.parse(device_collection["updatedAt"]).astimezone(timezone.utc) + timedelta(minutes=5) < datetime.now(timezone.utc):
                    res_d = self.user.delete("/deviceCollections/{}".format(device_collection.get("id")))
                    if not res_d.status_code == 204:
                        self.error_queue.put(Exception("過去作成されたデバイスコレクションの削除に失敗しました。手動でデバイスコレクションを削除してください"))
        except Exception as e:
            self.error_queue.put(e)


    
