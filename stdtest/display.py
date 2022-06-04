from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[1;96m'
    OKGREEN = '\033[1;92m'
    WARNING = '\033[93m'
    FAIL = '\033[1;91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

now = datetime.now()
current_datetime = f"{now.date()} {now.hour}h-{now.minute}m-{now.second}s"


def check(scenario_name, message=""):
    print("\n{}[{:^7s} ] {:8s}: {}{}".format(bcolors.HEADER, "CHECK", scenario_name, message, bcolors.ENDC))


def ok(scenario_name, message=""):
    print("{}[{:^8s}] {:8s}: {}{}".format(bcolors.OKGREEN, "OK", scenario_name, message, bcolors.ENDC))


def ng(scenario_name, message=""):
    print("{}[{:^8s}] {:8s}: {}{}".format(bcolors.FAIL, "NG", scenario_name, message, bcolors.ENDC))

def show_failTest(failTest={}):
    print("{}==Failed Test Cases=={}".format(bcolors.FAIL, bcolors.ENDC))
    print('\n'.join('{}- {}: {}'.format(i + 1, k, v) for i, (k, v) in enumerate(failTest.items())))
    print("{}====================={}".format(bcolors.FAIL, bcolors.ENDC))


def log_print(scenario_name, message=""):
    print("[{:^7s} ] {:8s}: {}{}{}".format("PRINT", scenario_name, bcolors.UNDERLINE, message, bcolors.ENDC))

def start_test(scenario_name, message=""):
    print("{}[{:^12s}] {:8s}: {} - {}{}".format(bcolors.OKCYAN, "START TEST", scenario_name, message, current_datetime, bcolors.ENDC))

def end_test(scenario_name, message="Finished at"):
    print("{}[{:^16s}] {:8s}: {} - {}{}\n".format(bcolors.OKCYAN, "TEST COMPLETED", scenario_name, message, current_datetime, bcolors.ENDC))