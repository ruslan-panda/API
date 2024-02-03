import os
import sys

import requests
import keyboard
from multiprocessing import Process
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


scale = 12
class BigMap(QWidget):
    def __init__(self):
        super().__init__()
        global scale
        try:
            self.lon = sys.argv[1]
            self.lat = sys.argv[2]
            self.scale = int(sys.argv[3])
        except IndexError:
            self.lon = "39.573954"
            self.lat = "52.621706"
            self.scale = scale
        self.getImage()
        self.initUI()

    def getImage(self):
        api_server = "http://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{self.lon},{self.lat}",
            "z": self.scale,
            "l": "map"
        }
        response = requests.get(api_server, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit()

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


def par():
    global scale
    while True:
        if keyboard.is_pressed("up"):
            scale += 1
            print(scale)
            ex = BigMap()
            ex.show()
            keyboard.record("up")


if __name__ == '__main__':
    Process(target=par).start()
    app = QApplication(sys.argv)
    ex = BigMap()
    ex.show()
    sys.exit(app.exec())
