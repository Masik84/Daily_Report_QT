# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_costs_supplOuBcQI.ui'
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
    QFrame, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
from wind import resource_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(971, 682)
        Form.setMinimumSize(QSize(930, 650))
        font = QFont()
        font.setFamilies([u"Tahoma"])
        font.setPointSize(8)
        Form.setFont(font)
        Form.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
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
        font1 = QFont()
        font1.setFamilies([u"Tahoma"])
        self.widget.setFont(font1)
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.Title_label = QLabel(self.widget)
        self.Title_label.setObjectName(u"Title_label")
        self.Title_label.setMinimumSize(QSize(0, 50))
        font2 = QFont()
        font2.setFamilies([u"Tahoma"])
        font2.setPointSize(22)
        font2.setBold(False)
        font2.setItalic(False)
        self.Title_label.setFont(font2)
        self.Title_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.Title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_6.addWidget(self.Title_label)

        self.frame_Search = QFrame(self.widget)
        self.frame_Search.setObjectName(u"frame_Search")
        self.frame_Search.setMinimumSize(QSize(0, 110))
        self.frame_Search.setMaximumSize(QSize(16777215, 155))
        self.horizontalLayout_5 = QHBoxLayout(self.frame_Search)
        self.horizontalLayout_5.setSpacing(4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(8, 0, 0, 0)
        self.frame = QFrame(self.frame_Search)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(60, 0))
        self.frame.setMaximumSize(QSize(170, 16777215))
        self.frame.setFont(font1)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 9, 6)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        font3 = QFont()
        font3.setFamilies([u"Tahoma"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_3.setFont(font3)
        self.label_3.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)


        self.horizontalLayout_5.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_Search)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(250, 0))
        self.frame_2.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.line_Suppl1 = QComboBox(self.frame_2)
        self.line_Suppl1.setObjectName(u"line_Suppl1")

        self.verticalLayout_3.addWidget(self.line_Suppl1)

        self.line_Suppl2 = QComboBox(self.frame_2)
        self.line_Suppl2.setObjectName(u"line_Suppl2")

        self.verticalLayout_3.addWidget(self.line_Suppl2)

        self.line_SupplRep = QComboBox(self.frame_2)
        self.line_SupplRep.setObjectName(u"line_SupplRep")

        self.verticalLayout_3.addWidget(self.line_SupplRep)


        self.horizontalLayout_5.addWidget(self.frame_2)

        self.horizontalSpacer_2 = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)

        self.frame_7 = QFrame(self.frame_Search)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(90, 0))
        self.frame_7.setMaximumSize(QSize(90, 16777215))
        self.frame_7.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame_7)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 1, -1, 6)
        self.label_2 = QLabel(self.frame_7)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_7.addWidget(self.label_2)

        self.label_5 = QLabel(self.frame_7)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_7.addWidget(self.label_5)

        self.label_6 = QLabel(self.frame_7)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_7.addWidget(self.label_6)


        self.horizontalLayout_5.addWidget(self.frame_7)

        self.frame_8 = QFrame(self.frame_Search)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.frame_8)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.line_Order = QComboBox(self.frame_8)
        self.line_Order.setObjectName(u"line_Order")

        self.verticalLayout_8.addWidget(self.line_Order)

        self.line_Shipp = QComboBox(self.frame_8)
        self.line_Shipp.setObjectName(u"line_Shipp")

        self.verticalLayout_8.addWidget(self.line_Shipp)

        self.line_Container = QLineEdit(self.frame_8)
        self.line_Container.setObjectName(u"line_Container")

        self.verticalLayout_8.addWidget(self.line_Container)


        self.horizontalLayout_5.addWidget(self.frame_8)

        self.horizontalSpacer = QSpacerItem(30, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.frame_3 = QFrame(self.frame_Search)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(100, 0))
        self.frame_3.setMaximumSize(QSize(100, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 9, 0, -1)
        self.btn_find = QPushButton(self.frame_3)
        self.btn_find.setObjectName(u"btn_find")
        self.btn_find.setMinimumSize(QSize(97, 30))
        self.btn_find.setMaximumSize(QSize(93, 16777215))
        icon = QIcon()
        icon.addFile(u":/icon/icon/search \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_find.setIcon(icon)

        self.verticalLayout_4.addWidget(self.btn_find)


        self.horizontalLayout_5.addWidget(self.frame_3)

        self.horizontalSpacer_3 = QSpacerItem(90, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addWidget(self.frame_Search)

        self.table = QTableWidget(self.widget)
        self.table.setObjectName(u"table")
        self.table.setMinimumSize(QSize(0, 0))
        self.table.setFont(font3)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
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
        self.table.verticalHeader().setDefaultSectionSize(25)
        self.table.verticalHeader().setHighlightSections(False)

        self.verticalLayout_6.addWidget(self.table)

        self.frame_Update = QFrame(self.widget)
        self.frame_Update.setObjectName(u"frame_Update")
        self.frame_Update.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_Update.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_Update)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_suppl_file = QFrame(self.frame_Update)
        self.frame_suppl_file.setObjectName(u"frame_suppl_file")
        self.frame_suppl_file.setMinimumSize(QSize(0, 45))
        self.frame_suppl_file.setMaximumSize(QSize(16777215, 45))
        self.frame_suppl_file.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_suppl_file.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame_suppl_file)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_suppl_file)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(0, 50))
        self.frame_4.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_Supplier_File = QLabel(self.frame_4)
        self.label_Supplier_File.setObjectName(u"label_Supplier_File")
        self.label_Supplier_File.setMinimumSize(QSize(0, 30))
        self.label_Supplier_File.setMaximumSize(QSize(16777215, 30))
        self.label_Supplier_File.setStyleSheet(u"QLabel {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	color: #964b09;\n"
"	font: 10pt \"Tahoma\";\n"
"}\n"
"")

        self.verticalLayout_5.addWidget(self.label_Supplier_File)


        self.horizontalLayout_4.addWidget(self.frame_4)

        self.frame_5 = QFrame(self.frame_suppl_file)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(120, 50))
        self.frame_5.setMaximumSize(QSize(250, 16777215))
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_open_file = QPushButton(self.frame_5)
        self.btn_open_file.setObjectName(u"btn_open_file")
        self.btn_open_file.setMinimumSize(QSize(90, 30))
        self.btn_open_file.setMaximumSize(QSize(90, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/folder \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_open_file.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.btn_open_file)

        self.btn_upload_file = QPushButton(self.frame_5)
        self.btn_upload_file.setObjectName(u"btn_upload_file")
        self.btn_upload_file.setMinimumSize(QSize(90, 30))
        self.btn_upload_file.setMaximumSize(QSize(90, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/icon/icon/upload \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_upload_file.setIcon(icon2)

        self.horizontalLayout_3.addWidget(self.btn_upload_file)


        self.horizontalLayout_4.addWidget(self.frame_5)


        self.verticalLayout.addWidget(self.frame_suppl_file)


        self.verticalLayout_6.addWidget(self.frame_Update)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Title_label.setText(QCoreApplication.translate("Form", u"\u0414\u043e\u043f \u0440\u0430\u0441\u0445\u043e\u0434\u044b (\u041f\u043e\u0441\u0442\u0430\u0432\u043a\u0438)", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0437\u0432. \u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0437\u0432. \u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430 2", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0437\u0432. \u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430 (\u043e\u0442\u0447\u0435\u0442)", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Order No", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Shipping No", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"Container", None))
        self.btn_find.setText(QCoreApplication.translate("Form", u"Search", None))
        self.label_Supplier_File.setText(QCoreApplication.translate("Form", u"\u0412\u044b\u0431\u0435\u0440\u0438 \u0444\u0430\u0439\u043b \u0438\u043b\u0438 \u043d\u0430\u0436\u043c\u0438 Upload, \u0444\u0430\u0439\u043b \u0431\u0443\u0434\u0435\u0442 \u0432\u0437\u044f\u0442 \u0438\u0437 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u043f\u0430\u043f\u043a\u0438", None))
        self.btn_open_file.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_upload_file.setText(QCoreApplication.translate("Form", u"Upload", None))
    # retranslateUi

