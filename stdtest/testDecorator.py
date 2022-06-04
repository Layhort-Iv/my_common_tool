from requests import models
from stdtest.display import check, ok, ng, show_failTest, log_print

def convert_res_to_csv_format(res):
    return [f'{res.request.path_url}', f'{res.request.method}', f'{bytes(res.request.body, "utf-8").decode("unicode_escape")}' if res.request.body else None,
                            f'{res.status_code}', f'{res.json()}', "{:.2f} ms".format(res.elapsed.total_seconds() * 1000)]

class testDecorator():
    
    def __init__(self, SCENARIO_NAME):
        self.SCENARIO_NAME = SCENARIO_NAME
        self.totalTests = 0
        self.totalFails = 0
        self.currentTest = ""
        self.currentTestResult = []
        self.failedTests = {}
        self.finishedTests = {}

    def put_testResult(self, res=[]):
        if isinstance(res, models.Response):
            try:
                self.currentTestResult.extend(
                [f'{res.request.path_url}', f'{res.request.method}',
                 f'{bytes(res.request.body, "utf-8").decode("unicode_escape")}' if res.request.body else None,
                 f'{res.status_code}', f'{res.json() if res.status_code != 204 else ""}',
                 "{:.2f} ms".format(res.elapsed.total_seconds() * 1000)])
            except Exception as e:
                self.currentTestResult.extend(
                [f'{res.request.path_url}', f'{res.request.method}',
                 f'{bytes(res.request.body, "utf-8").decode("unicode_escape")}' if res.request.body else None,
                 f'{res.status_code}', f'{res.text if res.status_code != 204 else ""}',
                 "{:.2f} ms".format(res.elapsed.total_seconds() * 1000)])
        else:
            self.currentTestResult.extend(res)

    def test_failed(self, e=None):
        e = str(e).split("|")
        self.totalFails += 1
        try:
            self.failedTests.update({self.currentTest: e[1]})
            ng(self.currentTest, e[0] + "\n" if e[0] else "Test Failed \n")
        except:
            self.put_testResult(["", "", "", "", "", ""])
            self.failedTests.update({self.currentTest: e[0]})
            ng(self.currentTest, e[0] if e is not None else "Test Failed \n")
        self.currentTestResult.append('NG')
        self.currentTestResult.append(e[0])

        self.writer.write_content(self.currentTestResult)

    def test_passed(self, res=None):
        self.put_testResult(res)
        self.currentTestResult.append('OK')
        self.currentTestResult.append('No Remark')
        self.writer.write_content(self.currentTestResult)
        ok(self.currentTest, "Test Success")

    def start_test(self, test_name, message=None):
        self.currentTestResult = []
        self.currentTest = test_name
        self.totalTests += 1
        self.currentTestResult.extend([f'{self.totalTests}', f'{self.currentTest}'])
        check(self.currentTest, "" if message is None else message)