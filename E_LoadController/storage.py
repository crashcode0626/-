import csv
from datetime import datetime
import os


class DataLogger:
    def __init__(self):
        self.filename = None
        self.file = None
        self.writer = None
        self.header_written = False
        self.last_record_time = None

    def _generate_filename(self):
        return datetime.now().strftime("%Y%m%d%H%M%S") + "_EL_data.csv"

    def start_logging(self):
        if not self.filename:
            self.filename = self._generate_filename()
            self.file = open(self.filename, 'a', newline='')
            self.writer = csv.writer(self.file)

    def log_data(self, data):
        if not self.file:
            self.start_logging()

        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        row = [
            data['switch_status']['value'],
            data['voltage']['value'],
            data['current']['value'],
            data['time']['value'],
            data['AH']['value'],
            data['WH']['value'],
            data['temperature']['value'],
            data['stop_voltage']['value'],
            data['timer']['value'],
            timestamp
        ]

        # 写入表头
        if not self.header_written:
            headers = [
                "switch_status", "voltage(V)", "current(A)", "time(s)",
                "AH", "WH", "temperature(°C)", "stop_voltage(V)",
                "timer(s)", "TimeStamp"
            ]
            self.writer.writerow(headers)
            self.header_written = True

        self.writer.writerow(row)
        self.last_record_time = datetime.now()

    def stop_logging(self):
        if self.file:
            # 使用最后记录时间重命名文件
            if self.last_record_time:
                new_filename = self.last_record_time.strftime("%Y%m%d%H%M%S") + "_EL_data.csv"
                os.rename(self.filename, new_filename)
            self.file.close()