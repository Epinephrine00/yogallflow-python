from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPoint

import math


class CircularLayout(QWidget):
    def __init__(self, parent=None, rad:int=50, center:tuple[int] = (0, 0), buttonSize:tuple[int] = (35, 30)):
        super().__init__(parent)
        self.buttons = []
        self.radius = rad  # 원의 반지름
        self.center = QPoint(center[0], center[1])  # 원의 중심 좌표
        self.buttonSize = buttonSize

        # 버튼 12개 생성
        for i in range(12):
            button = QPushButton("", self)
            button.setMinimumSize(self.buttonSize[0], self.buttonSize[1])
            button.setMaximumSize(self.buttonSize[0], self.buttonSize[1])
            self.buttons.append(button)
            #button.setGeometry(0, 0, 30, 30)  # 버튼 기본 크기 설정

    def resizeEvent(self, event):
        # 중심 좌표를 동적으로 계산
        self.center = self.rect().center()
        self._arrange_buttons()

    def _arrange_buttons(self):
        """버튼을 원형으로 배치"""
        angle_step = 360 / len(self.buttons)  # 각 버튼 간의 각도 차
        for i, button in enumerate(self.buttons):
            angle = math.radians(i * angle_step)
            x = self.center.x() + self.radius * math.cos(angle) - button.width() / 2
            y = self.center.y() + self.radius * math.sin(angle) - button.height() / 2
            button.move(int(x), int(y))