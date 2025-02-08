# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'plansDqWiVq.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)
from wind import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1074, 710)
        Form.setMinimumSize(QSize(930, 650))
        Form.setStyleSheet(u"QWidget{\n"
"	background-color: #f8f8f2;\n"
"}\n"
"\n"
"#Title_label.QLabel {\n"
"color: #262626;\n"
"font: 22pt \"Tahoma\";\n"
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
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: #f6c294;\n"
"    color: #262626;\n"
"}\n"
"QH"
                        "eaderView::section{\n"
"	background-color: #f8f8f2;\n"
"	max-width: 30px;\n"
"	border: none;\n"
"	border-style: none;\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: #f8994a;\n"
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
"	selection-background-color: #f28223;\n"
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
"	padding-left: 10p"
                        "x;\n"
"	selection-color: #f28223;\n"
"	selection-background-color: #f28223;\n"
"    color: #262626;\n"
"	font: 10pt \"Tahoma\";\n"
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
"    width: 15px;\n"
"    border-left-width: 1px;\n"
"    border-left-color: #f8994a;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"	color: #262626;\n"
"}\n"
"\n"
"QScrollBar:hori"
                        "zontal {\n"
"    border: none;\n"
"    background: #f8994a;\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: #f6c294;\n"
"    min-width: 25px;\n"
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
" QScrollBar:ver"
                        "tical {\n"
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
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 9)
        self.Title_label = QLabel(self.widget)
        self.Title_label.setObjectName(u"Title_label")
        self.Title_label.setMinimumSize(QSize(0, 40))
        font = QFont()
        font.setFamilies([u"Tahoma"])
        font.setPointSize(22)
        font.setBold(False)
        font.setItalic(False)
        self.Title_label.setFont(font)
        self.Title_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.Title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.Title_label)

        self.frame_Search = QFrame(self.widget)
        self.frame_Search.setObjectName(u"frame_Search")
        self.frame_Search.setMinimumSize(QSize(0, 130))
        self.frame_Search.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_5 = QHBoxLayout(self.frame_Search)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(12, 0, 0, 5)
        self.frame = QFrame(self.frame_Search)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(80, 0))
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 9, 0)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        font1 = QFont()
        font1.setFamilies([u"Tahoma"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.label_3.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_4)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_5)


        self.horizontalLayout_5.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_Search)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(250, 120))
        self.frame_2.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.line_plan_type = QComboBox(self.frame_2)
        self.line_plan_type.addItem("")
        self.line_plan_type.addItem("")
        self.line_plan_type.addItem("")
        self.line_plan_type.setObjectName(u"line_plan_type")
        self.line_plan_type.setMinimumSize(QSize(0, 25))
        self.line_plan_type.setMaximumSize(QSize(16777215, 25))
        self.line_plan_type.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.line_plan_type)

        self.line_Year = QComboBox(self.frame_2)
        self.line_Year.setObjectName(u"line_Year")
        self.line_Year.setMinimumSize(QSize(0, 25))
        self.line_Year.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_3.addWidget(self.line_Year)

        self.line_Qtr = QComboBox(self.frame_2)
        self.line_Qtr.setObjectName(u"line_Qtr")
        self.line_Qtr.setMinimumSize(QSize(0, 25))
        self.line_Qtr.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_3.addWidget(self.line_Qtr)

        self.line_Mnth = QComboBox(self.frame_2)
        self.line_Mnth.setObjectName(u"line_Mnth")
        self.line_Mnth.setMinimumSize(QSize(0, 25))
        self.line_Mnth.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_3.addWidget(self.line_Mnth)


        self.horizontalLayout_5.addWidget(self.frame_2)

        self.horizontalSpacer = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.frame_3 = QFrame(self.frame_Search)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(100, 0))
        self.frame_3.setMaximumSize(QSize(93, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(1, 0, 1, 0)
        self.btn_find = QPushButton(self.frame_3)
        self.btn_find.setObjectName(u"btn_find")
        self.btn_find.setMinimumSize(QSize(97, 30))
        self.btn_find.setMaximumSize(QSize(92, 16777215))
        icon = QIcon()
        icon.addFile(u":/icon/icon/search \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_find.setIcon(icon)

        self.verticalLayout_4.addWidget(self.btn_find)


        self.horizontalLayout_5.addWidget(self.frame_3)

        self.horizontalSpacer_3 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.frame_6 = QFrame(self.frame_Search)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_5.addWidget(self.frame_6)

        self.frame_4 = QFrame(self.frame_Search)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(80, 0))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, -1, 0)
        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_5.addWidget(self.label_6)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_5.addWidget(self.label_7)

        self.label = QLabel(self.frame_4)
        self.label.setObjectName(u"label")

        self.verticalLayout_5.addWidget(self.label)

        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_5.addWidget(self.label_8)


        self.horizontalLayout_5.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_Search)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(250, 120))
        self.frame_5.setMaximumSize(QSize(300, 16777215))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.line_tl = QComboBox(self.frame_5)
        self.line_tl.setObjectName(u"line_tl")
        self.line_tl.setMinimumSize(QSize(0, 25))
        self.line_tl.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.line_tl)

        self.line_kam = QComboBox(self.frame_5)
        self.line_kam.setObjectName(u"line_kam")
        self.line_kam.setMinimumSize(QSize(0, 25))
        self.line_kam.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.line_kam)

        self.line_Holding = QComboBox(self.frame_5)
        self.line_Holding.setObjectName(u"line_Holding")
        self.line_Holding.setMinimumSize(QSize(0, 25))
        self.line_Holding.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.line_Holding)

        self.line_ABC = QComboBox(self.frame_5)
        self.line_ABC.setObjectName(u"line_ABC")
        self.line_ABC.setMinimumSize(QSize(0, 25))
        self.line_ABC.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.line_ABC)


        self.horizontalLayout_5.addWidget(self.frame_5)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.frame_Search)

        self.frame_7 = QFrame(self.widget)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 40))
        self.frame_7.setStyleSheet(u"")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, 0, 9, 0)
        self.frame_Vol = QFrame(self.frame_7)
        self.frame_Vol.setObjectName(u"frame_Vol")
        self.frame_Vol.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Vol.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_Vol)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_Vol)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(50, 0))
        self.label_9.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.label_9)

        self.label_Volume = QLabel(self.frame_Vol)
        self.label_Volume.setObjectName(u"label_Volume")
        self.label_Volume.setStyleSheet(u"QLabel {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	color: #964b09;\n"
"	font: 700 10pt \"Tahoma\";\n"
"}")
        self.label_Volume.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_Volume)


        self.horizontalLayout_3.addWidget(self.frame_Vol)

        self.frame_Revenue = QFrame(self.frame_7)
        self.frame_Revenue.setObjectName(u"frame_Revenue")
        self.frame_Revenue.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Revenue.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_Revenue)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.frame_Revenue)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(70, 0))
        self.label_11.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_8.addWidget(self.label_11)

        self.label_Revenue = QLabel(self.frame_Revenue)
        self.label_Revenue.setObjectName(u"label_Revenue")
        self.label_Revenue.setStyleSheet(u"QLabel {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	color: #964b09;\n"
"	font: 700 10pt \"Tahoma\";\n"
"}")
        self.label_Revenue.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_Revenue)


        self.horizontalLayout_3.addWidget(self.frame_Revenue)

        self.frame_Margin = QFrame(self.frame_7)
        self.frame_Margin.setObjectName(u"frame_Margin")
        self.frame_Margin.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Margin.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_Margin)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.frame_Margin)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(80, 0))
        self.label_13.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout_9.addWidget(self.label_13)

        self.label_Margin = QLabel(self.frame_Margin)
        self.label_Margin.setObjectName(u"label_Margin")
        self.label_Margin.setStyleSheet(u"QLabel {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	color: #964b09;\n"
"	font: 700 10pt \"Tahoma\";\n"
"}")
        self.label_Margin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_9.addWidget(self.label_Margin)


        self.horizontalLayout_3.addWidget(self.frame_Margin)

        self.frame_uC3 = QFrame(self.frame_7)
        self.frame_uC3.setObjectName(u"frame_uC3")
        self.frame_uC3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_uC3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_uC3)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 9, 0)
        self.label_15 = QLabel(self.frame_uC3)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(50, 0))
        self.label_15.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_10.addWidget(self.label_15)

        self.label_uC3 = QLabel(self.frame_uC3)
        self.label_uC3.setObjectName(u"label_uC3")
        self.label_uC3.setStyleSheet(u"QLabel {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	color: #964b09;\n"
"	font: 700 10pt \"Tahoma\";\n"
"}")
        self.label_uC3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_10.addWidget(self.label_uC3)


        self.horizontalLayout_3.addWidget(self.frame_uC3)


        self.verticalLayout.addWidget(self.frame_7)

        self.table = QTableWidget(self.widget)
        self.table.setObjectName(u"table")
        font2 = QFont()
        font2.setFamilies([u"Tahoma"])
        font2.setPointSize(10)
        self.table.setFont(font2)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.setAutoScrollMargin(10)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        self.table.setColumnCount(0)
        self.table.horizontalHeader().setCascadingSectionResizes(True)
        self.table.horizontalHeader().setMinimumSectionSize(55)
        self.table.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setCascadingSectionResizes(True)
        self.table.verticalHeader().setMinimumSectionSize(25)
        self.table.verticalHeader().setDefaultSectionSize(25)
        self.table.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.table)

        self.frame_9 = QFrame(self.widget)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_9)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(12, 0, 0, 0)
        self.label_plan_File = QLabel(self.frame_9)
        self.label_plan_File.setObjectName(u"label_plan_File")
        self.label_plan_File.setMinimumSize(QSize(0, 30))
        self.label_plan_File.setMaximumSize(QSize(16777215, 30))
        self.label_plan_File.setStyleSheet(u"QLabel {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	color: #964b09;\n"
"	font: 10pt \"Tahoma\";\n"
"}")

        self.horizontalLayout_7.addWidget(self.label_plan_File)

        self.frame_10 = QFrame(self.frame_9)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setMinimumSize(QSize(220, 0))
        self.frame_10.setMaximumSize(QSize(220, 16777215))
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_10)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.btn_open_file = QPushButton(self.frame_10)
        self.btn_open_file.setObjectName(u"btn_open_file")
        self.btn_open_file.setMinimumSize(QSize(90, 30))
        self.btn_open_file.setMaximumSize(QSize(90, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/folder \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_open_file.setIcon(icon1)

        self.horizontalLayout_6.addWidget(self.btn_open_file)

        self.btn_upload_file = QPushButton(self.frame_10)
        self.btn_upload_file.setObjectName(u"btn_upload_file")
        self.btn_upload_file.setMinimumSize(QSize(90, 30))
        self.btn_upload_file.setMaximumSize(QSize(90, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/icon/icon/upload \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_upload_file.setIcon(icon2)

        self.horizontalLayout_6.addWidget(self.btn_upload_file)


        self.horizontalLayout_7.addWidget(self.frame_10)


        self.verticalLayout.addWidget(self.frame_9)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Title_label.setText(QCoreApplication.translate("Form", u"\u041f\u043b\u0430\u043d\u044b", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u0422\u0438\u043f \u041f\u043b\u0430\u043d\u0430", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u0413\u043e\u0434", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u041a\u0432\u0430\u0440\u0442\u0430\u043b", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u041c\u0435\u0441\u044f\u0446", None))
        self.line_plan_type.setItemText(0, QCoreApplication.translate("Form", u"-", None))
        self.line_plan_type.setItemText(1, QCoreApplication.translate("Form", u"\u041f\u043b\u0430\u043d \u041e\u0431\u0449\u0438\u0439", None))
        self.line_plan_type.setItemText(2, QCoreApplication.translate("Form", u"\u041f\u043b\u0430\u043d \u041a\u0410\u041c-\u041a\u043b\u0438\u0435\u043d\u0442", None))

        self.btn_find.setText(QCoreApplication.translate("Form", u"Search", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Team Lead", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u041a\u0410\u041c", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u0425\u043e\u043b\u0434\u0438\u043d\u0433", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f D", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u041e\u0431\u044a\u0435\u043c:", None))
        self.label_Volume.setText("")
        self.label_11.setText(QCoreApplication.translate("Form", u"\u0412\u044b\u0440\u0443\u0447\u043a\u0430:", None))
        self.label_Revenue.setText("")
        self.label_13.setText(QCoreApplication.translate("Form", u"\u041c\u0430\u0440\u0436\u0430 \u04213:", None))
        self.label_Margin.setText("")
        self.label_15.setText(QCoreApplication.translate("Form", u"uC3:", None))
        self.label_uC3.setText("")
        self.label_plan_File.setText(QCoreApplication.translate("Form", u"\u0412\u044b\u0431\u0435\u0440\u0438 \u0444\u0430\u0439\u043b \u0438\u043b\u0438 \u043d\u0430\u0436\u043c\u0438 Upload, \u0444\u0430\u0439\u043b \u0431\u0443\u0434\u0435\u0442 \u0432\u0437\u044f\u0442 \u0438\u0437 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u043f\u0430\u043f\u043a\u0438", None))
        self.btn_open_file.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_upload_file.setText(QCoreApplication.translate("Form", u"Upload", None))
    # retranslateUi

