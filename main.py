
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
        self.setWindowTitle("DASHBOARD")
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


        label_color_map = {
        "Low_Risk": QColor(255, 240, 133),
        "Medium_Risk": QColor(255, 214, 10),
        "Error": QColor(250, 129, 47),
        "High_Risk": QColor(241, 103, 103),
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
        with open("final_ftp_log.json", "r") as f:
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
        self.set_dummy_data()

        self.set_ftp_table()
        self.ied_data()

    
    def set_colors_ied_1(self):
        row_colors = [
            QColor(202, 240, 248), # light blue
        QColor(144, 224, 239),  
        QColor(0, 180, 216),  # darker yellow
        ]

        for row in range(self.table1.rowCount() + 1):
            color = row_colors[row % len(row_colors)]
            for col in range(self.table1.columnCount()):
                item = self.table1.item(row, col)
                if item:
                    item.setBackground(color)



    def set_colors_ied_2(self):
        row_colors = [
            QColor(236, 250, 229), # pista green
        QColor(221, 246, 210),  
        QColor(202, 232, 189),  # military green
        ]

        for row in range(self.table1.rowCount() + 1):
            color = row_colors[row % len(row_colors)]
            for col in range(self.table2.columnCount()):
                item = self.table2.item(row, col)
                if item:
                    item.setBackground(color)


    def set_colors_ftp_table(self):
        row_colors = [
        QColor(220, 255, 220),  
        QColor(255, 255, 200),  
        QColor(255, 220, 180),  
        QColor(255, 200, 200),  
        QColor(200, 220, 255),  
        ]

        for row in range(self.table1.rowCount()):
            color = row_colors[row % len(row_colors)]
            for col in range(self.table1.columnCount()):
                item = self.table1.item(row, col)
                if item:
                    item.setBackground(color)


    def set_ftp_table(self):
            # Load logs from JSON file
        logs = []
        with open("final_ftp_log.json", "r") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    if isinstance(data, list):
                        logs.extend(data)  # flatten the list
                    elif isinstance(data, dict):
                        logs.append(data)


        level_color_map = {
        "Low_Risk": QColor(255, 240, 133, 150),
        "Medium_Risk": QColor(255, 214, 10, 150),
        "Error": QColor(250, 129, 47, 150),
        "High_Risk": QColor(241, 103, 103, 150),
        }

        



        # Sort logs by timestamp (latest first)
        logs_sorted = sorted(logs, key=lambda x: x.get("timestamp", ""), reverse=True)

        # Pick latest 4 logs
        self.latest_logs_ftp = logs_sorted[:4]

        for row, log in enumerate(self.latest_logs_ftp):
            self.ftp.setItem(row, 0, QTableWidgetItem(log.get("timestamp", "")))
            self.ftp.setItem(row, 1, QTableWidgetItem(log.get("level", "")))
            self.ftp.setItem(row, 2, QTableWidgetItem(log.get("message", "")))
            self.ftp.setItem(row, 3, QTableWidgetItem(str(log.get("Attacker IP", ""))))
            self.ftp.setItem(row, 4, QTableWidgetItem(str(log.get("Attacker Port", ""))))

            # Set background color based on level
            level = log.get("level", "UNKNOWN")
            row_color = level_color_map.get(level, QColor(240, 240, 240))  # fallback color
            for col in range(self.ftp.columnCount()):
                item = self.ftp.item(row, col)
                if item:
                    item.setBackground(row_color)




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


        for row, entry in enumerate(self.latest_per_level.values()):
            self.table1.setItem(row, 0, QTableWidgetItem(entry.get("timestamp", "")))
            self.table1.setItem(row, 1, QTableWidgetItem(entry.get("goose-type", "")))
            self.table1.setItem(row, 2, QTableWidgetItem(entry.get("message", "")))

            self.table2.setItem(row, 0, QTableWidgetItem(entry.get("timestamp", "")))
            self.table2.setItem(row, 1, QTableWidgetItem(entry.get("goose-type", "")))
            self.table2.setItem(row, 2, QTableWidgetItem(entry.get("message", "")))
        
        self.set_colors_ied_1()
        self.set_colors_ied_2()

    def set_dummy_data(self):
         # Add 3 rows of example data
        data = [
            ("10:01 AM", "INFO", "Startup complete"),
            ("10:05 AM", "WARNING", "Voltage spike detected"),
            ("10:10 AM", "other", "Connection lost")
        ]

        for row_index, (time, type_, message) in enumerate(data):
            self.table1.setItem(row_index, 0, QTableWidgetItem(time))
            self.table1.setItem(row_index, 1, QTableWidgetItem(type_))
            self.table1.setItem(row_index, 2, QTableWidgetItem(message))

            self.table2.setItem(row_index, 0, QTableWidgetItem(time))
            self.table2.setItem(row_index, 1, QTableWidgetItem(type_))
            self.table2.setItem(row_index, 2, QTableWidgetItem(message))

    def handle_row_selection1(self):
        selected_indexes = self.table1.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()
            
        message = self.table2.item(row, 1).text()

        self.ied_json_display.setText(f"{self.latest_per_level[message]}")
        self.ied_json_display.setStyleSheet("background-color:white; color:blue;")


    def handle_row_selection2(self):
        selected_indexes = self.table2.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()


        message = self.table2.item(row, 1).text()

        self.ied_json_display.setText(f"{self.latest_per_level[message]}")
        self.ied_json_display.setStyleSheet("background-color:white; color:green;")

        
   


    def handle_row_selection3(self):
        selected_indexes = self.ftp.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()
        self.display_json3(row)

    def display_json3(self, row):
        self.ied_json_display.setText(f"{self.latest_logs_ftp[row-1]}")
        self.ied_json_display.setStyleSheet("background-color:white; color:#8D0B41;")


########### main function ###########
app=QApplication(sys.argv)
window = main_window("main")
app.exec_()

