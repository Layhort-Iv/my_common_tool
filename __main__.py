import json
import time
from pathlib import Path
from requests import api
import yaml
import sys
import logging.config
from argparse import ArgumentParser, RawTextHelpFormatter
from _collections import OrderedDict
import scenario
from scenario import *
from stdtest import scenario_map, injection_map
from stdtest.User import User
from stdtest.Option import Option
from stdtest.System import System
# from stdtest.Device import Device
from threading import Thread
import requests

yaml.add_representer(OrderedDict,lambda dumper, instance: dumper.represent_mapping('tag:yaml.org,2002:map', instance.items()))
yaml.add_constructor('tag:yaml.org,2002:map', lambda loader, node: OrderedDict(loader.construct_pairs(node)))

config_dir = Path("config")
with (config_dir/"environment.yml").open(encoding="utf-8") as file:
    conf_env = yaml.safe_load(file)
with (config_dir/"logger.yml").open(encoding="utf-8") as file:
    conf_logger = yaml.safe_load(file)
scenario_name_description = {
    v["scenario"]["name"]: {"description": v["scenario"]["description"], "process" : v["process"]}
    for v in scenario_map.values()
}

scenario_name_classname = {
    v["scenario"]["name"]: k
    for k, v in scenario_map.items()
}

parser = ArgumentParser(description="Standard Test", formatter_class=RawTextHelpFormatter)
parser.add_argument("-e", "--environment",
    choices=conf_env.keys(),
    required=True,
    help=yaml.dump(conf_env, default_flow_style=False, allow_unicode=True)
)
parser.add_argument("-s", "--scenario",
    choices=["all"] + list(scenario_name_classname.keys()),
    required=True,
    nargs="+",
    help=yaml.dump({
            **{"all": {"description": "全てのシナリオを実行します"}},
            **dict(scenario_name_description.items())
        }, default_flow_style=False, allow_unicode=True)
)
parser.add_argument("-l", "--log",
    choices= ["debug", "info", "warning", "error", "critical"],
    help="コンソールログの出力設定。指定しない場合はlogger.ymlの規定値を取ります"
)
parser.add_argument("-o", "--option",
    choices=["sync"],
    nargs="+",
    help=yaml.dump({
        "sync": "選択されたシナリオを同期処理します。出力されるログの可読性が上がりますが、終了まで時間がかかります"
    }, default_flow_style=False, allow_unicode=True)
)
cmd_args = parser.parse_args()




http_host = conf_env[cmd_args.environment]["http_host"]
http_port = conf_env[cmd_args.environment]["http_port"]
# mqtt_host = conf_env[cmd_args.environment]["mqtt_host"]
# mqtt_port = conf_env[cmd_args.environment]["mqtt_port"]
sys_api_key = conf_env[cmd_args.environment]["sys_api_key"]
certificate = conf_env[cmd_args.environment]["certificate"]
if "all" in cmd_args.scenario:
    selected_scenario = list(scenario_name_classname.keys())
else:
    selected_scenario = sorted(set(cmd_args.scenario), key=cmd_args.scenario.index)
if cmd_args.log:
    conf_logger["handlers"]["console"]["level"] = cmd_args.log.upper()

##GET PRIVATE APIs 
if (not conf_env[cmd_args.environment]["api_key"]):
    headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                "X-Spiral-Api-Version":"1.1"
            }
    try:
        res = requests.post(
                url=http_host + "/oauth2/token",
                headers=headers,
                data=conf_env[cmd_args.environment]["oauth_setting"],
                verify=conf_env[cmd_args.environment]["certificate"],
                timeout = 10
            )
        if (not res.status_code==200):
            raise Exception("Couldn't Retrived Private_API - Received GET {} {} With Body {}".format(res.status_code, http_host + "/oauth2/token", res._content))
    except Exception as e:
        print(e)
        sys.exit(0)
    conf_env[cmd_args.environment]["api_key"] = res.json().get('access_token')
api_key = conf_env[cmd_args.environment]["api_key"]


logging.config.dictConfig(conf_logger)
injection_map[User] = lambda: User(http_host, http_port, api_key, sys_api_key, certificate)
injection_map[Option] = lambda: Option(conf_env[cmd_args.environment]["mailDomainId"])
injection_map[System] = lambda: System(http_host, http_port, api_key, certificate)
# injection_map[Device] = lambda: Device(mqtt_host, mqtt_port, certificate)

try:
    option = cmd_args.option[0]
except:
    option = ''

Init.Init().start()
for scenario_name in selected_scenario:
    if "NO" in scenario_name:
        continue
    class_name = scenario_name_classname[scenario_name]
    instance = getattr(getattr(scenario, class_name), class_name)()
    instance.start()
    if isinstance(instance, Thread) and option == "sync":
        time.sleep(2)
        instance.join()


