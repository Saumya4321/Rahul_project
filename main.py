
from PyQt5.QtWidgets import QMainWindow,QApplication, QLabel, QTableWidget
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import json
from collections import Counter
from PyQt5.QtGui import QColor
from collections import OrderedDict
from datetime import datetime




class main_window(QMainWindow):
    def __init__(self, main):
        super(main_window,self).__init__()
        uic.loadUi("ftp.ui",self)
        self.main = main
        self.init_default()
        self.init_ui_elements()
        self.init_pie_content()
        self.init_chart()
   

        self.show()

    def init_default(self):
        self.log_name = []
        self.size_log = []
        self.latest_per_level = OrderedDict()

    def init_chart(self):
        # Access placeholder widget by object name
        self.chart_container = self.findChild(QtWidgets.QWidget, "chartWidget")

        # print("log_name:", self.log_name)
        # print("size_log:", self.size_log)

                # # Define the mapping of labels to colors
        # label_color_map = {
        #     "low-risk": QColor("white"),
        #     "medium-risk": QColor("yellow"),
        #     "error": QColor("orange"),
        #     "high-risk": QColor("red"),
        # }

        label_color_map = {
            "DEBUG": QColor(255, 155, 23),
            "INFO": QColor(255, 240, 133),
            "ERROR": QColor("orange"),
            "CRITICAL": QColor(241, 103, 103),
        }



        # Create pie chart
        series = QPieSeries()

        for i in range(len(self.log_name)):
            slice = series.append(self.log_name[i], self.size_log[i])
            label = self.log_name[i]
            # print(label)
            if label in label_color_map:
                slice.setBrush(label_color_map[label])

            slice.setLabelVisible(True)



        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Log Distribution")
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        # Replace chart_widget with chart_view
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(chart_view)
        self.chart_container.setLayout(layout)
        chart_view.setMinimumSize(350, 350)  # Try bigger values like 500x500


        series.setPieSize(1)  # Default is 0.7; max is 1.0

     

    def init_pie_content(self):
        with open("log_ftp_chart.json", "r") as f:
            log_entries = [json.loads(line) for line in f if line.strip()]


        labels = []

        for i in log_entries[0]:
            labels.append(i['level'])

        
        level_counts = Counter(labels)

        # # Step 4: Plot pie chart
        labels_new = list(level_counts.keys())
        sizes_new = list(level_counts.values())

        self.log_name = labels_new
        self.size_log = sizes_new




      
    def init_ui_elements(self):

        # Access the table widget
        self.table1 = self.findChild(QTableWidget, "ied1")
        self.table2 = self.findChild(QTableWidget, "ied2")
        self.ftp = self.findChild(QTableWidget, "ftp")

        self.table1.setColumnWidth(0, 120)  # Time Stamp
        self.table1.setColumnWidth(1, 80)   # Type
        self.table1.setColumnWidth(2, 263)  # Message (wider)

        # Stretch message column
        row_height = 25
        header_height = self.table1.horizontalHeader().height()
        total_height = row_height * (self.table1.rowCount() + 1) + header_height + 1  # +2 for border maybe

        self.table1.setFixedHeight(total_height)


        self.table2.setColumnWidth(0, 120)  # Time Stamp
        self.table2.setColumnWidth(1, 80)   # Type
        self.table2.setColumnWidth(2, 263)  # Message (wider)

        # Stretch message column
        row_height = 25
        header_height = self.table2.horizontalHeader().height()
        total_height = row_height * (self.table2.rowCount() + 1) + header_height + 1  # +2 for border maybe

        self.table2.setFixedHeight(total_height)

        self.ftp.setColumnWidth(0, 180)  # Time Stamp
        self.ftp.setColumnWidth(1, 80)   # Type
        self.ftp.setColumnWidth(2, 263)  # Message (wider)
        self.ftp.setColumnWidth(3, 80)
        self.ftp.setColumnWidth(4, 85)  

        # Stretch message column
        row_height = 25
        header_height = self.ftp.horizontalHeader().height()
        total_height = row_height * (self.ftp.rowCount() + 1) + header_height + 1  # +2 for border maybe

        self.ftp.setFixedHeight(total_height)


        # Select entire rows instead of individual cells
        self.table1.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ftp.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        # Optional: Allow only single row selection at a time
        self.table1.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ftp.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # Connect selection change to handler
        self.table1.itemSelectionChanged.connect(self.handle_row_selection1)
        self.table2.itemSelectionChanged.connect(self.handle_row_selection2)
        self.ftp.itemSelectionChanged.connect(self.handle_row_selection3)

        self.ied_json_display = self.findChild(QLabel,"ied_json_display")

        self.set_ftp_table()
        self.ied_data()

    

    def set_ftp_table(self):
            # Load logs from JSON file
        logs = []
        with open("log_ftp_table.json", "r") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if isinstance(data, list):
                        logs.extend(data)  # flatten the list
                    elif isinstance(data, dict):
                        logs.append(data)


        # Sort logs by timestamp (latest first)
        logs_sorted = sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)

        # Pick latest 4 logs
        self.latest_logs_ftp = logs_sorted[:4]

        for row, log in enumerate(self.latest_logs_ftp):
            self.ftp.setItem(row, 0, QTableWidgetItem(log.get("timestamp", "")))
            self.ftp.setItem(row, 1, QTableWidgetItem(log.get("Protocol", "")))
            self.ftp.setItem(row, 2, QTableWidgetItem(log.get("message", "")))
            self.ftp.setItem(row, 3, QTableWidgetItem(str(log.get("Attacker IP", ""))))
            self.ftp.setItem(row, 4, QTableWidgetItem(str(log.get("Attacker Port", ""))))


    def ied_data(self):
        logs = []
        with open("ied_log.json", "r") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if isinstance(data, list):
                        logs.extend(data)  # flatten the list
                    elif isinstance(data, dict):
                        logs.append(data)


        # Parse and sort logs by timestamp (newest first)
        def parse_time(entry):
            try:
                return datetime.fromisoformat(entry.get("timestamp", ""))
            except ValueError:
                return datetime.min

        logs_sorted = sorted(logs, key=parse_time, reverse=True)

        # Track seen levels and keep only the first (latest) entry per level
        
        for entry in logs_sorted:
            level = entry.get("goose-type", "UNKNOWN")
            if level not in self.latest_per_level:
                self.latest_per_level[level] = entry

        print(self.latest_per_level)

        for row, entry in enumerate(self.latest_per_level.values()):
            self.table1.setItem(row, 0, QTableWidgetItem(entry.get("timestamp", "")))
            self.table1.setItem(row, 1, QTableWidgetItem(entry.get("goose-type", "")))
            self.table1.setItem(row, 2, QTableWidgetItem(entry.get("message", "")))

            self.table2.setItem(row, 0, QTableWidgetItem(entry.get("timestamp", "")))
            self.table2.setItem(row, 1, QTableWidgetItem(entry.get("goose-type", "")))
            self.table2.setItem(row, 2, QTableWidgetItem(entry.get("message", "")))


    def handle_row_selection1(self):
        selected_indexes = self.table1.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()
            print(row)

        print(f"Selected Row {row + 1}:")
        message = self.table2.item(row, 1).text()

        self.ied_json_display.setText(f"{self.latest_per_level[message]}")
        self.ied_json_display.setStyleSheet("background-color:white; color:blue;")


    def handle_row_selection2(self):
        selected_indexes = self.table2.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()
            print(row)

        print(f"Selected Row {row + 1}:")
        message = self.table2.item(row, 1).text()

        self.ied_json_display.setText(f"{self.latest_per_level[message]}")
        self.ied_json_display.setStyleSheet("background-color:white; color:green;")

        
   


    def handle_row_selection3(self):
        selected_indexes = self.ftp.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()
            print(row)
        self.display_json3(row)

    def display_json3(self, row):
        self.ied_json_display.setText(f"{self.latest_logs_ftp[row-1]}")
        self.ied_json_display.setStyleSheet("background-color:white; color:orange;")


########### main function ###########
app=QApplication(sys.argv)
window = main_window("main")
app.exec_()

