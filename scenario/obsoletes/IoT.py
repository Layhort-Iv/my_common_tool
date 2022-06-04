from stdtest.decorator import scenario, inject, process
from stdtest.User import User
from stdtest.Device import Device
from pathlib import Path
import yaml
import json
from logging import getLogger
from time import sleep
from threading import Thread, current_thread
from queue import Queue
from _functools import reduce
from stdtest.display import check, ok, ng

@scenario(name="iot", description="IoT周りの動作を確認します")
class IoT(Thread):
    
    @inject(user=User, device=Device)
    def __init__(self, user, device):
        super().__init__(name=current_thread().name + ">" + __name__)
        self.user = user()
        self.device1 = device()
        self.device2 = device()
        self.device3 = device()
        self.logger = getLogger(__name__)
        self.user.logger = self.logger
        self.device1.logger = self.device2.logger = self.device3.logger = self.logger
        self.error_queue = Queue()
        self.TRANSMISSION_COUNT = 10
        self.MAX_LATENCY = 25
        self.AGGREGATION_INTERVAL = 20
    
    def run(self):
        SCENARIO_NAME = "IoT"
        check(SCENARIO_NAME, "この処理には終了まで20秒程要します")
        with Path("request/iot/app.yml").open(encoding="utf-8") as file:
            req_app = yaml.load(file)
        with Path("request/iot/db_device.yml").open(encoding="utf-8") as file:
            req_db_device = yaml.load(file)
        with Path("request/iot/db_result.yml").open(encoding="utf-8") as file:
            req_db_result = yaml.load(file)
        with Path("request/iot/devicecollection.yml").open(encoding="utf-8") as file:
            req_devicecollection = yaml.load(file)
        with Path("request/iot/device1.yml").open(encoding="utf-8") as file:
            req_device1 = yaml.load(file)
        with Path("request/iot/device2.yml").open(encoding="utf-8") as file:
            req_device2 = yaml.load(file)
        with Path("request/iot/device3.yml").open(encoding="utf-8") as file:
            req_device3 = yaml.load(file)
        with Path("request/iot/topic.yml").open(encoding="utf-8") as file:
            req_topic = yaml.load(file)
        with Path("request/iot/stream.yml").open(encoding="utf-8") as file:
            req_stream = yaml.load(file)
        with Path("request/iot/trigger.yml").open(encoding="utf-8") as file:
            req_trigger = yaml.load(file)
        try:
            res_app = self.create_app(req_app)
            app_id = res_app.json().get("id")
        except Exception as e:
            ng(SCENARIO_NAME, e)
            return
        try:
            req_db_device["app"] = req_db_result["app"] = app_id
            res_dbs = self.create_db(req_db_device, req_db_result, app_id)
            db_device_id = res_dbs[0].json().get("id")
            db_result_id = res_dbs[1].json().get("id")
            req_devicecollection["db"] = db_device_id
            res_device_collection = self.create_device_collection(req_devicecollection)
            device_collection_id = res_device_collection.json().get("id")
        except Exception as e:
            self.user.delete("/apps/{}".format(app_id))
            ng(SCENARIO_NAME, e)
            return
        try:
            res_devices = self.create_device(req_device1, req_device2, req_device3, device_collection_id)
            device1_name = res_devices[0].json().get("deviceName")
            device1_pass = res_devices[0].json().get("password")
            device2_name = res_devices[1].json().get("deviceName")
            device2_pass = res_devices[1].json().get("password")
            device3_name = res_devices[2].json().get("deviceName")
            device3_pass = res_devices[2].json().get("password")
            req_topic["deviceCollection"] = device_collection_id
            res_topic = self.create_topic(req_topic)
            topic_id = res_topic.json().get("id")
            req_stream["measures"][0]["statsMapping"]["db"] = db_result_id
            req_stream["topic"] = topic_id
            res_stream = self.create_stream(req_stream)
            stream_id = res_stream.json().get("id")
            req_trigger["actions"][0]["topic"] = topic_id
            res_trigger = self.create_trigger(req_trigger, stream_id)
        except Exception as e:
            self.user.delete("/apps/{}".format(app_id))
            self.user.delete("/deviceCollections/{}".format(device_collection_id))
            ng(SCENARIO_NAME, e)
            return
        th_1 = Thread(
            target=self.publish_from_user,
            name=current_thread().name + ">" + __name__ + self.publish_from_user.__name__,
            args=(topic_id, device_collection_id + "." + device1_name, device1_pass)
        )
        th_2 = Thread(
            target=self.publish_from_device,
            name=current_thread().name + "-" + __name__ + "." + self.publish_from_device.__name__,
            args=(db_result_id, topic_id, device_collection_id + "." + device2_name, device2_pass)
        )
        th_3 = Thread(
            target=self.pull_trigger,
            name=current_thread().name + "-" + __name__ + "." + self.pull_trigger.__name__,
            args=(db_result_id, topic_id, device_collection_id + "." + device3_name, device3_pass)
        )
        th_1.start()
        th_2.start()
        th_3.start()
        th_1.join()
        th_2.join()
        th_3.join()
        self.user.delete("/apps/{}".format(app_id))
        self.user.delete("/deviceCollections/{}".format(device_collection_id))
        if(self.error_queue.empty()):
            ok(SCENARIO_NAME)
        else:
            while not self.error_queue.empty():
                ng(SCENARIO_NAME, self.error_queue.get())
        
    @process("アプリ作成")
    def create_app(self, req_app):
        res = self.user.post("/apps", body=json.dumps(req_app))
        if not res.status_code == 201:
            raise Exception("アプリの作成に失敗しました")
        return res
    
    @process("DB作成")
    def create_db(self, req_db_device, req_db_result, app_id):
        res_db_device = self.user.post("/dbs", body=json.dumps(req_db_device))
        res_db_result = self.user.post("/dbs", body=json.dumps(req_db_result))
        if not res_db_device.status_code == 201 and res_db_device.status_code == 201:
            raise Exception("DBの作成に失敗しました")
        return (res_db_device, res_db_result)
    
    @process("デバイスコレクション作成")
    def create_device_collection(self, req_devicecollction):
        res = self.user.post("/deviceCollections", body=json.dumps(req_devicecollction))
        if not res.status_code == 201:
            raise Exception("デバイスコレクションの作成に失敗しました")
        return res
    
    @process("デバイス作成")
    def create_device(self, req_device1, req_device2, req_device3, device_collection_id):
        res_device1 = self.user.post("/deviceCollections/{}/devices".format(device_collection_id), body=json.dumps(req_device1))
        res_device2 = self.user.post("/deviceCollections/{}/devices".format(device_collection_id), body=json.dumps(req_device2))
        res_device3 = self.user.post("/deviceCollections/{}/devices".format(device_collection_id), body=json.dumps(req_device3))
        if not res_device1.status_code == 201:
            raise Exception("デバイスの追加に失敗しました")
        return (res_device1, res_device2, res_device3)
    
    @process("トピック作成")
    def create_topic(self, req_topic):
        res = self.user.post("/mqttTopics", body=json.dumps(req_topic))
        if not res.status_code == 201:
            raise Exception("トピックの作成に失敗しました")
        return res
    
    @process("ストリーム作成")
    def create_stream(self, req_stream):
        res = self.user.post("/streamAggregations", body=json.dumps(req_stream))
        if not res.status_code == 201:
            raise Exception("ストリームの作成に失敗しました")
        return res
    
    @process("トリガ作成")
    def create_trigger(self, req_trigger, stream_id):
        res = self.user.post("/streamAggregations/{}/triggers".format(stream_id), body=json.dumps(req_trigger))
        if not res.status_code == 201:
            raise Exception("トリガの作成に失敗しました")
        return res
    
    @process("ユーザからMQTT Publish->デバイスで受信確認")
    def publish_from_user(self, topic_id, device_username, device_password):
        TRANSMISSION_COUNT = 10
        TRANSMISSION_MESSAGE = '{"value":"publish_from_user"}'
        self.device1.connect(device_username, device_password)
        self.device1.subscribe(topic_id)
        for i in range(0, TRANSMISSION_COUNT):
            self.user.post("/mqttTopics/{}/publish".format(topic_id), body=TRANSMISSION_MESSAGE)
        sleep(1)
        self.device1.unsubscribe(topic_id)
        self.device1.disconnect()
        self.logger.debug("{} transmitted, {} received".format(TRANSMISSION_COUNT, self.device1.messages.count(TRANSMISSION_MESSAGE)))
        if not self.device1.messages or not TRANSMISSION_MESSAGE in self.device1.messages:
            self.error_queue.put(Exception("ユーザからMQTT Publish->デバイスで受信確認に失敗しました"))
    
    @process("デバイスからMQTT Publish->集計確認")
    def publish_from_device(self, db_result_id, topic_id, device_username, device_password):
        self.device2.connect(device_username, device_password)
        for i in range(0, self.TRANSMISSION_COUNT):
            self.device2.publish(topic_id, json.dumps({"measureKey": 0}))
        sleep(self.AGGREGATION_INTERVAL)
        waiting = 0
        while not self.user.get("/dbs/{}/records?where=@newField4='2'".format(db_result_id)).json().get("totalCount"):
            if self.MAX_LATENCY > self.AGGREGATION_INTERVAL + waiting:
                waiting += 1
                sleep(1)
            else:
                self.error_queue.put(Exception("デバイスからMQTT Publish->集計確認に失敗しました"))
                break
        self.device2.disconnect()
        res = self.user.get("/dbs/{}/records?where=@newField4='2'".format(db_result_id))
        self.logger.debug("{} transmitted, {} aggregated".format(
                self.TRANSMISSION_COUNT,
                reduce(lambda x, y: x + y, [0] + [int(x.get("newField5")) for x in res.json().get("items")])
        ))
        if waiting > 0:
            self.logger.warning("delay {} seconds".format(waiting))
        if res.json().get("totalCount") == 0:
            self.error_queue.put(Exception("デバイスからの集計データの登録に失敗しました"))
    
    @process("トリガからMQTT Publish->デバイスで受信確認")
    def pull_trigger(self, db_result_id, topic_id, device_username, device_password):
        TRANSMISSION_MESSAGE = '{"value":"publish_from_device"}'
        self.device3.connect(device_username, device_password)
        self.device3.subscribe(topic_id)
        for i in range(0, self.TRANSMISSION_COUNT):
            self.device3.publish(topic_id, json.dumps({"measureKey": 1}))
        sleep(self.AGGREGATION_INTERVAL)
        waiting = 0
        while not self.user.get("/dbs/{}/records?where=@newField4='3'".format(db_result_id)).json().get("totalCount"):
            if self.MAX_LATENCY > self.AGGREGATION_INTERVAL + waiting:
                waiting += 1
                sleep(1)
            else:
                self.error_queue.put(Exception("トリガからのMQTTメッセージの受信に失敗しました"))
                break
        self.device3.unsubscribe(topic_id)
        self.device3.disconnect()
        res = self.user.get("/dbs/{}/records?where=@newField4='3'".format(db_result_id))
        self.logger.debug("{} registered, {} received".format(
            res.json().get("totalCount"),
            self.device3.messages.count(TRANSMISSION_MESSAGE)
        ))
        if waiting > 0:
            self.logger.warning("delay {} seconds".format(waiting))
        if not self.device3.messages or not TRANSMISSION_MESSAGE in self.device3.messages:
            self.error_queue.put(Exception("トリガからMQTT Publish->デバイスで受信確認に失敗しました"))
    
