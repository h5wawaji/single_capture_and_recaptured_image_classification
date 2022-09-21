import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QIcon
from Classification import *



class Ui_MainWindow(object):
    """
    Class for the creation and connection of the graphical interface.
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_image = QtWidgets.QLabel(self.centralwidget)
        self.label_image.setGeometry(QtCore.QRect(300, 20, 750, 563))
        self.label_image.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image.setLineWidth(1)
        self.label_image.setText("")
        self.label_image.setScaledContents(True)
        self.label_image.setObjectName("label_image")
        self.select_button = QtWidgets.QPushButton(self.centralwidget)
        self.select_button.setGeometry(QtCore.QRect(80, 180, 160, 50))
        self.select_button.setObjectName("select_button")
        self.label_result = QtWidgets.QLabel(self.centralwidget)
        self.label_result.setGeometry(QtCore.QRect(40, 410, 261, 101))
        self.label_result.setText("")
        self.label_result.setObjectName("label_result")
        self.label_classification = QtWidgets.QLabel(self.centralwidget)
        self.label_classification.setGeometry(QtCore.QRect(70, 480, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_classification.setFont(font)
        self.label_classification.setText("")
        self.label_classification.setObjectName("label_classification")
        self.label_classification.setAlignment(QtCore.Qt.AlignCenter)
        self.analyze_button = QtWidgets.QPushButton(self.centralwidget)
        self.analyze_button.setGeometry(QtCore.QRect(80, 240, 160, 50))
        self.analyze_button.setObjectName("analyze_button")
        self.more_info = QtWidgets.QPushButton(self.centralwidget)
        self.more_info.setGeometry(QtCore.QRect(80, 300, 160, 50))
        self.more_info.setObjectName("more_info_button")
        self.widget_filtered_block = QtWidgets.QWidget(self.centralwidget)
        self.widget_filtered_block.setGeometry(QtCore.QRect(430, 610, 40, 40))
        self.widget_filtered_block.setStyleSheet("background-color:rgb(0, 0, 0)")
        self.widget_filtered_block.setObjectName("widget")
        self.label_filtered_block = QtWidgets.QLabel(self.centralwidget)
        self.label_filtered_block.setGeometry(QtCore.QRect(490, 610, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_filtered_block.setFont(font)
        self.label_filtered_block.setObjectName("label")
        self.widget_wrong_classification = QtWidgets.QWidget(self.centralwidget)
        self.widget_wrong_classification.setGeometry(QtCore.QRect(660, 610, 40, 40))
        self.widget_wrong_classification.setStyleSheet("background-color:rgb(255, 78, 81)")
        self.widget_wrong_classification.setObjectName("widget_4")
        self.label_wrong_classification = QtWidgets.QLabel(self.centralwidget)
        self.label_wrong_classification.setGeometry(QtCore.QRect(720, 610, 261, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_wrong_classification.setFont(font)
        self.label_wrong_classification.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1106, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.path = None
        self.info = None
        self.image_class = None
        self.image_mask = None

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """
        Changes the names of the labels and buttons. Also set images.
        """
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Classifier"))
        MainWindow.setWindowIcon(QIcon("logo.png"))
        self.label_image.setText(_translate("MainWindow", ""))
        self.select_button.setText(_translate("MainWindow", "Select Image"))
        self.label_classification.setText(_translate("MainWindow", ""))
        self.analyze_button.setText(_translate("MainWindow", "Analyze Image"))
        self.label_wrong_classification.setText(_translate("MainWindow", "Wrongly classified block"))
        self.label_filtered_block.setText(_translate("MainWindow", "Filtered block"))
        self.more_info.setText(_translate("MainWindow", "More info"))
        # connections for the buttons
        self.select_button.clicked.connect(self.button_handler)
        self.analyze_button.clicked.connect(self.analyze_button_handler)
        self.more_info.clicked.connect(self.more_info_handler)

    def button_handler(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        txt = path.split('.')
        accepted_extensions = ['png', 'jpg', 'tif', 'TIF', 'PNG', 'JPG']  #accepted extensions for images
        if any(word in accepted_extensions for word in txt):
            self.label_image.setPixmap(QtGui.QPixmap(path))
            self.label_classification.setText("")
            self.path = path
            self.info = None
        else:
            self.show_popup_wrongfile()

    def analyze_button_handler(self):
        if self.path is None:
            self.show_popup_noimage()
        else:
            classification = Classification(self.path)
            self.image_class = classification.prediction()
            self.info = classification.info()
            self.image_mask = classification.create_mask()
            if self.image_class == 1:
                self.label_classification.setText("This is a \n recaptured image.")
                self.label_classification.adjustSize()
            else:
                self.label_classification.setText("This is a \n single capture \n image.")
                self.label_classification.adjustSize()

    def show_popup_wrongfile(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR: Wrong file extension")
        msg.setText("Please open a file with the following extensions: .jpg, .png, .tif")
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()

    def show_popup_noimage(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR: No image")
        msg.setText("You must load an image before analyzing it.")
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()

    def show_popup_noinfo(self):
        msg = QMessageBox()
        msg.setWindowTitle("ERROR: No info")
        msg.setText("To obtain more information about the classification, first you have to analyze an image.")
        msg.setIcon(QMessageBox.Warning)

        x = msg.exec_()

    def more_info_handler(self):
        if self.info is None:
            self.show_popup_noinfo()
        else:
            recaptured_blocks = np.count_nonzero(self.info == 1)
            single_capture_blocks = np.count_nonzero(self.info == 0)
            self.show_popup_info(recaptured_blocks, single_capture_blocks)

    def show_popup_info(self, recaptured_blocks, single_capture_blocks):
        msg = QMessageBox()
        msg.setWindowTitle("Information")
        msg.setText(" -{} blocks were analyzed \n"
                    " -{} blocks were classified as part of a recaptured image \n"
                    " -{} blocks were classified as part of a single capture image".format(
            recaptured_blocks + single_capture_blocks, recaptured_blocks, single_capture_blocks))
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Close)
        msg.addButton("Show blocks", QtWidgets.QMessageBox.YesRole)

        msg.buttonClicked.connect(self.show_blocks_clicked)

        x = msg.exec_()

    def show_blocks_clicked(self, i):
        if i.text() == "Close":
            pass
        else:
            image_to_show = QImage(self.image_mask.data, self.image_mask.shape[1], self.image_mask.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.label_image.setPixmap(QtGui.QPixmap(image_to_show))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
