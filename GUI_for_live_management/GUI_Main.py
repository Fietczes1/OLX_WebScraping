import sys
import timeit

from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QTimer, QObject

# class SignalHandler(QObject):
#     update_signal = pyqtSignal(str)

class App(QWidget):
    def __init__(self, update_queue):
        super().__init__()
        self.update_queue = update_queue
        self.initUI()
        self.oldlist = []

    def initUI(self):
        try:
            layout = QVBoxLayout(self)
            self.table_widget = QTableWidget()
            layout.addWidget(self.table_widget)


            self.setGeometry(300, 100, 800, 300)
            self.setWindowTitle('Dynamic QTableWidget Example')
            QTimer.singleShot(100, self.check_queue)
            print("Initialization successful.")
        except Exception as e:
            print("Failed during initialization:", e)

            # # Setup the signal handler for updating the table
            # self.signal_handler = SignalHandler()
            # self.signal_handler.update_signal.connect(self.update_data)


    #Unlock as well signal handler Above
    # def simulate_external_data_load(self):
    #     print("Simulating data load.")
    #     self.signal_handler.update_signal.emit([
    #         {'Ads_id': '897306208', 'Area': 50, 'Location': 'Suburb', 'Price': '750000',
    #          'Price_per_meter2': 15000, 'Title': 'Spacious suburban house', 'URL': 'http://examplehouse.com', 'Validity': '2025'}
    #     ])

    def update_data(self, new_data):
        """ Update the table with new data """
        self.table_widget.setRowCount(len(new_data))
        if new_data:
            self.table_widget.setColumnCount(len(new_data[0]))
            self.table_widget.setHorizontalHeaderLabels(new_data[0].keys())

        for row, item in enumerate(new_data):
            for col, key in enumerate(item):
                value = str(item[key])  # Convert values to strings for display
                self.table_widget.setItem(row, col, QTableWidgetItem(value))

    def check_queue(self):
        #print(self.update_queue.get_nowait())
        if self.update_queue:
            Queue_at_function_start = self.update_queue.empty()

            while not self.update_queue.empty():
                try:
                    # Try to get data from the queue
                    data = self.update_queue.get_nowait()
                    print(data)
                    #data.pop('lefted_elements')
                    self.oldlist.append(data) if type(data) == dict else self.oldlist.extend(data)
                    #print(self.oldlist)

                    # if data:
                    #     self.signal_handler.update_signal.emit(data)
                except:
                    pass
            if not Queue_at_function_start:
                self.update_data(self.oldlist)

            # Re-check the queue after a short delay
            QTimer.singleShot(20, self.check_queue)

def main(update_queue):
    app = QApplication(sys.argv)
    ex = App(update_queue)
    ex.show()
    sys.exit(app.exec_())
