# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'commission_create_formqbnDwd.ui'
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
    QGridLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)
from wind import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(682, 453)
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
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.widget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
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

        self.verticalLayout_4.addWidget(self.Title_label)

        self.frame_customer = QFrame(self.frame_2)
        self.frame_customer.setObjectName(u"frame_customer")
        self.frame_customer.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_customer.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.frame_customer)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.frame_customer)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(400, 0))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setSpacing(4)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(100, 0))
        self.label.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_2.addWidget(self.label)

        self.line_cust_code = QLineEdit(self.frame)
        self.line_cust_code.setObjectName(u"line_cust_code")
        self.line_cust_code.setMinimumSize(QSize(0, 22))
        self.line_cust_code.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_2.addWidget(self.line_cust_code)


        self.gridLayout_3.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.frame_customer)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.frame_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.line_date_start = QDateEdit(self.frame_5)
        self.line_date_start.setObjectName(u"line_date_start")
        self.line_date_start.setMinimumSize(QSize(104, 22))
        self.line_date_start.setMaximumSize(QSize(16777215, 22))
        font1 = QFont()
        font1.setFamilies([u"Tahoma"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setKerning(False)
        self.line_date_start.setFont(font1)
        self.line_date_start.setCalendarPopup(True)

        self.horizontalLayout_5.addWidget(self.line_date_start)


        self.gridLayout_3.addWidget(self.frame_5, 0, 1, 1, 1)

        self.frame_3 = QFrame(self.frame_customer)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(400, 0))
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(100, 0))
        self.label_2.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.line_cust_name = QComboBox(self.frame_3)
        self.line_cust_name.setObjectName(u"line_cust_name")
        self.line_cust_name.setMinimumSize(QSize(250, 22))
        self.line_cust_name.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_3.addWidget(self.line_cust_name)


        self.gridLayout_3.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_6 = QFrame(self.frame_customer)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(200, 0))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.frame_6)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.line_date_end = QDateEdit(self.frame_6)
        self.line_date_end.setObjectName(u"line_date_end")
        self.line_date_end.setMinimumSize(QSize(104, 22))
        self.line_date_end.setMaximumSize(QSize(16777215, 22))
        self.line_date_end.setCalendarPopup(True)

        self.horizontalLayout_6.addWidget(self.line_date_end)


        self.gridLayout_3.addWidget(self.frame_6, 1, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.frame_customer)

        self.frame_product = QFrame(self.frame_2)
        self.frame_product.setObjectName(u"frame_product")
        self.frame_product.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_product.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_product.setLineWidth(0)
        self.gridLayout_2 = QGridLayout(self.frame_product)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_product)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(230, 0))
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setSpacing(4)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_5 = QLabel(self.frame_8)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_7.addWidget(self.label_5)

        self.line_prodCode = QLineEdit(self.frame_8)
        self.line_prodCode.setObjectName(u"line_prodCode")
        self.line_prodCode.setMinimumSize(QSize(150, 22))
        self.line_prodCode.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_7.addWidget(self.line_prodCode)


        self.gridLayout_2.addWidget(self.frame_8, 0, 0, 1, 1)

        self.frame_9 = QFrame(self.frame_product)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_9.setSpacing(4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_7 = QLabel(self.frame_9)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_9.addWidget(self.label_7)

        self.line_prod_name = QComboBox(self.frame_9)
        self.line_prod_name.setObjectName(u"line_prod_name")
        self.line_prod_name.setMinimumSize(QSize(250, 22))
        self.line_prod_name.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_9.addWidget(self.line_prod_name)


        self.gridLayout_2.addWidget(self.frame_9, 0, 1, 1, 1)

        self.frame_11 = QFrame(self.frame_product)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setMinimumSize(QSize(230, 0))
        self.frame_11.setMaximumSize(QSize(16777215, 16777215))
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_8.setSpacing(4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_6 = QLabel(self.frame_11)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_8.addWidget(self.label_6)

        self.line_article = QLineEdit(self.frame_11)
        self.line_article.setObjectName(u"line_article")
        self.line_article.setMinimumSize(QSize(150, 22))
        self.line_article.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_8.addWidget(self.line_article)


        self.gridLayout_2.addWidget(self.frame_11, 1, 0, 1, 1)

        self.frame_10 = QFrame(self.frame_product)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_10.setSpacing(4)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_8 = QLabel(self.frame_10)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_10.addWidget(self.label_8)

        self.line_prod_group = QComboBox(self.frame_10)
        self.line_prod_group.setObjectName(u"line_prod_group")
        self.line_prod_group.setMinimumSize(QSize(250, 22))
        self.line_prod_group.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_10.addWidget(self.line_prod_group)


        self.gridLayout_2.addWidget(self.frame_10, 1, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.frame_product)

        self.frame_commis = QFrame(self.frame_2)
        self.frame_commis.setObjectName(u"frame_commis")
        self.frame_commis.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_commis.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout = QGridLayout(self.frame_commis)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_15 = QFrame(self.frame_commis)
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

        self.line_commis_rub = QLineEdit(self.frame_15)
        self.line_commis_rub.setObjectName(u"line_commis_rub")
        self.line_commis_rub.setMinimumSize(QSize(0, 22))
        self.line_commis_rub.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_11.addWidget(self.line_commis_rub)


        self.gridLayout.addWidget(self.frame_15, 0, 0, 1, 1)

        self.frame_17 = QFrame(self.frame_commis)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_13.setSpacing(4)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_11 = QLabel(self.frame_17)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_13.addWidget(self.label_11)

        self.line_cost_rub = QLineEdit(self.frame_17)
        self.line_cost_rub.setObjectName(u"line_cost_rub")
        self.line_cost_rub.setMinimumSize(QSize(0, 22))
        self.line_cost_rub.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_13.addWidget(self.line_cost_rub)


        self.gridLayout.addWidget(self.frame_17, 0, 1, 1, 1)

        self.frame_16 = QFrame(self.frame_commis)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_12.setSpacing(4)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_10 = QLabel(self.frame_16)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_12.addWidget(self.label_10)

        self.line_commis_pers = QLineEdit(self.frame_16)
        self.line_commis_pers.setObjectName(u"line_commis_pers")
        self.line_commis_pers.setMinimumSize(QSize(0, 22))
        self.line_commis_pers.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_12.addWidget(self.line_commis_pers)


        self.gridLayout.addWidget(self.frame_16, 1, 0, 1, 1)

        self.frame_18 = QFrame(self.frame_commis)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_14.setSpacing(4)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_12 = QLabel(self.frame_18)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_14.addWidget(self.label_12)

        self.line_cost_perc = QLineEdit(self.frame_18)
        self.line_cost_perc.setObjectName(u"line_cost_perc")
        self.line_cost_perc.setMinimumSize(QSize(0, 22))
        self.line_cost_perc.setMaximumSize(QSize(16777215, 22))

        self.horizontalLayout_14.addWidget(self.line_cost_perc)


        self.gridLayout.addWidget(self.frame_18, 1, 1, 1, 1)


        self.verticalLayout_4.addWidget(self.frame_commis)

        self.frame_7 = QFrame(self.frame_2)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 45))
        self.frame_7.setMaximumSize(QSize(16777215, 45))
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_15 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.btn_save = QPushButton(self.frame_7)
        self.btn_save.setObjectName(u"btn_save")
        self.btn_save.setMinimumSize(QSize(110, 30))
        self.btn_save.setMaximumSize(QSize(110, 30))
        icon = QIcon()
        icon.addFile(u":/icon/icon/check-circle \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_save.setIcon(icon)

        self.horizontalLayout_15.addWidget(self.btn_save)

        self.btn_cancel = QPushButton(self.frame_7)
        self.btn_cancel.setObjectName(u"btn_cancel")
        self.btn_cancel.setMinimumSize(QSize(110, 30))
        self.btn_cancel.setMaximumSize(QSize(110, 30))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/x-circle \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_cancel.setIcon(icon1)

        self.horizontalLayout_15.addWidget(self.btn_cancel)


        self.verticalLayout_4.addWidget(self.frame_7)


        self.verticalLayout.addWidget(self.frame_2)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Title_label.setText(QCoreApplication.translate("Form", u"\u0424\u043e\u0440\u043c\u0430 \u0434\u043b\u044f \u0437\u0430\u0432\u0435\u0434\u0435\u043d\u0438\u044f \u043d\u043e\u0432\u043e\u0439 \u041a\u043e\u043c\u0438\u0441\u0441\u0438\u0438", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043d\u0442\u0440\u0430\u0433\u0435\u043d\u0442.\u041a\u043e\u0434", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u0414\u0430\u0442\u0430 \u043d\u0430\u0447\u0430\u043b\u0430", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043d\u0442\u0440\u0430\u0433\u0435\u043d\u0442", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u0414\u0430\u0442\u0430 \u043e\u043a\u043e\u043d\u0447\u0430\u043d\u0438\u044f", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u0434 1\u0421", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u041f\u0440\u043e\u0434\u0443\u043a\u0442", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u0410\u0440\u0442\u0438\u043a\u0443\u043b", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"Prod.Name", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043c\u0438\u0441\u0441\u0438\u044f, \u0440\u0443\u0431", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u0421\u0442-\u0442\u044c \u043a\u043e\u043c\u0438\u0441., \u0440\u0443\u0431", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043c\u0438\u0441\u0441\u0438\u044f, %", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u0421\u0442-\u0442\u044c \u043a\u043e\u043c\u0438\u0441., %", None))
        self.btn_save.setText(QCoreApplication.translate("Form", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
        self.btn_cancel.setText(QCoreApplication.translate("Form", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
    # retranslateUi

