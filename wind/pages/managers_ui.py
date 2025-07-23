# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'managersDtFmZF.ui'
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
        Form.resize(930, 650)
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
"QTableWidget {\n"
"    background-color: #f8f8f2;\n"
"    padding: 10px;\n"
"    border-radius: 5px;\n"
"    gridline-color: #f8994a;\n"
"    outline: none;\n"
"    color: #262626; /* Основной цвет текста */\n"
"    font: 10pt \"Tahoma\"; /* Добавляем явное указание шрифта */\n"
"}\n"
"QTableWidget::item {\n"
"    border-color: #f8994a;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    gridline-color: #f8994a;\n"
"    color: #262626 !important; /* Принудительно устанавливаем цвет текста */\n"
"    background-color: #f8f8f2; /* Фон ячеек */\n"
"}\n"
"QTableWidget::item:selected {\n"
"    background-color: #f6c294;\n"
"    color: #262626;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #ffd4af;\n"
"    padding: 3px;\n"
"    border: 1px solid #f8994a;\n"
"    color: #262626;\n"
"    font: bold 10pt \"Tahoma\";\n"
"}\n"
"QTableCornerButton::section {\n"
"    background-color: #ffd4af;\n"
"    border: 1px solid #f8994a;\n"
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
        self.widget.setEnabled(True)
        self.widget.setVisible(True)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Title_label = QLabel(self.widget)
        self.Title_label.setObjectName(u"Title_label")
        self.Title_label.setMinimumSize(QSize(0, 50))
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
        self.frame_Search.setMinimumSize(QSize(0, 120))
        self.frame_Search.setMaximumSize(QSize(16777215, 140))
        self.horizontalLayout_5 = QHBoxLayout(self.frame_Search)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(12, 0, 0, 9)
        self.frame = QFrame(self.frame_Search)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(100, 0))
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


        self.horizontalLayout_5.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_Search)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(250, 70))
        self.frame_2.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.line_kam = QComboBox(self.frame_2)
        self.line_kam.setObjectName(u"line_kam")
        self.line_kam.setMinimumSize(QSize(0, 25))

        self.verticalLayout_3.addWidget(self.line_kam)

        self.line_stl = QComboBox(self.frame_2)
        self.line_stl.setObjectName(u"line_stl")
        self.line_stl.setMinimumSize(QSize(0, 25))

        self.verticalLayout_3.addWidget(self.line_stl)

        self.line_tl = QComboBox(self.frame_2)
        self.line_tl.setObjectName(u"line_tl")
        self.line_tl.setMinimumSize(QSize(0, 25))
        self.line_tl.setMaximumSize(QSize(16777215, 25))

        self.verticalLayout_3.addWidget(self.line_tl)


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
        self.btn_find_KAM = QPushButton(self.frame_3)
        self.btn_find_KAM.setObjectName(u"btn_find_KAM")
        self.btn_find_KAM.setMinimumSize(QSize(97, 30))
        self.btn_find_KAM.setMaximumSize(QSize(92, 16777215))
        icon = QIcon()
        icon.addFile(u":/icon/icon/search \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_find_KAM.setIcon(icon)

        self.verticalLayout_4.addWidget(self.btn_find_KAM)

        self.btn_find_STL = QPushButton(self.frame_3)
        self.btn_find_STL.setObjectName(u"btn_find_STL")
        self.btn_find_STL.setMinimumSize(QSize(97, 30))
        self.btn_find_STL.setMaximumSize(QSize(92, 16777215))
        self.btn_find_STL.setIcon(icon)

        self.verticalLayout_4.addWidget(self.btn_find_STL)

        self.btn_find_TL = QPushButton(self.frame_3)
        self.btn_find_TL.setObjectName(u"btn_find_TL")
        self.btn_find_TL.setMinimumSize(QSize(97, 30))
        self.btn_find_TL.setIcon(icon)

        self.verticalLayout_4.addWidget(self.btn_find_TL)


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

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addWidget(self.frame_Search)

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
        self.label_manager_File = QLabel(self.frame_9)
        self.label_manager_File.setObjectName(u"label_manager_File")
        self.label_manager_File.setMinimumSize(QSize(0, 30))
        self.label_manager_File.setMaximumSize(QSize(16777215, 30))
        self.label_manager_File.setStyleSheet(u"QLabel {\n"
"	background-color: #f8f8f2;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #f09d54;\n"
"	padding-left: 10px;\n"
"	color: #964b09;\n"
"	font: 10pt \"Tahoma\";\n"
"}")

        self.horizontalLayout_7.addWidget(self.label_manager_File)

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
        self.btn_open_file_manager = QPushButton(self.frame_10)
        self.btn_open_file_manager.setObjectName(u"btn_open_file_manager")
        self.btn_open_file_manager.setMinimumSize(QSize(90, 30))
        self.btn_open_file_manager.setMaximumSize(QSize(90, 16777215))
        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/folder \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_open_file_manager.setIcon(icon1)

        self.horizontalLayout_6.addWidget(self.btn_open_file_manager)

        self.btn_upload_file_manager = QPushButton(self.frame_10)
        self.btn_upload_file_manager.setObjectName(u"btn_upload_file_manager")
        self.btn_upload_file_manager.setMinimumSize(QSize(90, 30))
        self.btn_upload_file_manager.setMaximumSize(QSize(90, 16777215))
        icon2 = QIcon()
        icon2.addFile(u":/icon/icon/upload \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_upload_file_manager.setIcon(icon2)

        self.horizontalLayout_6.addWidget(self.btn_upload_file_manager)


        self.horizontalLayout_7.addWidget(self.frame_10)


        self.verticalLayout.addWidget(self.frame_9)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Title_label.setText(QCoreApplication.translate("Form", u"\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u044b", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"STL", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Team Lead", None))
        self.btn_find_KAM.setText(QCoreApplication.translate("Form", u"Search KAM", None))
        self.btn_find_STL.setText(QCoreApplication.translate("Form", u"Search STL", None))
        self.btn_find_TL.setText(QCoreApplication.translate("Form", u"Search TL", None))
        self.label_manager_File.setText(QCoreApplication.translate("Form", u"\u0412\u044b\u0431\u0435\u0440\u0438 \u0444\u0430\u0439\u043b \u0438\u043b\u0438 \u043d\u0430\u0436\u043c\u0438 Upload, \u0444\u0430\u0439\u043b \u0431\u0443\u0434\u0435\u0442 \u0432\u0437\u044f\u0442 \u0438\u0437 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u043f\u0430\u043f\u043a\u0438", None))
        self.btn_open_file_manager.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_upload_file_manager.setText(QCoreApplication.translate("Form", u"Upload", None))
    # retranslateUi

