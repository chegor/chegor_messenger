from datetime import datetime

import requests
from PyQt5 import QtWidgets, QtCore

from pyuiclient import Ui_MainWindow


class Messenger(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, url):
        super().__init__()
        self.setupUi(self)

        self.url = url
        self.after_timestamp = -1

        self.sendButton.pressed.connect(self.button_pressed)

        self.load_messages()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_messages)
        self.timer.start(1000)

    def pretty_print(self, message):
        dt = datetime.fromtimestamp(message['timestamp'])
        dt = dt.strftime('%Y/%m/%d %H:%M:%S')
        first_line = dt + ' ' + message['name']
        self.textBrowser.append(first_line)
        self.textBrowser.append(message['text'])
        self.textBrowser.append('')
        #self.textBrowser.repaint()

    def update_messages(self):
        response = None
        try:
            response = requests.get(
                self.url + '/messages',
                params={'after_timestamp': self.after_timestamp}
                )
        except:
            pass

        if response and response.status_code == 200:
            messages = response.json()['messages']
            for message in messages:
                self.pretty_print(message)
                self.after_timestamp = message['timestamp']

            return messages


    def load_messages(self):
        while self.update_messages():
            pass

    def button_pressed(self):
        text = self.inputText.toPlainText()
        name = self.inputName.text()
        data = {'name': name, 'text': text}

        response = None
        try:
            response = requests.post(self.url + '/send', json=data)
        except:
            pass

        if response and response.status_code == 200:
            self.inputText.clear()
            #self.textBrowser.repaint()
        else:
            self.textBrowser.append('Error during sending')
            self.textBrowser.append('')
            #self.textBrowser.repaint()


app = QtWidgets.QApplication([])
window = Messenger('http://127.0.0.1:5000')
window.show()
app.exec_()