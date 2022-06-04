import csv
import os

class csvGenerator:
    writer = None
    header = None

    def __init__(self, path="csv_report", fileName="csvReport", header=["ID", "TestName", "API Route","Method", "Request Payload", "Status Code", "Response Payload", 'Response Time','Test Result','Remark']):
        self.header = header
        self.path = path
        self.fileName = fileName
        isExist = os.path.exists("./"+path)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(path)
            print("The new directory is created!")
        with open(f'{self.path}/{self.fileName}.csv', 'w+', encoding='UTF8', newline='') as f:
            self.writer = csv.writer(f)
            self.writer.writerow(self.header)

    def write_content(self, content=None):
        with open(f'{self.path}/{self.fileName}.csv', 'a+', encoding='utf8', newline='') as f:
            self.writer = csv.writer(f)
            self.writer.writerow(content)