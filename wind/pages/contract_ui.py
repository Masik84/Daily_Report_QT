# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'contractYddDrw.ui'
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
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
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
        self.verticalLayout_7 = QVBoxLayout(Form)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_9 = QVBoxLayout(self.widget)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 50))
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_9.addWidget(self.label)

        self.frame_Search = QFrame(self.widget)
        self.frame_Search.setObjectName(u"frame_Search")
        self.frame_Search.setMinimumSize(QSize(0, 110))
        self.frame_Search.setMaximumSize(QSize(16777215, 110))
        self.horizontalLayout_5 = QHBoxLayout(self.frame_Search)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.frame = QFrame(self.frame_Search)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(100, 0))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 9, 0)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        font1 = QFont()
        font1.setPointSize(9)
        self.label_2.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_3)

        self.label_6 = QLabel(self.frame)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font1)

        self.verticalLayout_2.addWidget(self.label_6)


        self.horizontalLayout_5.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_Search)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.line_KSSS = QLineEdit(self.frame_2)
        self.line_KSSS.setObjectName(u"line_KSSS")

        self.verticalLayout_3.addWidget(self.line_KSSS)

        self.line_Contr_N = QLineEdit(self.frame_2)
        self.line_Contr_N.setObjectName(u"line_Contr_N")

        self.verticalLayout_3.addWidget(self.line_Contr_N)

        self.line_Cust_type = QComboBox(self.frame_2)
        self.line_Cust_type.addItem("")
        self.line_Cust_type.addItem("")
        self.line_Cust_type.addItem("")
        self.line_Cust_type.addItem("")
        self.line_Cust_type.addItem("")
        self.line_Cust_type.addItem("")
        self.line_Cust_type.addItem("")
        self.line_Cust_type.addItem("")
        self.line_Cust_type.addItem("")
        self.line_Cust_type.setObjectName(u"line_Cust_type")

        self.verticalLayout_3.addWidget(self.line_Cust_type)


        self.horizontalLayout_5.addWidget(self.frame_2)

        self.horizontalSpacer = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.frame_3 = QFrame(self.frame_Search)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(93, 0))
        self.frame_3.setMaximumSize(QSize(93, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.btn_find = QPushButton(self.frame_3)
        self.btn_find.setObjectName(u"btn_find")
        self.btn_find.setMinimumSize(QSize(92, 30))
        self.btn_find.setMaximumSize(QSize(92, 16777215))
        icon = QIcon()
        icon.addFile(u":/icon/icon/search.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_find.setIcon(icon)

        self.verticalLayout_4.addWidget(self.btn_find)

        self.btn_download = QPushButton(self.frame_3)
        self.btn_download.setObjectName(u"btn_download")
        self.btn_download.setMinimumSize(QSize(92, 30))
        self.btn_download.setMaximumSize(QSize(92, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/download.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_download.setIcon(icon1)

        self.verticalLayout_4.addWidget(self.btn_download)


        self.horizontalLayout_5.addWidget(self.frame_3)

        self.horizontalSpacer_3 = QSpacerItem(50, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout_9.addWidget(self.frame_Search)

        self.table = QTableWidget(self.widget)
        if (self.table.columnCount() < 4):
            self.table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.table.setObjectName(u"table")
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(False)
        self.table.setColumnCount(4)
        self.table.horizontalHeader().setCascadingSectionResizes(True)
        self.table.horizontalHeader().setMinimumSectionSize(25)
        self.table.horizontalHeader().setProperty(u"showSortIndicator", True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setCascadingSectionResizes(False)
        self.table.verticalHeader().setMinimumSectionSize(0)
        self.table.verticalHeader().setDefaultSectionSize(10)
        self.table.verticalHeader().setHighlightSections(False)

        self.verticalLayout_9.addWidget(self.table)

        self.frame_Update = QFrame(self.widget)
        self.frame_Update.setObjectName(u"frame_Update")
        self.frame_Update.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Update.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_Update)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_contr_file = QFrame(self.frame_Update)
        self.frame_contr_file.setObjectName(u"frame_contr_file")
        self.frame_contr_file.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_contr_file.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_contr_file)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_6 = QFrame(self.frame_contr_file)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setMinimumSize(QSize(0, 50))
        self.frame_6.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_sap_contr_file = QLabel(self.frame_6)
        self.label_sap_contr_file.setObjectName(u"label_sap_contr_file")
        self.label_sap_contr_file.setMinimumSize(QSize(0, 30))
        self.label_sap_contr_file.setMaximumSize(QSize(16777215, 30))
        self.label_sap_contr_file.setStyleSheet(u"background-color: #6272a4;\n"
"border-radius: 5px;\n"
"border: 2px solid #6272a4;\n"
"padding-left: 10px;\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 121, 198);\n"
"color: #f8f8f2;")

        self.verticalLayout_8.addWidget(self.label_sap_contr_file)


        self.horizontalLayout_10.addWidget(self.frame_6)

        self.frame_12 = QFrame(self.frame_contr_file)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setMinimumSize(QSize(250, 0))
        self.frame_12.setMaximumSize(QSize(250, 16777215))
        self.frame_12.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_11.setSpacing(0)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_open_file_sap_cont = QPushButton(self.frame_12)
        self.btn_open_file_sap_cont.setObjectName(u"btn_open_file_sap_cont")
        self.btn_open_file_sap_cont.setMinimumSize(QSize(90, 30))
        self.btn_open_file_sap_cont.setMaximumSize(QSize(90, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/icon/icon/folder.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_open_file_sap_cont.setIcon(icon2)

        self.horizontalLayout_11.addWidget(self.btn_open_file_sap_cont)

        self.btn_upload_file_sap_cont = QPushButton(self.frame_12)
        self.btn_upload_file_sap_cont.setObjectName(u"btn_upload_file_sap_cont")
        self.btn_upload_file_sap_cont.setMinimumSize(QSize(90, 30))
        self.btn_upload_file_sap_cont.setMaximumSize(QSize(90, 16777215))
        icon3 = QIcon()
        icon3.addFile(u":/icon/icon/upload.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_upload_file_sap_cont.setIcon(icon3)

        self.horizontalLayout_11.addWidget(self.btn_upload_file_sap_cont)


        self.horizontalLayout_10.addWidget(self.frame_12)


        self.verticalLayout.addWidget(self.frame_contr_file)

        self.frame_cust_type_file = QFrame(self.frame_Update)
        self.frame_cust_type_file.setObjectName(u"frame_cust_type_file")
        self.frame_cust_type_file.setMinimumSize(QSize(0, 50))
        self.frame_cust_type_file.setMaximumSize(QSize(16777215, 50))
        self.frame_cust_type_file.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_cust_type_file.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_cust_type_file)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_cust_type_file)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 50))
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label_Cust_File = QLabel(self.frame_4)
        self.label_Cust_File.setObjectName(u"label_Cust_File")
        self.label_Cust_File.setMinimumSize(QSize(0, 30))
        self.label_Cust_File.setMaximumSize(QSize(16777215, 30))
        self.label_Cust_File.setStyleSheet(u"background-color: #6272a4;\n"
"border-radius: 5px;\n"
"border: 2px solid #6272a4;\n"
"padding-left: 10px;\n"
"selection-color: rgb(255, 255, 255);\n"
"selection-background-color: rgb(255, 121, 198);\n"
"color: #f8f8f2;")

        self.verticalLayout_5.addWidget(self.label_Cust_File)


        self.horizontalLayout_4.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_cust_type_file)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(120, 50))
        self.frame_5.setMaximumSize(QSize(250, 16777215))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_open_file_cust_type = QPushButton(self.frame_5)
        self.btn_open_file_cust_type.setObjectName(u"btn_open_file_cust_type")
        self.btn_open_file_cust_type.setMinimumSize(QSize(90, 30))
        self.btn_open_file_cust_type.setMaximumSize(QSize(90, 16777215))
        self.btn_open_file_cust_type.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.btn_open_file_cust_type)

        self.btn_upload_file_cust_type = QPushButton(self.frame_5)
        self.btn_upload_file_cust_type.setObjectName(u"btn_upload_file_cust_type")
        self.btn_upload_file_cust_type.setMinimumSize(QSize(90, 30))
        self.btn_upload_file_cust_type.setMaximumSize(QSize(90, 16777215))
        self.btn_upload_file_cust_type.setIcon(icon3)

        self.horizontalLayout_3.addWidget(self.btn_upload_file_cust_type)


        self.horizontalLayout_4.addWidget(self.frame_5)


        self.verticalLayout.addWidget(self.frame_cust_type_file)


        self.verticalLayout_9.addWidget(self.frame_Update)


        self.verticalLayout_7.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u041a\u043b\u0438\u0435\u043d\u0442\u0430 \u0438 \u0414\u043e\u0433\u043e\u0432\u043e\u0440\u0430", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u041a\u0421\u0421\u0421 \u043a\u043b\u0438\u0435\u043d\u0442\u0430", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u041d\u043e\u043c\u0435\u0440 \u0414\u043e\u0433\u043e\u0432\u043e\u0440\u0430", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u0422\u0438\u043f \u041a\u043b\u0438\u0435\u043d\u0442\u0430", None))
        self.line_KSSS.setText("")
        self.line_Cust_type.setItemText(0, QCoreApplication.translate("Form", u"All", None))
        self.line_Cust_type.setItemText(1, QCoreApplication.translate("Form", u"Dealer_LLK", None))
        self.line_Cust_type.setItemText(2, QCoreApplication.translate("Form", u"Dealer_TEBOIL", None))
        self.line_Cust_type.setItemText(3, QCoreApplication.translate("Form", u"Dir_LLK", None))
        self.line_Cust_type.setItemText(4, QCoreApplication.translate("Form", u"Dir_TEBOIL", None))
        self.line_Cust_type.setItemText(5, QCoreApplication.translate("Form", u"FWS_LLK", None))
        self.line_Cust_type.setItemText(6, QCoreApplication.translate("Form", u"FWS_TEBOIL", None))
        self.line_Cust_type.setItemText(7, QCoreApplication.translate("Form", u"MarketPlace_TEBOIL", None))
        self.line_Cust_type.setItemText(8, QCoreApplication.translate("Form", u"other_LLK", None))

        self.btn_find.setText(QCoreApplication.translate("Form", u"Search", None))
        self.btn_download.setText(QCoreApplication.translate("Form", u"Download", None))
        ___qtablewidgetitem = self.table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Contract", None));
        ___qtablewidgetitem1 = self.table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"\u041a\u0421\u0421\u0421", None));
        ___qtablewidgetitem2 = self.table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Customer Name", None));
        ___qtablewidgetitem3 = self.table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Cust type", None));
        self.label_sap_contr_file.setText(QCoreApplication.translate("Form", u"SAP Contracts File Path", None))
        self.btn_open_file_sap_cont.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_upload_file_sap_cont.setText(QCoreApplication.translate("Form", u"Upload", None))
        self.label_Cust_File.setText(QCoreApplication.translate("Form", u"Customer type File Path", None))
        self.btn_open_file_cust_type.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_upload_file_cust_type.setText(QCoreApplication.translate("Form", u"Upload", None))
    # retranslateUi

