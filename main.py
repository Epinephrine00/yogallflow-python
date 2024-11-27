

from ui import Ui_MainWindow as ui


from PyQt5.QtWidgets import *     
from PyQt5 import QtCore
from vcolorpicker import getColor
import copy
import sys 
import json
import os
import pickle
from CustomWidgets import CircularLayout as CirLayout


class MainWindow(QMainWindow, ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.CurrentSelectedLED = 0
        self.isPaletteSelected = False
        

        self.horizontalSlider.  setValue(50)
        self.horizontalSlider_2.setValue(50)
        self.horizontalSlider_3.setValue(50)
        self.spinBox.           setValue(50)
        self.spinBox_2.         setValue(50)
        self.spinBox_3.         setValue(50)
        
        self.horizontalSlider.valueChanged.connect(self.setColorsBySlider)
        self.horizontalSlider_2.valueChanged.connect(self.setColorsBySlider)
        self.horizontalSlider_3.valueChanged.connect(self.setColorsBySlider)

        self.spinBox.valueChanged.connect(self.setColorsBySpinBox)
        self.spinBox_2.valueChanged.connect(self.setColorsBySpinBox)
        self.spinBox_3.valueChanged.connect(self.setColorsBySpinBox)

        self.pushButton_17.clicked.connect(self.exportAsJson)
        self.pushButton_16.clicked.connect(self.newSequence)
        self.pushButton_15.clicked.connect(self.callColorPicker)
        self.pushButton_14.clicked.connect(self.addSets2List)
        self.pushButton_13.clicked.connect(self.addList2Data)

        self.pushButton_18.clicked.connect(self.rotateCounterClockwise)
        self.pushButton_19.clicked.connect(self.rotateClockwise)
        

        self.listWidget.itemDoubleClicked.connect(self.item_double_clicked)


        self.spinBox_4.setValue(50)

        self.Palettes = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
                         self.pushButton_5, self.pushButton_6, self.pushButton_7, self.pushButton_8,
                         self.pushButton_9, self.pushButton_10, self.pushButton_11, self.pushButton_12]
        for button in self.Palettes:
            button.hide()

        self.Data:list[dict]= []
        self.loadData()
        self.ledSets:list[list[int]] = [[50, 50, 50]]*12
        self.ledList:list[list[list[int]]] = []
        self.duration:list[int] = []



        self.initCircleButtons()


        self.show()
    
    def initCircleButtons(self):
        for i in range(12):
            self.circle.buttons[i].clicked.connect(lambda _, index=i:self.setCurrentSelectedLED(index))
        self.setColors()
    
    def setCurrentSelectedLED(self, i:int):
        self.CurrentSelectedLED = i
        self.setColorsBySlider()

    def callColorPicker(self):
        r, g, b = self.horizontalSlider.value(), self.horizontalSlider_2.value(), self.horizontalSlider_3.value()
        oldColor = (int((r/100)*255), int((g/100)*255), int((b/100)*255))
        color = getColor(oldColor)
        print(color)

        r, g, b = color
        r, g, b = int((r/255)*100), int((g/255)*100), int((b/255)*100)
        self.spinBox.setValue(r)
        self.spinBox_2.setValue(g)
        self.spinBox_3.setValue(b)
        self.horizontalSlider.setValue(r)
        self.horizontalSlider_2.setValue(g)
        self.horizontalSlider_3.setValue(b)
        self.ledSets[self.CurrentSelectedLED] = [r, g, b]
        self.setColors()


    def setColorsBySlider(self):
        r, g, b = self.horizontalSlider.value(), self.horizontalSlider_2.value(), self.horizontalSlider_3.value()
        self.spinBox.setValue(r)
        self.spinBox_2.setValue(g)
        self.spinBox_3.setValue(b)
        self.ledSets[self.CurrentSelectedLED] = [r, g, b]
        self.setColors()
    def setColorsBySpinBox(self):
        r, g, b = self.spinBox.value(), self.spinBox_2.value(), self.spinBox_3.value()
        self.horizontalSlider.setValue(r)
        self.horizontalSlider_2.setValue(g)
        self.horizontalSlider_3.setValue(b)
        self.ledSets[self.CurrentSelectedLED] = [r, g, b]
        self.setColors()
    def setColors(self):
        for i in range(len(self.ledSets)):
            r, g, b = self.ledSets[i]
            hexcode = "background:#%02x%02x%02x"%(int((r/100)*255), int((g/100)*255), int((b/100)*255))
            self.circle.buttons[i].setStyleSheet(hexcode)

    def addSets2List(self):
        self.duration.append(self.spinBox_4.value())
        self.ledList.append(copy.deepcopy(self.ledSets))
        self.renderScrollList()
    def renderScrollList_(self):
        for i in range(len(self.ledList)):
            circle = CirLayout(self.centralwidget, buttonSize=(5, 5), rad=20)
            circle.setMinimumSize(30, 30)
            for j in range(12):
                r, g, b = self.ledList[i][j]
                hexcode = "background:#%02x%02x%02x"%(int((r/100)*255), int((g/100)*255), int((b/100)*255))
                circle.buttons[j].setStyleSheet(hexcode)
            du = str(self.duration[i])
            lab = QLabel(self.centralwidget)
            lab.setText(du)

    def renderScrollList(self):
        self.scrollArea.takeWidget()
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 198, 76))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # 새로 만들 레이아웃 설정
        layout = QHBoxLayout(self.scrollAreaWidgetContents)  # 새로운 레이아웃을 설정합니다.
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)

        # 각 항목들을 반복하여 레이아웃에 추가합니다.
        for i in range(len(self.ledList)):
            # Create a vertical layout for the circle and label
            vbox = QVBoxLayout()
            vbox.setAlignment(QtCore.Qt.AlignCenter)

            # Create the CirLayout instance
            circle = CirLayout(self.scrollAreaWidgetContents, buttonSize=(5, 5), rad=20)
            circle.setMinimumSize(45, 45)

            # Set the color for each button in the circle
            for j in range(12):
                r, g, b = self.ledList[i][j]
                hexcode = "background:#%02x%02x%02x" % (
                    int((r / 100) * 255), int((g / 100) * 255), int((b / 100) * 255)
                )
                circle.buttons[j].setStyleSheet(hexcode)

            # Add the circle to the vertical layout
            vbox.addWidget(circle)

            # Create the label for duration and add to the layout
            du = str(self.duration[i])
            lab = QLabel(self.scrollAreaWidgetContents)
            lab.setText(du)
            lab.setAlignment(QtCore.Qt.AlignCenter)
            vbox.addWidget(lab)

            # Add the vertical layout to the main horizontal layout
            layout.addLayout(vbox)

        # Update the scroll area to use the new layout
        self.scrollAreaWidgetContents.setLayout(layout)
    
    def addList2Data(self):
        name = self.getName()
        if name is None:
            name = ''
        
        self.Data.append({
            'duration':copy.deepcopy(self.duration),
            'ledList' :copy.deepcopy(self.ledList),
            'name':name
        })

        self.renderDataList()
    def getName(self):
        # QInputDialog를 사용하여 텍스트 입력 받기
        text, ok = QInputDialog.getText(self, "시퀀스 이름", "시퀀스 이름을 입력해주세요. ")
        
        if ok:
            return text
        else:
            return None

    def renderDataList(self):
        self.listWidget.clear()
        for i in self.Data:
            self.listWidget.addItem(i['name'])
        self.saveData()

    def item_double_clicked(self, item):
        row = self.listWidget.row(item)
        del self.Data[row]
        self.renderDataList()

    def newSequence(self):
        self.ledSets:list[list[int]] = [[50, 50, 50]]*12
        self.ledList:list[list[list[int]]] = []
        self.duration:list[int] = []
        self.renderScrollList()
        self.setColors()
        self.saveData()
    
    def exportAsJson(self):
        self.saveData()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(None, "저장할 파일 선택", "", "JSON Files (*.json);;All Files (*)", options=options)

        if file_name:
            if not file_name.lower().endswith('.json'):
                file_name += '.json'

            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(self.Data, f, ensure_ascii=False, indent=4)
                QMessageBox.information(None, "저장 성공", f"파일이 성공적으로 저장되었습니다. ")
            except Exception as e:
                QMessageBox.critical(None, "저장 오류", f"파일 저장에 실패했습니다. ")

    def rotateCounterClockwise(self):
        self.rotate(11)
    def rotateClockwise(self):
        self.rotate(1)
    
    def rotate(self, way):
        tmp = copy.deepcopy(self.ledSets)
        self.ledSets = [[]]*12
        for i in range(12):
            self.ledSets[(i+way)%12] = tmp[i]
        self.CurrentSelectedLED += way
        self.CurrentSelectedLED %= 12
        self.setColors()
    
    def loadData(self):
        if os.path.isfile("data.bin"):
            with open("data.bin", 'rb') as f:
                self.Data = pickle.load(f)
                self.renderDataList()
    
    def saveData(self):
        with open("data.bin", 'wb') as f:
            pickle.dump(self.Data, f)

        

if __name__ == "__main__":
    isDebuging = True
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    app.exec_()