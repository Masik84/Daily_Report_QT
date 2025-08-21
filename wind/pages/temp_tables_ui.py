# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'temp_tablesBuJGAM.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QComboBox,
    QDateEdit, QFrame, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)
import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1102, 710)
        Form.setMinimumSize(QSize(930, 650))
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
"}\n"
"QTableWidget::item:selected{\n"
"	background-co"
                        "lor: #f6c294;\n"
"    color: #262626;\n"
"}\n"
"QHeaderView::section{\n"
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
""
                        "	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
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
""
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
" "
                        "    background: none;\n"
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
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    "
                        " background: none;\n"
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
"    border-left-color: #f8994a;\n"
"    border-left-style: solid;\n"
"    border-top-right-radius: 3px;\n"
"    border-bottom-right-radius: 3px;\n"
"    background-color: #f8f8f2;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"	image: url(:/icon/icon/chevron-down \u2014 \u043a\u043e"
                        "\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg);\n"
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
"    color: #ffffff;\n"
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
"    border: 1px solid #f09"
                        "d54;\n"
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
"QCalendarWidget QSpinBox::down-arrow {\n"
"	image: url(:/icon/icon/chevron-down \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg);\n"
"    width: 10px;\n"
"    height: 10px;\n"
"}\n"
"")
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
        font.setPointSize(18)
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
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(9, 0, 0, 9)
        self.frame_6 = QFrame(self.frame_Search)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_6)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(80, 0))
        self.frame_4.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 6, -1, 6)
        self.label_6 = QLabel(self.frame_4)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_5.addWidget(self.label_6)

        self.label_8 = QLabel(self.frame_4)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_5.addWidget(self.label_8)

        self.label_7 = QLabel(self.frame_4)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_5.addWidget(self.label_7)


        self.horizontalLayout_2.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_6)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(250, 120))
        self.frame_5.setMaximumSize(QSize(300, 16777215))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.line_table = QComboBox(self.frame_5)
        self.line_table.setObjectName(u"line_table")
        self.line_table.setMinimumSize(QSize(0, 25))
        self.line_table.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.line_table)

        self.line_article = QLineEdit(self.frame_5)
        self.line_article.setObjectName(u"line_article")
        self.line_article.setMinimumSize(QSize(0, 25))
        self.line_article.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.line_article)

        self.line_product = QComboBox(self.frame_5)
        self.line_product.setObjectName(u"line_product")
        self.line_product.setMinimumSize(QSize(0, 25))
        self.line_product.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.line_product)


        self.horizontalLayout_2.addWidget(self.frame_5)


        self.horizontalLayout_5.addWidget(self.frame_6)

        self.horizontalSpacer_3 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.frame = QFrame(self.frame_Search)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(80, 0))
        self.frame.setMaximumSize(QSize(16777215, 16777215))
        font1 = QFont()
        font1.setPointSize(1)
        self.frame.setFont(font1)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 6, 9, 6)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        font2 = QFont()
        font2.setFamilies([u"Tahoma"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.label_3.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font2)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_5 = QLabel(self.frame)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font2)

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
        self.line_doc_type = QComboBox(self.frame_2)
        self.line_doc_type.setObjectName(u"line_doc_type")
        self.line_doc_type.setMinimumSize(QSize(0, 25))
        self.line_doc_type.setMaximumSize(QSize(16777215, 25))
        self.line_doc_type.setIconSize(QSize(16, 16))

        self.verticalLayout_3.addWidget(self.line_doc_type)

        self.line_Year = QComboBox(self.frame_2)
        self.line_Year.setObjectName(u"line_Year")
        self.line_Year.setMinimumSize(QSize(0, 25))
        self.line_Year.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_3.addWidget(self.line_Year)

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
        self.frame_pcs = QFrame(self.frame_7)
        self.frame_pcs.setObjectName(u"frame_pcs")
        self.frame_pcs.setMinimumSize(QSize(300, 0))
        self.frame_pcs.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_pcs.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_pcs)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.frame_pcs)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(70, 0))
        self.label_11.setMaximumSize(QSize(70, 16777215))

        self.horizontalLayout_8.addWidget(self.label_11)

        self.label_qty_pcs = QLabel(self.frame_pcs)
        self.label_qty_pcs.setObjectName(u"label_qty_pcs")
        self.label_qty_pcs.setStyleSheet(u"QLabel {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	color: #964b09;\n"
"	font: 700 10pt \"Tahoma\";\n"
"}")
        self.label_qty_pcs.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_8.addWidget(self.label_qty_pcs)


        self.horizontalLayout_3.addWidget(self.frame_pcs)

        self.frame_Vol = QFrame(self.frame_7)
        self.frame_Vol.setObjectName(u"frame_Vol")
        self.frame_Vol.setMinimumSize(QSize(300, 0))
        self.frame_Vol.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Vol.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_Vol)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.frame_Vol)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(70, 0))
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

        self.horizontalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.date_Start = QDateEdit(self.frame_7)
        self.date_Start.setObjectName(u"date_Start")
        self.date_Start.setMinimumSize(QSize(104, 32))
        font3 = QFont()
        font3.setFamilies([u"Tahoma"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        font3.setKerning(False)
        self.date_Start.setFont(font3)
        self.date_Start.setMinimumDate(QDate(2022, 1, 1))
        self.date_Start.setCalendarPopup(True)

        self.horizontalLayout_3.addWidget(self.date_Start)

        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(162, 0))
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_8)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.btn_refresh = QPushButton(self.frame_8)
        self.btn_refresh.setObjectName(u"btn_refresh")
        self.btn_refresh.setMinimumSize(QSize(160, 30))
        self.btn_refresh.setMaximumSize(QSize(160, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/refresh-ccw \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_refresh.setIcon(icon1)

        self.horizontalLayout_9.addWidget(self.btn_refresh)


        self.horizontalLayout_3.addWidget(self.frame_8)

        self.horizontalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addWidget(self.frame_7)

        self.table = QTableWidget(self.widget)
        self.table.setObjectName(u"table")
        font4 = QFont()
        font4.setFamilies([u"Tahoma"])
        font4.setPointSize(10)
        self.table.setFont(font4)
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


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Title_label.setText(QCoreApplication.translate("Form", u"\u0412\u0440\u0435\u043c\u0435\u043d\u043d\u044b\u0435 \u0442\u0430\u0431\u043b\u0438\u0446\u044b (\u0417\u0430\u043a\u0443\u043f\u043a\u0438, \u041f\u0440\u043e\u0434\u0430\u0436\u0438, \u0417\u0430\u043a\u0430\u0437\u044b)", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u0422\u0430\u0431\u043b\u0438\u0446\u0430", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u0410\u0440\u0442\u0438\u043a\u0443\u043b", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u041f\u0440\u043e\u0434\u0443\u043a\u0442", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u0422\u0438\u043f \u0434\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u0430", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u0413\u043e\u0434", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u041c\u0435\u0441\u044f\u0446", None))
        self.btn_find.setText(QCoreApplication.translate("Form", u"Search", None))
        self.label_11.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043b-\u0432\u043e, \u0448\u0442", None))
        self.label_qty_pcs.setText("")
        self.label_9.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u043b-\u0432\u043e, \u043b", None))
        self.label_Volume.setText("")
        self.btn_refresh.setText(QCoreApplication.translate("Form", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0434\u0430\u043d\u043d\u044b\u0435", None))
    # retranslateUi

