# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'delivery_create_formGFlfci.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)
from wind import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(582, 406)
        Form.setStyleSheet(u"Form.QWidget{border: 2px solid #f28223;}\n"
"\n"
"QWidget{\n"
"	background-color: #f8f8f2;\n"
"}\n"
"\n"
"#Title_label.QLabel {\n"
"color: #262626;\n"
"font: 18pt \"Tahoma\";\n"
"}\n"
"\n"
"QLabel {\n"
"color: #262626;\n"
"font: 10pt \"Tahoma\";\n"
"}\n"
"\n"
"QPushButton {\n"
"	border: 2px solid #f09d54;\n"
"	border-radius: 5px;\n"
"	background-color: #f8f8f2;\n"
"	color: #964b09;\n"
"	font: 10pt \"Tahoma\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #f28223;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #f28223;\n"
"	border: 2px solid #f28223;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"\n"
"QTableWidget {	\n"
"	background-color: #f8f8f2;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: #f8994a;\n"
"    outline: none;\n"
"	color: #262626;\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: #f8994a;\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: #f8994a;\n"
"	color: #262626;\n"
"	padding: 1px;\n"
"    font: 7pt \"Tahoma\"; \n"
"}\n"
""
                        "QTableWidget::item:selected{\n"
"	background-color: #f28223;\n"
"    color: #ffffff;\n"
"}\n"
"QTableWidget::item:editable {\n"
"	background-color: #ffffd0;\n"
"	border: #ffffff;\n"
"}\n"
"QTableWidget::item:focus {\n"
"	background-color: #f28223;\n"
"	border: 2px solid #ffffff;\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: #f8f8f2;\n"
"	border: none;\n"
"	border-style: none;\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: #f8994a;\n"
"	font: 10pt \"Tahoma\";\n"
"}\n"
"QHeaderView::section:horizontal {\n"
"    border: 1px solid #f8994a;\n"
"	background-color: #ffd4af;\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    color: #262626;\n"
"}\n"
"QHeaderView::section:vertical {\n"
"    border: 1px solid #f8994a;\n"
"	color: #262626;\n"
"}\n"
"\n"
"QLineEdit {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-"
                        "color: #f28223;\n"
"    color: #262626;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid #f28223;\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid #f28223;\n"
"}\n"
"\n"
"QComboBox {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	selection-color: #f28223;\n"
"	selection-background-color: #f28223;\n"
"    color: #262626;\n"
"	font: 9pt \"Tahoma\";\n"
"}\n"
"QComboBox:hover {\n"
"	border: 2px solid #f28223;\n"
"	\n"
"}\n"
"QComboBox:focus {\n"
"	border: 2px solid #f28223;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView::item {\n"
"	color: #262626;\n"
"}\n"
"QComboBox QAbstractItemView::item::selected {\n"
"	background-color: #f09d54;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"	\n"
"	image: url(:/icon/icon/chevron-down \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg);\n"
"}\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 1"
                        "5px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: #f8994a;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"	color: #262626;\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: #f8994a;\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: #f6c294;\n"
"    min-width: 20px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: #f8994a;\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: #f8994a;\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontr"
                        "ol-position: left;\n"
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
"    background-color: #f8994a;\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: #f6c294;\n"
"    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: #f8994a;\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: #f8994a;\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subc"
                        "ontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"QDateEdit {\n"
"    background-color: #f8f8f2;\n"
"    border-radius: 5px;\n"
"    border: 2px solid #f09d54;\n"
"    padding-left: 10px; /* Add left padding */\n"
"    padding-right: 10px; /* Add right padding to accommodate the dropdown arrow */\n"
"    color: #262626;\n"
"    font: 10pt \"Tahoma\";\n"
"    min-width: 80px; /* Minimum width to prevent text clipping */\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 2px solid #f28223;\n"
"}\n"
"\n"
"QDateEdit:focus {\n"
"    border: 2px solid #f28223;\n"
"}\n"
"\n"
"QDateEdit::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 25px; /* Keep the dropdown arrow width */\n"
"    border-left-width: 1px;\n"
"    border-left-color: #"
                        "f8994a;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"    background-color: #f8f8f2;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"	image: url(:/icon/icon/chevron-down \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg);\n"
"    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"/* Calendar Styling */\n"
"QCalendarWidget {\n"
"    background-color: #f8f8f2;\n"
"    border: 2px solid #f28223;\n"
"    color: #262626;\n"
"}\n"
"\n"
"QCalendarWidget QWidget {\n"
"    color: #262626;\n"
"}\n"
"\n"
"QCalendarWidget QAbstractItemView {\n"
"    background-color: #f8f8f2;\n"
"    selection-background-color: #f28223;\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton {\n"
"    background-color: #ffd4af;\n"
"    color: #262626;\n"
"    font: 10pt \"Tahoma\";\n"
"    border-radius: 3px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton:hover {\n"
"    background-color: #f28223;\n"
"    c"
                        "olor: #ffffff;\n"
"}\n"
"\n"
"QCalendarWidget QMenu {\n"
"    background-color: #f8f8f2;\n"
"    border: 1px solid #f28223;\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox {\n"
"    background-color: #f8f8f2;\n"
"    color: #262626;\n"
"    border: 1px solid #f09d54;\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: #f8994a;\n"
"    border-left-style: solid;\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 15px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: #f8994a;\n"
"    border-left-style: solid;\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox::up-arrow {\n"
"	image: url(:/icon/icon/chevron-up \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"\n"
"QCalendarWidget QSpinBox::d"
                        "own-arrow {\n"
"	image: url(:/icon/icon/chevron-down \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"")
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_17 = QHBoxLayout(self.widget)
        self.horizontalLayout_17.setSpacing(0)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 9, 0, 10)
        self.Title_label = QLabel(self.frame_2)
        self.Title_label.setObjectName(u"Title_label")
        self.Title_label.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setFamilies([u"Tahoma"])
        font.setPointSize(18)
        font.setBold(False)
        font.setItalic(False)
        self.Title_label.setFont(font)
        self.Title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.Title_label)

        self.frame_date_bill = QFrame(self.frame_2)
        self.frame_date_bill.setObjectName(u"frame_date_bill")
        self.frame_date_bill.setMinimumSize(QSize(0, 45))
        self.frame_date_bill.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_date_bill.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_date_bill)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.frame_date_bill)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 44))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.line_deliv_date = QDateEdit(self.frame_5)
        self.line_deliv_date.setObjectName(u"line_deliv_date")
        self.line_deliv_date.setMinimumSize(QSize(104, 22))
        self.line_deliv_date.setMaximumSize(QSize(16777215, 22))
        font1 = QFont()
        font1.setFamilies([u"Tahoma"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setKerning(False)
        self.line_deliv_date.setFont(font1)
        self.line_deliv_date.setCalendarPopup(True)

        self.horizontalLayout_5.addWidget(self.line_deliv_date)


        self.horizontalLayout_8.addWidget(self.frame_5)

        self.frame = QFrame(self.frame_date_bill)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 44))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.line_bill = QLineEdit(self.frame)
        self.line_bill.setObjectName(u"line_bill")
        self.line_bill.setMinimumSize(QSize(160, 22))
        self.line_bill.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_2.addWidget(self.line_bill)


        self.horizontalLayout_8.addWidget(self.frame)


        self.verticalLayout.addWidget(self.frame_date_bill)

        self.frame_customer = QFrame(self.frame_2)
        self.frame_customer.setObjectName(u"frame_customer")
        self.frame_customer.setMinimumSize(QSize(0, 45))
        self.frame_customer.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_customer.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_customer)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_customer)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(330, 44))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(9, 0, 9, 0)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(73, 0))
        self.label_2.setMaximumSize(QSize(73, 16777215))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.line_cust_name = QComboBox(self.frame_3)
        self.line_cust_name.setObjectName(u"line_cust_name")
        self.line_cust_name.setMinimumSize(QSize(240, 22))
        self.line_cust_name.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_3.addWidget(self.line_cust_name)


        self.horizontalLayout_7.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_customer)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 44))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.label_4 = QLabel(self.frame_4)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.line_inn = QLineEdit(self.frame_4)
        self.line_inn.setObjectName(u"line_inn")
        self.line_inn.setMinimumSize(QSize(100, 22))
        self.line_inn.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_4.addWidget(self.line_inn)


        self.horizontalLayout_7.addWidget(self.frame_4)


        self.verticalLayout.addWidget(self.frame_customer)

        self.frame_sborka = QFrame(self.frame_2)
        self.frame_sborka.setObjectName(u"frame_sborka")
        self.frame_sborka.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_sborka.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_sborka)
        self.horizontalLayout_12.setSpacing(0)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, 0, 0, 0)
        self.frame_10 = QFrame(self.frame_sborka)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_5 = QLabel(self.frame_10)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_9.addWidget(self.label_5)

        self.line_sborka = QLineEdit(self.frame_10)
        self.line_sborka.setObjectName(u"line_sborka")
        self.line_sborka.setMinimumSize(QSize(100, 22))
        self.line_sborka.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_9.addWidget(self.line_sborka)


        self.horizontalLayout_12.addWidget(self.frame_10)

        self.frame_11 = QFrame(self.frame_sborka)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_6 = QLabel(self.frame_11)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_10.addWidget(self.label_6)

        self.line_ts = QLineEdit(self.frame_11)
        self.line_ts.setObjectName(u"line_ts")
        self.line_ts.setMinimumSize(QSize(100, 22))
        self.line_ts.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_10.addWidget(self.line_ts)


        self.horizontalLayout_12.addWidget(self.frame_11)


        self.verticalLayout.addWidget(self.frame_sborka)

        self.frame_amounts = QFrame(self.frame_2)
        self.frame_amounts.setObjectName(u"frame_amounts")
        self.frame_amounts.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_amounts.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_amounts)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_15 = QFrame(self.frame_amounts)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_11.setSpacing(4)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(9, 9, 9, -1)
        self.label_9 = QLabel(self.frame_15)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_11.addWidget(self.label_9)

        self.line_amount = QLineEdit(self.frame_15)
        self.line_amount.setObjectName(u"line_amount")
        self.line_amount.setMinimumSize(QSize(140, 22))
        self.line_amount.setMaximumSize(QSize(140, 22))

        self.horizontalLayout_11.addWidget(self.line_amount)


        self.horizontalLayout_6.addWidget(self.frame_15)

        self.frame_17 = QFrame(self.frame_amounts)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_13.setSpacing(4)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_11 = QLabel(self.frame_17)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_13.addWidget(self.label_11)

        self.line_volume = QLineEdit(self.frame_17)
        self.line_volume.setObjectName(u"line_volume")
        self.line_volume.setMinimumSize(QSize(140, 22))
        self.line_volume.setMaximumSize(QSize(140, 22))

        self.horizontalLayout_13.addWidget(self.line_volume)


        self.horizontalLayout_6.addWidget(self.frame_17)


        self.verticalLayout.addWidget(self.frame_amounts)

        self.frame_comment = QFrame(self.frame_2)
        self.frame_comment.setObjectName(u"frame_comment")
        self.frame_comment.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_comment.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_comment)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_7 = QLabel(self.frame_comment)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_14.addWidget(self.label_7)

        self.line_comment = QLineEdit(self.frame_comment)
        self.line_comment.setObjectName(u"line_comment")
        self.line_comment.setMinimumSize(QSize(250, 22))
        self.line_comment.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_14.addWidget(self.line_comment)


        self.verticalLayout.addWidget(self.frame_comment)

        self.frame_ozon = QFrame(self.frame_2)
        self.frame_ozon.setObjectName(u"frame_ozon")
        self.frame_ozon.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_ozon.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_ozon)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_8 = QLabel(self.frame_ozon)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_16.addWidget(self.label_8)

        self.line_ozon = QLineEdit(self.frame_ozon)
        self.line_ozon.setObjectName(u"line_ozon")
        self.line_ozon.setMinimumSize(QSize(250, 22))
        self.line_ozon.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_16.addWidget(self.line_ozon)


        self.verticalLayout.addWidget(self.frame_ozon)

        self.frame_buttons = QFrame(self.frame_2)
        self.frame_buttons.setObjectName(u"frame_buttons")
        self.frame_buttons.setMinimumSize(QSize(0, 45))
        self.frame_buttons.setMaximumSize(QSize(16777215, 45))
        self.frame_buttons.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_buttons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_buttons)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.btn_save = QPushButton(self.frame_buttons)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setMinimumSize(QSize(110, 30))
        self.btn_save.setMaximumSize(QSize(110, 30))
        icon = QIcon()
        icon.addFile(u":/icon/icon/check-circle \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_save.setIcon(icon)

        self.horizontalLayout_15.addWidget(self.btn_save)

        self.btn_cancel = QPushButton(self.frame_buttons)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setMinimumSize(QSize(110, 30))
        self.btn_cancel.setMaximumSize(QSize(110, 30))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/x-circle \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_cancel.setIcon(icon1)

        self.horizontalLayout_15.addWidget(self.btn_cancel)


        self.verticalLayout.addWidget(self.frame_buttons)


        self.horizontalLayout_17.addWidget(self.frame_2)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Title_label.setText(QCoreApplication.translate("Form", u"\u0424\u043e\u0440\u043c\u0430 \u0434\u043b\u044f \u0437\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0438 \u0434\u043e \u043a\u043b\u0438\u0435\u043d\u0442\u0430", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u0414\u0430\u0442\u0430 \u043e\u0442\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u0421\u0447\u0435\u0442", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043d\u0442\u0440\u0430\u0433\u0435\u043d\u0442", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u0418\u041d\u041d", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u0421\u0431\u043e\u0440\u043a\u0430", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u2116 \u0422\u0421", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u0421\u0442\u0430\u0432\u043a\u0430, \u0440\u0443\u0431 (\u0441 \u041d\u0414\u0421 20%)", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u041e\u0431\u044a\u0435\u043c \u0437\u0430\u043a\u0430\u0437\u0430, \u043b", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043c\u043c\u0435\u043d\u0442\u0430\u0440\u0438\u0439", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u041e\u0417\u041e\u041d", None))
        self.btn_save.setText(QCoreApplication.translate("Form", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_cancel.setText(QCoreApplication.translate("Form", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

