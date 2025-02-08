# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'costsgEYcMN.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
from wind import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(930, 650)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(930, 650))
        Form.setStyleSheet(u"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: #9faeda;\n"
"    outline: none;\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: #9faeda;\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: #9faeda;\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"    color: #f8f8f2;\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: #6272a4;\n"
"	max-width: 30px;\n"
"	border: none;\n"
"	border-style: none;\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: #6272a4;\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid #6272a4;\n"
"	background-color: #6272a4;\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    color: #f8f8f2;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid #6272a4;\n"
"}\n"
"\n"
"QLineEdit {\n"
"	background-color: #6272a4;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #6272a4;"
                        "\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"    color: #f8f8f2;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid #ff79c6;\n"
"}\n"
"\n"
"QComboBox {\n"
"	background-color: #6272a4;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #6272a4;\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"    color: #f8f8f2;\n"
"	font: 9pt \"Segoe UI\";\n"
"}\n"
"QComboBox:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QComboBox:focus {\n"
"	border: 2px solid #ff79c6;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: #6272a4;\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:hori"
                        "zontal {\n"
"    border: none;\n"
"    background: #6272a4;\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: #6272a4;\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background-color: #6272a4;\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::ad"
                        "d-line:vertical {\n"
"     border: none;\n"
"    background: #6272a4;\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: #6272a4;\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }")
        self.verticalLayout_6 = QVBoxLayout(Form)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)
        self.label.setMinimumSize(QSize(0, 50))
        self.label.setMaximumSize(QSize(16777215, 50))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignmentFlag.AlignHCenter)

        self.frame_Stock_type = QFrame(self.widget)
        self.frame_Stock_type.setObjectName(u"frame_Stock_type")
        self.frame_Stock_type.setMinimumSize(QSize(0, 60))
        self.frame_Stock_type.setMaximumSize(QSize(16777215, 60))
        self.frame_Stock_type.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Stock_type.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_Stock_type)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_Stock_type)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 0))
        self.frame_4.setMaximumSize(QSize(150, 16777215))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(12, 0, 0, 0)
        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(0, 0))
        self.label_5.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_5.setFont(font1)

        self.horizontalLayout_11.addWidget(self.label_5)


        self.horizontalLayout_12.addWidget(self.frame_4)

        self.frame_21 = QFrame(self.frame_Stock_type)
        self.frame_21.setObjectName(u"frame_21")
        self.frame_21.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_10 = QVBoxLayout(self.frame_21)
        self.verticalLayout_10.setSpacing(6)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_st_type_file = QLabel(self.frame_21)
        self.label_st_type_file.setObjectName(u"label_st_type_file")
        self.label_st_type_file.setMinimumSize(QSize(0, 30))
        self.label_st_type_file.setMaximumSize(QSize(16777215, 30))
        self.label_st_type_file.setStyleSheet(u"background-color: #6272a4;\n"
"border-radius: 5px;\n"
"border: 2px solid #6272a4;\n"
"padding-left: 10px;\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 121, 198);\n"
"color: #f8f8f2;")

        self.verticalLayout_10.addWidget(self.label_st_type_file)


        self.horizontalLayout_12.addWidget(self.frame_21)

        self.horizontalSpacer_8 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_8)

        self.frame_22 = QFrame(self.frame_Stock_type)
        self.frame_22.setObjectName(u"frame_22")
        self.frame_22.setMinimumSize(QSize(220, 0))
        self.frame_22.setMaximumSize(QSize(220, 16777215))
        self.horizontalLayout_17 = QHBoxLayout(self.frame_22)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(9, 9, -1, -1)
        self.btn_st_type_open_file = QPushButton(self.frame_22)
        self.btn_st_type_open_file.setObjectName(u"btn_st_type_open_file")
        self.btn_st_type_open_file.setMinimumSize(QSize(90, 30))
        self.btn_st_type_open_file.setMaximumSize(QSize(90, 16777215))
        icon = QIcon()
        icon.addFile(u":/icon/icon/folder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_st_type_open_file.setIcon(icon)

        self.horizontalLayout_17.addWidget(self.btn_st_type_open_file)

        self.btn_st_type_upload_file = QPushButton(self.frame_22)
        self.btn_st_type_upload_file.setObjectName(u"btn_st_type_upload_file")
        self.btn_st_type_upload_file.setMinimumSize(QSize(90, 30))
        self.btn_st_type_upload_file.setMaximumSize(QSize(90, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/upload.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_st_type_upload_file.setIcon(icon1)

        self.horizontalLayout_17.addWidget(self.btn_st_type_upload_file)


        self.horizontalLayout_12.addWidget(self.frame_22)


        self.verticalLayout.addWidget(self.frame_Stock_type)

        self.frame_LPC = QFrame(self.widget)
        self.frame_LPC.setObjectName(u"frame_LPC")
        self.frame_LPC.setMinimumSize(QSize(0, 60))
        self.frame_LPC.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout_2 = QHBoxLayout(self.frame_LPC)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_LPC)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(150, 0))
        self.frame.setMaximumSize(QSize(150, 16777215))
        self.frame.setStyleSheet(u"")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(12, 0, 0, 0)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(0, 0))
        self.label_2.setMaximumSize(QSize(16777215, 16777215))
        self.label_2.setFont(font1)

        self.horizontalLayout_6.addWidget(self.label_2)


        self.horizontalLayout_2.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_LPC)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_lpc_file = QLabel(self.frame_2)
        self.label_lpc_file.setObjectName(u"label_lpc_file")
        self.label_lpc_file.setMinimumSize(QSize(0, 30))
        self.label_lpc_file.setMaximumSize(QSize(16777215, 30))
        self.label_lpc_file.setStyleSheet(u"background-color: #6272a4;\n"
"border-radius: 5px;\n"
"border: 2px solid #6272a4;\n"
"padding-left: 10px;\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 121, 198);\n"
"color: #f8f8f2;")

        self.verticalLayout_3.addWidget(self.label_lpc_file)


        self.horizontalLayout_2.addWidget(self.frame_2)

        self.horizontalSpacer = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.frame_3 = QFrame(self.frame_LPC)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(220, 0))
        self.frame_3.setMaximumSize(QSize(220, 16777215))
        self.horizontalLayout_5 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(9, 9, -1, -1)
        self.btn_lpc_open_file = QPushButton(self.frame_3)
        self.btn_lpc_open_file.setObjectName(u"btn_lpc_open_file")
        self.btn_lpc_open_file.setMinimumSize(QSize(90, 30))
        self.btn_lpc_open_file.setMaximumSize(QSize(90, 16777215))
        self.btn_lpc_open_file.setIcon(icon)

        self.horizontalLayout_5.addWidget(self.btn_lpc_open_file)

        self.btn_lpc_upload_file = QPushButton(self.frame_3)
        self.btn_lpc_upload_file.setObjectName(u"btn_lpc_upload_file")
        self.btn_lpc_upload_file.setMinimumSize(QSize(90, 30))
        self.btn_lpc_upload_file.setMaximumSize(QSize(90, 16777215))
        self.btn_lpc_upload_file.setIcon(icon1)

        self.horizontalLayout_5.addWidget(self.btn_lpc_upload_file)


        self.horizontalLayout_2.addWidget(self.frame_3)


        self.verticalLayout.addWidget(self.frame_LPC)

        self.frame_Stock = QFrame(self.widget)
        self.frame_Stock.setObjectName(u"frame_Stock")
        self.frame_Stock.setMinimumSize(QSize(0, 60))
        self.frame_Stock.setMaximumSize(QSize(16777215, 60))
        self.frame_Stock.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Stock.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_Stock)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_stock = QFrame(self.frame_Stock)
        self.frame_stock.setObjectName(u"frame_stock")
        self.frame_stock.setMaximumSize(QSize(150, 16777215))
        self.frame_stock.setStyleSheet(u"")
        self.frame_stock.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_stock.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_stock)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(12, 0, 0, 0)
        self.label_4 = QLabel(self.frame_stock)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 0))
        self.label_4.setMaximumSize(QSize(16777215, 16777215))
        self.label_4.setFont(font1)

        self.horizontalLayout_4.addWidget(self.label_4)


        self.horizontalLayout_3.addWidget(self.frame_stock)

        self.frame_7 = QFrame(self.frame_Stock)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.frame_7)
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_stock_file = QLabel(self.frame_7)
        self.label_stock_file.setObjectName(u"label_stock_file")
        self.label_stock_file.setMinimumSize(QSize(0, 30))
        self.label_stock_file.setMaximumSize(QSize(16777215, 30))
        self.label_stock_file.setStyleSheet(u"background-color: #6272a4;\n"
"border-radius: 5px;\n"
"border: 2px solid #6272a4;\n"
"padding-left: 10px;\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 121, 198);\n"
"color: #f8f8f2;")

        self.verticalLayout_4.addWidget(self.label_stock_file)


        self.horizontalLayout_3.addWidget(self.frame_7)

        self.horizontalSpacer_2 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.frame_8 = QFrame(self.frame_Stock)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(220, 0))
        self.frame_8.setMaximumSize(QSize(220, 16777215))
        self.horizontalLayout_7 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(9, 9, -1, -1)
        self.btn_stock_open_file = QPushButton(self.frame_8)
        self.btn_stock_open_file.setObjectName(u"btn_stock_open_file")
        self.btn_stock_open_file.setMinimumSize(QSize(90, 30))
        self.btn_stock_open_file.setMaximumSize(QSize(90, 16777215))
        self.btn_stock_open_file.setIcon(icon)

        self.horizontalLayout_7.addWidget(self.btn_stock_open_file)

        self.btn_stock_upload_file = QPushButton(self.frame_8)
        self.btn_stock_upload_file.setObjectName(u"btn_stock_upload_file")
        self.btn_stock_upload_file.setMinimumSize(QSize(90, 30))
        self.btn_stock_upload_file.setMaximumSize(QSize(90, 16777215))
        self.btn_stock_upload_file.setIcon(icon1)

        self.horizontalLayout_7.addWidget(self.btn_stock_upload_file)


        self.horizontalLayout_3.addWidget(self.frame_8)


        self.verticalLayout.addWidget(self.frame_Stock)

        self.frame_Batch = QFrame(self.widget)
        self.frame_Batch.setObjectName(u"frame_Batch")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_Batch.sizePolicy().hasHeightForWidth())
        self.frame_Batch.setSizePolicy(sizePolicy1)
        self.frame_Batch.setMinimumSize(QSize(0, 60))
        self.frame_Batch.setMaximumSize(QSize(16777215, 60))
        self.frame_Batch.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Batch.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_Batch)
        self.horizontalLayout_15.setSpacing(0)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.frame_9 = QFrame(self.frame_Batch)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setMinimumSize(QSize(150, 0))
        self.frame_9.setMaximumSize(QSize(150, 16777215))
        self.frame_9.setStyleSheet(u"")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(12, 0, 0, 0)
        self.label_3 = QLabel(self.frame_9)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(0, 0))
        self.label_3.setMaximumSize(QSize(16777215, 16777215))
        self.label_3.setFont(font1)

        self.horizontalLayout_13.addWidget(self.label_3)


        self.horizontalLayout_15.addWidget(self.frame_9)

        self.frame_19 = QFrame(self.frame_Batch)
        self.frame_19.setObjectName(u"frame_19")
        self.frame_19.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_9 = QVBoxLayout(self.frame_19)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_batch_file = QLabel(self.frame_19)
        self.label_batch_file.setObjectName(u"label_batch_file")
        self.label_batch_file.setMinimumSize(QSize(0, 30))
        self.label_batch_file.setMaximumSize(QSize(16777215, 30))
        self.label_batch_file.setStyleSheet(u"background-color: #6272a4;\n"
"border-radius: 5px;\n"
"border: 2px solid #6272a4;\n"
"padding-left: 10px;\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 121, 198);\n"
"color: #f8f8f2;")

        self.verticalLayout_9.addWidget(self.label_batch_file)


        self.horizontalLayout_15.addWidget(self.frame_19)

        self.horizontalSpacer_5 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_15.addItem(self.horizontalSpacer_5)

        self.frame_20 = QFrame(self.frame_Batch)
        self.frame_20.setObjectName(u"frame_20")
        self.frame_20.setMinimumSize(QSize(220, 0))
        self.frame_20.setMaximumSize(QSize(220, 16777215))
        self.horizontalLayout_14 = QHBoxLayout(self.frame_20)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(9, 9, -1, -1)
        self.btn_batch_open_file = QPushButton(self.frame_20)
        self.btn_batch_open_file.setObjectName(u"btn_batch_open_file")
        self.btn_batch_open_file.setMinimumSize(QSize(90, 30))
        self.btn_batch_open_file.setMaximumSize(QSize(90, 16777215))
        self.btn_batch_open_file.setIcon(icon)

        self.horizontalLayout_14.addWidget(self.btn_batch_open_file)

        self.btn_batch_upload_file = QPushButton(self.frame_20)
        self.btn_batch_upload_file.setObjectName(u"btn_batch_upload_file")
        self.btn_batch_upload_file.setMinimumSize(QSize(90, 30))
        self.btn_batch_upload_file.setMaximumSize(QSize(90, 16777215))
        self.btn_batch_upload_file.setIcon(icon1)

        self.horizontalLayout_14.addWidget(self.btn_batch_upload_file)


        self.horizontalLayout_15.addWidget(self.frame_20)


        self.verticalLayout.addWidget(self.frame_Batch)

        self.frame_ED = QFrame(self.widget)
        self.frame_ED.setObjectName(u"frame_ED")
        self.frame_ED.setMinimumSize(QSize(0, 80))
        self.frame_ED.setMaximumSize(QSize(16777215, 100))
        self.frame_ED.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_ED.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_ED)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frame_ED)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(200, 0))
        self.frame_6.setMaximumSize(QSize(200, 16777215))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(12, 0, 0, 0)
        self.label_6 = QLabel(self.frame_6)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.horizontalLayout_8.addWidget(self.label_6)


        self.horizontalLayout_9.addWidget(self.frame_6)

        self.frame_10 = QFrame(self.frame_ED)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(110, 0))
        self.frame_10.setMaximumSize(QSize(110, 16777215))
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_10)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(9, 0, 9, 9)
        self.label_7 = QLabel(self.frame_10)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_2.addWidget(self.label_7)

        self.line_ed_year = QLineEdit(self.frame_10)
        self.line_ed_year.setObjectName(u"line_ed_year")
        self.line_ed_year.setMinimumSize(QSize(80, 25))
        self.line_ed_year.setMaximumSize(QSize(80, 16777215))

        self.verticalLayout_2.addWidget(self.line_ed_year)


        self.horizontalLayout_9.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.frame_ED)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(130, 0))
        self.frame_11.setMaximumSize(QSize(130, 16777215))
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_11)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(9, 0, 9, 9)
        self.label_8 = QLabel(self.frame_11)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_5.addWidget(self.label_8)

        self.line_ed_amount = QLineEdit(self.frame_11)
        self.line_ed_amount.setObjectName(u"line_ed_amount")
        self.line_ed_amount.setMinimumSize(QSize(90, 25))
        self.line_ed_amount.setMaximumSize(QSize(90, 16777215))

        self.verticalLayout_5.addWidget(self.line_ed_amount)


        self.horizontalLayout_9.addWidget(self.frame_11)

        self.frame_16 = QFrame(self.frame_ED)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(130, 0))
        self.frame_16.setMaximumSize(QSize(130, 16777215))
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_16)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(9, 0, 9, 9)
        self.label_11 = QLabel(self.frame_16)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_8.addWidget(self.label_11)

        self.line_eco_amount = QLineEdit(self.frame_16)
        self.line_eco_amount.setObjectName(u"line_eco_amount")
        self.line_eco_amount.setMinimumSize(QSize(90, 25))
        self.line_eco_amount.setMaximumSize(QSize(90, 16777215))

        self.verticalLayout_8.addWidget(self.line_eco_amount)


        self.horizontalLayout_9.addWidget(self.frame_16)

        self.frame_12 = QFrame(self.frame_ED)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(0, 0))
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.btn_ocogs_create = QPushButton(self.frame_12)
        self.btn_ocogs_create.setObjectName(u"btn_ocogs_create")
        self.btn_ocogs_create.setMinimumSize(QSize(90, 30))
        self.btn_ocogs_create.setMaximumSize(QSize(90, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/icon/icon/file-plus.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_ocogs_create.setIcon(icon2)

        self.horizontalLayout_10.addWidget(self.btn_ocogs_create)


        self.horizontalLayout_9.addWidget(self.frame_12)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_7)

        self.frame_18 = QFrame(self.frame_ED)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 0))
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.btn_update_tab = QPushButton(self.frame_18)
        self.btn_update_tab.setObjectName(u"btn_update_tab")
        self.btn_update_tab.setMinimumSize(QSize(120, 30))
        self.btn_update_tab.setMaximumSize(QSize(16777215, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/icon/icon/refresh-cw.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_update_tab.setIcon(icon3)

        self.horizontalLayout_16.addWidget(self.btn_update_tab)


        self.horizontalLayout_9.addWidget(self.frame_18)

        self.horizontalSpacer_3 = QSpacerItem(642, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addWidget(self.frame_ED)

        self.frame_cost_table = QFrame(self.widget)
        self.frame_cost_table.setObjectName(u"frame_cost_table")
        self.frame_cost_table.setMinimumSize(QSize(0, 280))
        self.frame_cost_table.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_cost_table.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_cost_table)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_9 = QSpacerItem(150, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_9)

        self.table = QTableWidget(self.frame_cost_table)
        if (self.table.columnCount() < 3):
            self.table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.table.setObjectName(u"table")
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        self.table.setMinimumSize(QSize(350, 0))
        self.table.setMaximumSize(QSize(350, 16777215))
        font2 = QFont()
        font2.setPointSize(8)
        self.table.setFont(font2)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setColumnCount(3)
        self.table.horizontalHeader().setMinimumSectionSize(25)
        self.table.verticalHeader().setMinimumSectionSize(0)
        self.table.verticalHeader().setDefaultSectionSize(10)

        self.horizontalLayout.addWidget(self.table)

        self.frame_5 = QFrame(self.frame_cost_table)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_9 = QLabel(self.frame_5)
        self.label_9.setObjectName(u"label_9")
        font3 = QFont()
        font3.setPointSize(11)
        font3.setBold(True)
        self.label_9.setFont(font3)

        self.verticalLayout_7.addWidget(self.label_9)


        self.horizontalLayout.addWidget(self.frame_5)

        self.horizontalSpacer_6 = QSpacerItem(540, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_6)


        self.verticalLayout.addWidget(self.frame_cost_table)


        self.verticalLayout_6.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u0417\u0430\u0442\u0440\u0430\u0442\u044b & \u041e\u0441\u0442\u0430\u0442\u043a\u0438", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u0422\u0438\u043f\u044b \u0441\u043a\u043b\u0430\u0434\u043e\u0432", None))
        self.label_st_type_file.setText(QCoreApplication.translate("Form", u"File Path", None))
        self.btn_st_type_open_file.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_st_type_upload_file.setText(QCoreApplication.translate("Form", u"Upload", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u0421\u0435\u0431-\u0442\u044c", None))
        self.label_lpc_file.setText(QCoreApplication.translate("Form", u"File Path", None))
        self.btn_lpc_open_file.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_lpc_upload_file.setText(QCoreApplication.translate("Form", u"Upload", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u041e\u0441\u0442\u0430\u0442\u043a\u0438", None))
        self.label_stock_file.setText(QCoreApplication.translate("Form", u"File Path", None))
        self.btn_stock_open_file.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_stock_upload_file.setText(QCoreApplication.translate("Form", u"Upload", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u041f\u0430\u0440\u0442\u0438\u0438", None))
        self.label_batch_file.setText(QCoreApplication.translate("Form", u"File Path", None))
        self.btn_batch_open_file.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_batch_upload_file.setText(QCoreApplication.translate("Form", u"Upload", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u0410\u043a\u0446\u0438\u0437 & \u0423\u0442\u0438\u043b.\u0421\u0431\u043e\u0440", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u0413\u043e\u0434", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u0421\u0443\u043c\u043c\u0430 \u0410\u043a\u0446\u0438\u0437\u0430", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u0421\u0443\u043c\u043c\u0430 \u0423\u0442\u0438\u043b", None))
        self.btn_ocogs_create.setText(QCoreApplication.translate("Form", u"Create", None))
        self.btn_update_tab.setText(QCoreApplication.translate("Form", u"Refrash Table", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"\u0413\u043e\u0434", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u0410\u043a\u0446\u0438\u0437", None));
        ___qtablewidgetitem2 = self.table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"\u0423\u0442\u0438\u043b.\u0421\u0431\u043e\u0440", None));
        self.label_9.setText(QCoreApplication.translate("Form", u"! \u0421\u043d\u0430\u0447\u0430\u043b\u0430 \u043e\u0431\u043d\u043e\u0432\u0438 \u0422\u0438\u043f\u044b \u0421\u043a\u043b\u0430\u0434\u043e\u0432 !", None))
    # retranslateUi

