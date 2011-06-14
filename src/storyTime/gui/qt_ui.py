# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\moonbot\dev\storyTime\design\qt_ui.ui'
#
# Created: Tue Jun 07 12:36:38 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(598, 507)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView_2 = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_2.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.graphicsView_2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.timeLabel = QtGui.QLabel(self.centralwidget)
        self.timeLabel.setMinimumSize(QtCore.QSize(52, 0))
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout_3.addWidget(self.timeLabel)
        self.timeSlider = QtGui.QSlider(self.centralwidget)
        self.timeSlider.setProperty("value", 0)
        self.timeSlider.setProperty("minimum", 0)
        self.timeSlider.setProperty("maximum", 0)
        self.timeSlider.setSliderPosition(0)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.horizontalLayout_3.addWidget(self.timeSlider)
        self.recordBtn = QtGui.QPushButton(self.centralwidget)
        self.recordBtn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.recordBtn.setObjectName("recordBtn")
        self.horizontalLayout_3.addWidget(self.recordBtn)
        self.playBtn = QtGui.QPushButton(self.centralwidget)
        self.playBtn.setMaximumSize(QtCore.QSize(50, 16777215))
        self.playBtn.setObjectName("playBtn")
        self.horizontalLayout_3.addWidget(self.playBtn)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.curTimeLabel = QtGui.QLabel(self.centralwidget)
        self.curTimeLabel.setMaximumSize(QtCore.QSize(125, 16777215))
        self.curTimeLabel.setObjectName("curTimeLabel")
        self.horizontalLayout.addWidget(self.curTimeLabel)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setMaximumSize(QtCore.QSize(125, 16777215))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 598, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport_Image_Sequence = QtGui.QAction(MainWindow)
        self.actionImport_Image_Sequence.setObjectName("actionImport_Image_Sequence")
        self.actionImport_Directory = QtGui.QAction(MainWindow)
        self.actionImport_Directory.setObjectName("actionImport_Directory")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionExport_To_FCP = QtGui.QAction(MainWindow)
        self.actionExport_To_FCP.setObjectName("actionExport_To_FCP")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionImport_Image_Sequence)
        self.menuFile.addAction(self.actionImport_Directory)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addAction(self.actionExport_To_FCP)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        MainWindow.setStyleSheet(QtGui.QApplication.translate("MainWindow", "background-color: rgb(50, 50, 50);color: rgb(255, 255, 255);selection-background-color:rgb(140, 140, 140)", None, QtGui.QApplication.UnicodeUTF8))
        self.timeLabel.setText(QtGui.QApplication.translate("MainWindow", "0/0", None, QtGui.QApplication.UnicodeUTF8))
        self.recordBtn.setStyleSheet(QtGui.QApplication.translate("MainWindow", "background-color: rgb(70, 70, 70);", None, QtGui.QApplication.UnicodeUTF8))
        self.recordBtn.setText(QtGui.QApplication.translate("MainWindow", "Record", None, QtGui.QApplication.UnicodeUTF8))
        self.playBtn.setStyleSheet(QtGui.QApplication.translate("MainWindow", "background-color: rgb(70, 70, 70);", None, QtGui.QApplication.UnicodeUTF8))
        self.playBtn.setText(QtGui.QApplication.translate("MainWindow", "Play", None, QtGui.QApplication.UnicodeUTF8))
        self.curTimeLabel.setText(QtGui.QApplication.translate("MainWindow", "00:00:00:000", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Press Space to advance frame", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "Film (24 fps)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "PAL (25 fps)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("MainWindow", "NTSC (30 fps)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(3, QtGui.QApplication.translate("MainWindow", "Show (48 fps)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(4, QtGui.QApplication.translate("MainWindow", "PAL Field (50 fps)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(5, QtGui.QApplication.translate("MainWindow", "NTSC Field (60 fps)", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(6, QtGui.QApplication.translate("MainWindow", "Custom...", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Directory.setText(QtGui.QApplication.translate("MainWindow", "Import Directory...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_Image_Sequence.setText(QtGui.QApplication.translate("MainWindow", "Import Image Sequence...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("MainWindow", "Open...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("MainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_As.setText(QtGui.QApplication.translate("MainWindow", "Save As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_To_FCP.setText(QtGui.QApplication.translate("MainWindow", "Export To Final Cut Pro...", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

