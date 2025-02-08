# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'invoicedpaHQW.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)
from wind import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(930, 650)
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
        self.verticalLayout_4 = QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setStyleSheet(u"#frame_cust_ksss {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	border-color: #bd93f9;\n"
"}\n"
"\n"
"#frame_deliv_date {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	border-color: #bd93f9;\n"
"}\n"
"\n"
"#frame_inv_date {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	border-color: #bd93f9;\n"
"}\n"
"\n"
"#frame_brand {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	border-color: #bd93f9;\n"
"}\n"
"\n"
"#frame_pr_group {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	border-color: #bd93f9;\n"
"}\n"
"\n"
"#frame_pr_segment {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	border-color: #bd93f9;\n"
"}\n"
"\n"
"#frame_luk_cust {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	border-color: #bd93f9;\n"
"}\n"
"\n"
"#frame_teboil_cust {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	bo"
                        "rder-color: #bd93f9;\n"
"}\n"
"\n"
"QDateEdit {\n"
"	border : 2px solid #6272a4;\n"
"	border-radius: 5px;\n"
"	background-color : #f8f8f2;\n"
"	padding : 5px;\n"
"}\n"
"\n"
"QDateEdit::up-arrow {\n"
"	border: 1px solid #6272a4;\n"
"	border-radius: 2px;\n"
"	background-color: #6272a4;\n"
"	color: #f8f8f2;\n"
"}\n"
"\n"
"QDateEdit::down-arrow {\n"
"	border: 1px solid #6272a4;\n"
"	border-radius: 2px;\n"
"	background-color: #6272a4;\n"
"	color: #f8f8f2;\n"
"}\n"
"\n"
"\n"
"\n"
"/* Style for header area  ####################################################*/ \n"
"\n"
"QCalendarWidget QWidget {\n"
"	 alternate-background-color: #8ea6ee;\n"
"	\n"
"}\n"
"\n"
"/* style for top navigation area ###############################################*/ \n"
"\n"
"#qt_calendar_navigationbar {\n"
"    background-color: #6272a4;\n"
"	border: 2px solid  #6272a4;\n"
"	border-bottom: 0px;\n"
"	border-top-left-radius: 5px;\n"
"	border-top-right-radius: 5px;\n"
"}\n"
"\n"
"/* style for month change buttons ###############################"
                        "############# */\n"
"\n"
"#qt_calendar_prevmonth, \n"
"#qt_calendar_nextmonth {\n"
"	/* border delete */\n"
"    border: none;  \n"
"    /* delete default icons */\n"
"	qproperty-icon: none; \n"
"	\n"
"    min-width: 13px;\n"
"    max-width: 13px;\n"
"    min-height: 13px;\n"
"    max-height: 13px;\n"
"\n"
"    border-radius: 5px; \n"
"	/* set background transparent */\n"
"    background-color: transparent; \n"
"	padding: 5px;\n"
"}\n"
"\n"
"/* style for pre month button ############################################ */\n"
"\n"
"#qt_calendar_prevmonth {\n"
"	/* set text for button */\n"
"	/*qproperty-text: \">\";*/\n"
"	margin-left:5px;\n"
"	image: url(:/icon/icon/chevrons-left.svg);\n"
"}\n"
"\n"
"/* style for next month button ########################################### */\n"
"#qt_calendar_nextmonth {\n"
"	margin-right:5px;\n"
"	\n"
"	image: url(:/icon/icon/chevrons-right.svg);\n"
"    /* qproperty-text: \">\"; */\n"
"}\n"
"#qt_calendar_prevmonth:hover, \n"
"#qt_calendar_nextmonth:hover {\n"
"    background-co"
                        "lor: #bd93f9;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth:pressed, \n"
"#qt_calendar_nextmonth:pressed {\n"
"    background-color: #ff79c6;\n"
"	color: rgb(255, 255, 255)\n"
"}\n"
"\n"
"\n"
"/* Style for month and yeat buttons #################################### */\n"
"\n"
"#qt_calendar_yearbutton {\n"
"    color: #f8f8f2;\n"
"	margin:5px;\n"
"    border-radius: 5px;\n"
"	/*font-size: 15px;*/\n"
"	padding:0px 10px;\n"
"}\n"
"\n"
" #qt_calendar_monthbutton {\n"
"	width: 110px;\n"
"    color: #f8f8f2;\n"
"	/*font-size: 15px;*/\n"
"	margin:5px 0px;\n"
"    border-radius: 5px;\n"
"	padding:0px 2px;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton:hover, \n"
"#qt_calendar_monthbutton:hover {\n"
"    background-color: #bd93f9;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton:pressed, \n"
"#qt_calendar_monthbutton:pressed {\n"
"    background-color: #ff79c6;\n"
"	color: rgb(255, 255, 255)\n"
"}\n"
"\n"
"/* Style for year input lineEdit ######################################*/\n"
"\n"
"#qt_calendar_yearedit {\n"
"    min-width: 53px;\n"
"    "
                        "color: #000;\n"
"    background: transparent;\n"
"	font-size: 13px;\n"
"}\n"
"\n"
"/* Style for year change buttons ######################################*/\n"
"\n"
"#qt_calendar_yearedit::up-button {\n"
"	image: url(:/icon/icon/chevron-up.svg);\n"
"    subcontrol-position: right;\n"
"}\n"
"\n"
"#qt_calendar_yearedit::down-button { \n"
"	image: url(:/icon/icon/chevron-down.svg);\n"
"    subcontrol-position: left; \n"
"}\n"
"\n"
"#qt_calendar_yearedit::down-button, \n"
"#qt_calendar_yearedit::up-button {\n"
"	width:10px;\n"
"	padding: 0px 5px;\n"
"	border-radius:3px;\n"
"}\n"
"\n"
"#qt_calendar_yearedit::down-button:hover, \n"
"#qt_calendar_yearedit::up-button:hover {\n"
"	background-color: #bd93f9;\n"
"}\n"
"\n"
"/* Style for month select menu ##################################### */\n"
"\n"
"#calendarWidget QToolButton QMenu {\n"
"     background-color: white;\n"
"\n"
"}\n"
"#calendarWidget QToolButton QMenu::item {\n"
"	/*padding: 10px;*/\n"
"}\n"
" #calendarWidget QToolButton QMenu::item:selected:enabled {\n"
""
                        "	background-color: #bd93f9;\n"
"	border: 2px solid #7082b6;\n"
"	color: rgb(255, 255, 255)\n"
"}\n"
"\n"
"#calendarWidget QToolButton::menu-indicator {\n"
"	/* Remove toolButton arrow */\n"
"      /*image: none; */\n"
"	nosubcontrol-origin: margin;\n"
"	subcontrol-position: right center;\n"
"	margin-top: 10px;\n"
"	width:20px;\n"
"}\n"
"\n"
"/* Style for calendar table ########################################## */\n"
"#qt_calendar_calendarview {\n"
"	/* Remove the selected dashed box */\n"
"    outline: 0px;\n"
"\n"
"	border: 2px solid  #6272a4;\n"
"	border-top: 0px;\n"
"	border-bottom-left-radius: 5px;\n"
"	border-bottom-right-radius: 5px;\n"
"}\n"
"\n"
"#qt_calendar_calendarview::item:hover {\n"
"   border-radius:5px;\n"
"	background-color:#bd93f9\n"
"}\n"
"\n"
"#qt_calendar_calendarview::item:selected {\n"
"    background-color: #ff79c6;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"")
        self.verticalLayout_15 = QVBoxLayout(self.widget)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(6, 6, 6, 6)
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_15.addWidget(self.label)

        self.frame_17 = QFrame(self.widget)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_17)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.frame_Search = QFrame(self.frame_17)
        self.frame_Search.setObjectName(u"frame_Search")
        self.frame_Search.setMinimumSize(QSize(0, 0))
        self.frame_Search.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_12 = QVBoxLayout(self.frame_Search)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.frame_dates = QFrame(self.frame_Search)
        self.frame_dates.setObjectName(u"frame_dates")
        self.frame_dates.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_dates.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_dates)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_inv_date = QFrame(self.frame_dates)
        self.frame_inv_date.setObjectName(u"frame_inv_date")
        self.frame_inv_date.setMinimumSize(QSize(150, 0))
        self.frame_inv_date.setMaximumSize(QSize(16777215, 16777215))
        self.frame_inv_date.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_inv_date.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_inv_date)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_7 = QLabel(self.frame_inv_date)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(0, 35))
        self.label_7.setMaximumSize(QSize(16777215, 35))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_7.setFont(font1)
        self.label_7.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_7)

        self.frame_11 = QFrame(self.frame_inv_date)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_11)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.frame_12 = QFrame(self.frame_11)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.frame_12)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_3 = QLabel(self.frame_12)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 25))
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_3)

        self.line_inv_year = QComboBox(self.frame_12)
        self.line_inv_year.setObjectName(u"line_inv_year")
        self.line_inv_year.setMinimumSize(QSize(0, 25))
        self.line_inv_year.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_9.addWidget(self.line_inv_year)


        self.horizontalLayout_7.addWidget(self.frame_12)

        self.frame_13 = QFrame(self.frame_11)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.frame_13)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.label_8 = QLabel(self.frame_13)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMaximumSize(QSize(16777215, 25))
        self.label_8.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_10.addWidget(self.label_8)

        self.line_inv_qtr = QComboBox(self.frame_13)
        self.line_inv_qtr.setObjectName(u"line_inv_qtr")
        self.line_inv_qtr.setMinimumSize(QSize(0, 25))
        self.line_inv_qtr.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_10.addWidget(self.line_inv_qtr)


        self.horizontalLayout_7.addWidget(self.frame_13)

        self.frame_14 = QFrame(self.frame_11)
        self.frame_14.setObjectName(u"frame_14")
        self.frame_14.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_14.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.frame_14)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.label_9 = QLabel(self.frame_14)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMaximumSize(QSize(16777215, 25))
        self.label_9.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_11.addWidget(self.label_9)

        self.line_inv_mnth = QComboBox(self.frame_14)
        self.line_inv_mnth.setObjectName(u"line_inv_mnth")
        self.line_inv_mnth.setMinimumSize(QSize(0, 25))
        self.line_inv_mnth.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_11.addWidget(self.line_inv_mnth)


        self.horizontalLayout_7.addWidget(self.frame_14)


        self.verticalLayout_8.addWidget(self.frame_11)


        self.horizontalLayout_2.addWidget(self.frame_inv_date)

        self.frame_deliv_date = QFrame(self.frame_dates)
        self.frame_deliv_date.setObjectName(u"frame_deliv_date")
        self.frame_deliv_date.setMinimumSize(QSize(150, 0))
        self.frame_deliv_date.setMaximumSize(QSize(16777215, 16777215))
        self.frame_deliv_date.setStyleSheet(u"#frame_Period {\n"
"	border-width: 1;\n"
"	border-radius: 3;\n"
"	border-style: solid;\n"
"	border-color: #bd93f9;\n"
"}")
        self.frame_deliv_date.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_deliv_date.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_deliv_date)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.frame_deliv_date)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(0, 35))
        self.label_6.setMaximumSize(QSize(16777215, 35))
        self.label_6.setFont(font1)
        self.label_6.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_6)

        self.frame_7 = QFrame(self.frame_deliv_date)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.frame_7)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_8)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.frame_8)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 25))
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.label_2)

        self.line_del_year = QComboBox(self.frame_8)
        self.line_del_year.setObjectName(u"line_del_year")
        self.line_del_year.setMinimumSize(QSize(0, 25))
        self.line_del_year.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_2.addWidget(self.line_del_year)


        self.horizontalLayout_6.addWidget(self.frame_8)

        self.frame_9 = QFrame(self.frame_7)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_9)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_4 = QLabel(self.frame_9)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(16777215, 25))
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_4)

        self.line_del_qtr = QComboBox(self.frame_9)
        self.line_del_qtr.setObjectName(u"line_del_qtr")
        self.line_del_qtr.setMinimumSize(QSize(0, 25))
        self.line_del_qtr.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_3.addWidget(self.line_del_qtr)


        self.horizontalLayout_6.addWidget(self.frame_9)

        self.frame_10 = QFrame(self.frame_7)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_10)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_5 = QLabel(self.frame_10)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(16777215, 25))
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_5)

        self.line_del_mnth = QComboBox(self.frame_10)
        self.line_del_mnth.setObjectName(u"line_del_mnth")
        self.line_del_mnth.setMinimumSize(QSize(0, 25))
        self.line_del_mnth.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_6.addWidget(self.line_del_mnth)


        self.horizontalLayout_6.addWidget(self.frame_10)


        self.verticalLayout_7.addWidget(self.frame_7)


        self.horizontalLayout_2.addWidget(self.frame_deliv_date)


        self.verticalLayout_12.addWidget(self.frame_dates)

        self.frame_brand = QFrame(self.frame_Search)
        self.frame_brand.setObjectName(u"frame_brand")
        self.frame_brand.setMinimumSize(QSize(0, 50))
        self.frame_brand.setMaximumSize(QSize(16777215, 50))
        self.frame_brand.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_brand.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_brand)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_10 = QLabel(self.frame_brand)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(150, 0))
        self.label_10.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout.addWidget(self.label_10)

        self.line_brand = QComboBox(self.frame_brand)
        self.line_brand.addItem("")
        self.line_brand.addItem("")
        self.line_brand.addItem("")
        self.line_brand.addItem("")
        self.line_brand.addItem("")
        self.line_brand.setObjectName(u"line_brand")
        self.line_brand.setMinimumSize(QSize(350, 25))
        self.line_brand.setMaximumSize(QSize(350, 25))

        self.horizontalLayout.addWidget(self.line_brand)

        self.horizontalSpacer = QSpacerItem(237, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_12.addWidget(self.frame_brand)

        self.frame_pr_segment = QFrame(self.frame_Search)
        self.frame_pr_segment.setObjectName(u"frame_pr_segment")
        self.frame_pr_segment.setMinimumSize(QSize(0, 50))
        self.frame_pr_segment.setMaximumSize(QSize(16777215, 50))
        self.frame_pr_segment.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_pr_segment.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_pr_segment)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_12 = QLabel(self.frame_pr_segment)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(150, 0))
        self.label_12.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_9.addWidget(self.label_12)

        self.line_segment = QComboBox(self.frame_pr_segment)
        self.line_segment.addItem("")
        self.line_segment.addItem("")
        self.line_segment.addItem("")
        self.line_segment.addItem("")
        self.line_segment.addItem("")
        self.line_segment.addItem("")
        self.line_segment.addItem("")
        self.line_segment.addItem("")
        self.line_segment.setObjectName(u"line_segment")
        self.line_segment.setMinimumSize(QSize(350, 25))
        self.line_segment.setMaximumSize(QSize(350, 25))

        self.horizontalLayout_9.addWidget(self.line_segment)

        self.horizontalSpacer_3 = QSpacerItem(237, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_3)


        self.verticalLayout_12.addWidget(self.frame_pr_segment)

        self.frame_pr_group = QFrame(self.frame_Search)
        self.frame_pr_group.setObjectName(u"frame_pr_group")
        self.frame_pr_group.setMinimumSize(QSize(0, 50))
        self.frame_pr_group.setMaximumSize(QSize(16777215, 50))
        self.frame_pr_group.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_pr_group.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_pr_group)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_11 = QLabel(self.frame_pr_group)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setMinimumSize(QSize(150, 0))
        self.label_11.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_8.addWidget(self.label_11)

        self.line_pr_group = QComboBox(self.frame_pr_group)
        self.line_pr_group.setObjectName(u"line_pr_group")
        self.line_pr_group.setMinimumSize(QSize(350, 25))
        self.line_pr_group.setMaximumSize(QSize(350, 25))

        self.horizontalLayout_8.addWidget(self.line_pr_group)

        self.horizontalSpacer_2 = QSpacerItem(237, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)


        self.verticalLayout_12.addWidget(self.frame_pr_group)

        self.frame_cust_ksss = QFrame(self.frame_Search)
        self.frame_cust_ksss.setObjectName(u"frame_cust_ksss")
        self.frame_cust_ksss.setMinimumSize(QSize(0, 50))
        self.frame_cust_ksss.setMaximumSize(QSize(16777215, 50))
        self.frame_cust_ksss.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_cust_ksss.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_14 = QHBoxLayout(self.frame_cust_ksss)
        self.horizontalLayout_14.setSpacing(0)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_15 = QLabel(self.frame_cust_ksss)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setMinimumSize(QSize(150, 0))
        self.label_15.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_14.addWidget(self.label_15)

        self.line_cust_ksss = QLineEdit(self.frame_cust_ksss)
        self.line_cust_ksss.setObjectName(u"line_cust_ksss")
        self.line_cust_ksss.setMinimumSize(QSize(350, 25))
        self.line_cust_ksss.setMaximumSize(QSize(350, 25))

        self.horizontalLayout_14.addWidget(self.line_cust_ksss)

        self.horizontalSpacer_5 = QSpacerItem(237, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_5)


        self.verticalLayout_12.addWidget(self.frame_cust_ksss)


        self.horizontalLayout_10.addWidget(self.frame_Search)

        self.frame_3 = QFrame(self.frame_17)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(97, 70))
        self.frame_3.setMaximumSize(QSize(97, 70))
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_select_cols = QPushButton(self.frame_3)
        self.btn_select_cols.setObjectName(u"btn_select_cols")
        self.btn_select_cols.setMinimumSize(QSize(97, 30))
        self.btn_select_cols.setMaximumSize(QSize(97, 30))
        icon = QIcon()
        icon.addFile(u":/icon/icon/list.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_select_cols.setIcon(icon)

        self.verticalLayout.addWidget(self.btn_select_cols)

        self.btn_download = QPushButton(self.frame_3)
        self.btn_download.setObjectName(u"btn_download")
        self.btn_download.setMinimumSize(QSize(97, 30))
        self.btn_download.setMaximumSize(QSize(97, 30))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/download.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_download.setIcon(icon1)

        self.verticalLayout.addWidget(self.btn_download)


        self.horizontalLayout_10.addWidget(self.frame_3)


        self.verticalLayout_15.addWidget(self.frame_17)

        self.frame = QFrame(self.widget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.frame_teboil_cust = QFrame(self.frame)
        self.frame_teboil_cust.setObjectName(u"frame_teboil_cust")
        self.frame_teboil_cust.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_teboil_cust.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.frame_teboil_cust)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.label_13 = QLabel(self.frame_teboil_cust)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(0, 35))
        self.label_13.setMaximumSize(QSize(16777215, 35))
        self.label_13.setFont(font1)
        self.label_13.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_13.addWidget(self.label_13)

        self.frame_16 = QFrame(self.frame_teboil_cust)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setMinimumSize(QSize(0, 40))
        self.frame_16.setMaximumSize(QSize(16777215, 40))
        self.frame_16.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(9, 9, 9, 9)
        self.check_teb_dealer = QCheckBox(self.frame_16)
        self.check_teb_dealer.setObjectName(u"check_teb_dealer")

        self.horizontalLayout_11.addWidget(self.check_teb_dealer)

        self.check_teb_direct = QCheckBox(self.frame_16)
        self.check_teb_direct.setObjectName(u"check_teb_direct")

        self.horizontalLayout_11.addWidget(self.check_teb_direct)

        self.check_teb_fws = QCheckBox(self.frame_16)
        self.check_teb_fws.setObjectName(u"check_teb_fws")

        self.horizontalLayout_11.addWidget(self.check_teb_fws)

        self.check_teb_market = QCheckBox(self.frame_16)
        self.check_teb_market.setObjectName(u"check_teb_market")

        self.horizontalLayout_11.addWidget(self.check_teb_market)


        self.verticalLayout_13.addWidget(self.frame_16)


        self.horizontalLayout_13.addWidget(self.frame_teboil_cust)

        self.frame_luk_cust = QFrame(self.frame)
        self.frame_luk_cust.setObjectName(u"frame_luk_cust")
        self.frame_luk_cust.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_luk_cust.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.frame_luk_cust)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.frame_luk_cust)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(0, 35))
        self.label_14.setMaximumSize(QSize(16777215, 35))
        self.label_14.setFont(font1)
        self.label_14.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_14.addWidget(self.label_14)

        self.frame_18 = QFrame(self.frame_luk_cust)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setMinimumSize(QSize(0, 40))
        self.frame_18.setMaximumSize(QSize(16777215, 40))
        self.frame_18.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(9, 9, 9, 9)
        self.check_luk_dealer = QCheckBox(self.frame_18)
        self.check_luk_dealer.setObjectName(u"check_luk_dealer")

        self.horizontalLayout_12.addWidget(self.check_luk_dealer)

        self.check_luk_direct = QCheckBox(self.frame_18)
        self.check_luk_direct.setObjectName(u"check_luk_direct")

        self.horizontalLayout_12.addWidget(self.check_luk_direct)

        self.check_luk_fws = QCheckBox(self.frame_18)
        self.check_luk_fws.setObjectName(u"check_luk_fws")

        self.horizontalLayout_12.addWidget(self.check_luk_fws)

        self.check_luk_market = QCheckBox(self.frame_18)
        self.check_luk_market.setObjectName(u"check_luk_market")

        self.horizontalLayout_12.addWidget(self.check_luk_market)

        self.check_luk_other = QCheckBox(self.frame_18)
        self.check_luk_other.setObjectName(u"check_luk_other")

        self.horizontalLayout_12.addWidget(self.check_luk_other)


        self.verticalLayout_14.addWidget(self.frame_18)


        self.horizontalLayout_13.addWidget(self.frame_luk_cust)


        self.verticalLayout_15.addWidget(self.frame)

        self.verticalSpacer = QSpacerItem(20, 173, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_15.addItem(self.verticalSpacer)

        self.frame_Update = QFrame(self.widget)
        self.frame_Update.setObjectName(u"frame_Update")
        self.frame_Update.setMinimumSize(QSize(0, 40))
        self.frame_Update.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_4 = QHBoxLayout(self.frame_Update)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_Update)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 40))
        self.horizontalLayout_5 = QHBoxLayout(self.frame_4)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frame_4)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(120, 40))
        self.frame_6.setMaximumSize(QSize(150, 40))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_6)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(12, 0, 12, 0)
        self.rep_date = QDateEdit(self.frame_6)
        self.rep_date.setObjectName(u"rep_date")
        self.rep_date.setFont(font1)
        self.rep_date.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rep_date.setDateTime(QDateTime(QDate(2023, 1, 1), QTime(3, 0, 0)))
        self.rep_date.setMaximumDate(QDate(10000, 1, 1))
        self.rep_date.setMaximumTime(QTime(2, 59, 59))
        self.rep_date.setMinimumTime(QTime(3, 0, 0))
        self.rep_date.setTimeSpec(Qt.TimeSpec.LocalTime)
        self.rep_date.setDate(QDate(2023, 1, 1))

        self.verticalLayout_5.addWidget(self.rep_date)


        self.horizontalLayout_5.addWidget(self.frame_6)

        self.label_invoice_File = QLabel(self.frame_4)
        self.label_invoice_File.setObjectName(u"label_invoice_File")
        self.label_invoice_File.setMinimumSize(QSize(0, 30))
        self.label_invoice_File.setMaximumSize(QSize(16777215, 30))
        self.label_invoice_File.setStyleSheet(u"background-color: #6272a4;\n"
"border-radius: 5px;\n"
"border: 2px solid #6272a4;\n"
"padding-left: 10px;\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 121, 198);\n"
"color: #f8f8f2;")

        self.horizontalLayout_5.addWidget(self.label_invoice_File)


        self.horizontalLayout_4.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_Update)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(120, 40))
        self.frame_5.setMaximumSize(QSize(250, 16777215))
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_open_file = QPushButton(self.frame_5)
        self.btn_open_file.setObjectName(u"btn_open_file")
        self.btn_open_file.setMinimumSize(QSize(90, 30))
        self.btn_open_file.setMaximumSize(QSize(90, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/icon/icon/folder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_open_file.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.btn_open_file)

        self.btn_upload_file = QPushButton(self.frame_5)
        self.btn_upload_file.setObjectName(u"btn_upload_file")
        self.btn_upload_file.setMinimumSize(QSize(90, 30))
        self.btn_upload_file.setMaximumSize(QSize(90, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/icon/icon/upload.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_upload_file.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.btn_upload_file)


        self.horizontalLayout_4.addWidget(self.frame_5)


        self.verticalLayout_15.addWidget(self.frame_Update)


        self.verticalLayout_4.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u0421\u0447\u0435\u0442\u0430-\u0444\u0430\u043a\u0442\u0443\u0440\u044b", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u0414\u0430\u0442\u0430 \u0441\u0447\u0435\u0442-\u0444\u0430\u043a\u0442\u0443\u0440\u044b", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u0413\u043e\u0434", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u041a\u0432\u0430\u0440\u0442\u0430\u043b", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u041c\u0435\u0441\u044f\u0446", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u0414\u0430\u0442\u0430 \u043e\u0442\u0433\u0440\u0443\u0437\u043a\u0438", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u0413\u043e\u0434", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u041a\u0432\u0430\u0440\u0442\u0430\u043b", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u041c\u0435\u0441\u044f\u0446", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u0411\u0440\u044d\u043d\u0434", None))
        self.line_brand.setItemText(0, QCoreApplication.translate("Form", u"-", None))
        self.line_brand.setItemText(1, QCoreApplication.translate("Form", u"TEBOIL", None))
        self.line_brand.setItemText(2, QCoreApplication.translate("Form", u"Shell", None))
        self.line_brand.setItemText(3, QCoreApplication.translate("Form", u"\u041b\u0443\u043a\u043e\u0439\u043b", None))
        self.line_brand.setItemText(4, QCoreApplication.translate("Form", u"GPO", None))

        self.label_12.setText(QCoreApplication.translate("Form", u"\u0421\u0435\u0433\u043c\u0435\u043d\u0442", None))
        self.line_segment.setItemText(0, QCoreApplication.translate("Form", u"-", None))
        self.line_segment.setItemText(1, QCoreApplication.translate("Form", u"PVL", None))
        self.line_segment.setItemText(2, QCoreApplication.translate("Form", u"CVL", None))
        self.line_segment.setItemText(3, QCoreApplication.translate("Form", u"IND", None))
        self.line_segment.setItemText(4, QCoreApplication.translate("Form", u"DL", None))
        self.line_segment.setItemText(5, QCoreApplication.translate("Form", u"Grease", None))
        self.line_segment.setItemText(6, QCoreApplication.translate("Form", u"Antifr", None))
        self.line_segment.setItemText(7, QCoreApplication.translate("Form", u"other", None))

        self.label_11.setText(QCoreApplication.translate("Form", u"\u0413\u0440\u0443\u043f\u043f\u0430 \u043f\u0440\u043e\u0434\u0443\u043a\u0442\u043e\u0432", None))
        self.label_15.setText(QCoreApplication.translate("Form", u"\u041a\u0421\u0421\u0421 \u043a\u043b\u0438\u0435\u043d\u0442\u0430", None))
        self.btn_select_cols.setText(QCoreApplication.translate("Form", u"Select Cols", None))
        self.btn_download.setText(QCoreApplication.translate("Form", u"Download", None))
        self.label_13.setText(QCoreApplication.translate("Form", u"\u041a\u043b\u0438\u0435\u043d\u0442\u044b TEBOIL", None))
        self.check_teb_dealer.setText(QCoreApplication.translate("Form", u"Dealer", None))
        self.check_teb_direct.setText(QCoreApplication.translate("Form", u"Direct", None))
        self.check_teb_fws.setText(QCoreApplication.translate("Form", u"FWS", None))
        self.check_teb_market.setText(QCoreApplication.translate("Form", u"Market Place", None))
        self.label_14.setText(QCoreApplication.translate("Form", u"\u041a\u043b\u0438\u0435\u043d\u0442\u044b \u041b\u0443\u043a\u043e\u0439\u043b", None))
        self.check_luk_dealer.setText(QCoreApplication.translate("Form", u"Dealer", None))
        self.check_luk_direct.setText(QCoreApplication.translate("Form", u"Direct", None))
        self.check_luk_fws.setText(QCoreApplication.translate("Form", u"FWS", None))
        self.check_luk_market.setText(QCoreApplication.translate("Form", u"Market Place", None))
        self.check_luk_other.setText(QCoreApplication.translate("Form", u"Others", None))
        self.rep_date.setDisplayFormat(QCoreApplication.translate("Form", u"MM.yyyy", None))
        self.label_invoice_File.setText(QCoreApplication.translate("Form", u"File Path", None))
        self.btn_open_file.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_upload_file.setText(QCoreApplication.translate("Form", u"Upload", None))
    # retranslateUi

