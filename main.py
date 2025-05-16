
from PyQt5.QtWidgets import QMainWindow,QApplication, QLabel, QTableWidget
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import sys



class main_window(QMainWindow):
    def __init__(self, main):
        super(main_window,self).__init__()
        uic.loadUi("ftp.ui",self)
        self.main = main

        self.init_ui_elements()
   

        self.show()

      
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

        self.ftp.setColumnWidth(0, 120)  # Time Stamp
        self.ftp.setColumnWidth(1, 80)   # Type
        self.ftp.setColumnWidth(2, 263)  # Message (wider)
        self.ftp.setColumnWidth(3, 80)
        self.ftp.setColumnWidth(4, 85)  

        # Stretch message column
        row_height = 25
        header_height = self.ftp.horizontalHeader().height()
        total_height = row_height * (self.ftp.rowCount() + 1) + header_height + 1  # +2 for border maybe

        self.ftp.setFixedHeight(total_height)

        self.set_dummy_data()

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

    
    def set_dummy_data(self):
         # Add 3 rows of example data
        data = [
            ("10:01 AM", "INFO", "Startup complete"),
            ("10:05 AM", "WARNING", "Voltage spike detected"),
            ("10:10 AM", "ERROR", "Connection lost")
        ]

        for row_index, (time, type_, message) in enumerate(data):
            self.table1.setItem(row_index, 0, QTableWidgetItem(time))
            self.table1.setItem(row_index, 1, QTableWidgetItem(type_))
            self.table1.setItem(row_index, 2, QTableWidgetItem(message))
    


    def handle_row_selection1(self):
        selected_indexes = self.table1.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()
            print(row)

        print(f"Selected Row {row + 1}:")
   

        # Do something with this row's data
        self.display_json1(row)

    def display_json1(self, row):
        self.ied_json_display.setText(f"Showing Table 1, row {row} json data")
        self.ied_json_display.setStyleSheet("background-color:white; color:blue;")

    def display_json2(self, row):
        self.ied_json_display.setText(f"Showing Table 2, row {row} json data")
        self.ied_json_display.setStyleSheet("background-color:white; color:green;")



    def handle_row_selection2(self):
        selected_indexes = self.table2.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()
            print(row)

        print(f"Selected Row {row + 1}:")
   

        # Do something with this row's data
        self.display_json2(row)

    def handle_row_selection3(self):
        selected_indexes = self.ftp.selectionModel().selectedRows()
    
        if selected_indexes:
            row = selected_indexes[0].row()
            print(row)

        print(f"Selected Row {row + 1}:")
   

        # Do something with this row's data
        self.display_json3(row)

    def display_json3(self, row):
        self.ied_json_display.setText(f"Showing Table 3, row {row} json data")
        self.ied_json_display.setStyleSheet("background-color:white; color:orange;")


########### main function ###########
app=QApplication(sys.argv)
window = main_window("main")
app.exec_()

