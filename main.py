import os
import sys

import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class BigMap(QWidget):
    def __init__(self):
        super().__init__()
        try:
            self.lon = sys.argv[1]
            self.lat = sys.argv[2]
            self.scale = int(sys.argv[3])
        except IndexError:
            self.lon = "39.573954"
            self.lat = "52.621706"
            self.scale = 12
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
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.create_image()

    def closeEvent(self, event):
        os.remove(self.map_file)

    def create_image(self):
        self.getImage()
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.scale = min(self.scale + 1, 21)
            self.create_image()
        if event.key() == Qt.Key_Down:
            self.scale = max(self.scale - 1, 0)
            self.create_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BigMap()
    ex.show()
    sys.exit(app.exec())