# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'supplierSYmYsM.ui'
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
"/* \u0421\u0442\u0438\u043b\u0438 \u0434\u043b\u044f \u043c\u043d\u043e\u0436\u0435\u0441\u0442\u0432\u0435\u043d\u043d\u043e\u0433\u043e \u0432\u044b\u0431\u043e\u0440\u0430 */\n"
"QListWidget {\n"
"    background-color: #f8f8f2;\n"
"    border: 2px solid #f09d54;\n"
"    border-radius: 5px;\n"
"    color: #262626;\n"
"    font: 10pt \"Tahoma\";\n"
"}\n"
"\n"
"QListWidget::item {\n"
"    padding: 5px;\n"
"    border-bottom: 1px solid #f8994a;\n"
"}\n"
"\n"
"QListWidget::item:selected {\n"
"    background-color: #f28223;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QListWidget::item:hover {\n"
"    background-color: #ffd4af;\n"
"}\n"
"\n"
"/* \u0423\u043b\u0443\u0447\u0448\u0435\u043d\u043d\u0430\u044f \u0432\u0438\u0434\u0438\u043c\u043e\u0441\u0442\u044c \u0447\u0435\u043a\u0431\u043e\u043a\u0441\u043e\u0432 */\n"
"QCheckBox::indicator {\n"
""
                        "    width: 16px;\n"
"    height: 16px;\n"
"}\n"
"\n"
"QCheckBox::indicator:unchecked {\n"
"    border: 2px solid #f09d54;\n"
"    background-color: #f8f8f2;\n"
"    border-radius: 3px;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked {\n"
"    border: 2px solid #f28223;\n"
"    background-color: #f28223;\n"
"    border-radius: 3px;\n"
"    image: url(:/icon/icon/check.svg);\n"
"}\n"
"\n"
"QCheckBox::indicator:hover {\n"
"    border: 2px solid #f28223;\n"
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
""
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
"    border-bottom-right-r"
                        "adius: 4px;\n"
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
"    border-bottom-righ"
                        "t-radius: 4px;\n"
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
""
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
"    selection-color: "
                        "#ffffff;\n"
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
""
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
        font1 = QFont()
        font1.setFamilies([u"Tahoma"])
        self.widget.setFont(font1)
        self.verticalLayout_6 = QVBoxLayout(self.widget)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.Title_label = QLabel(self.widget)
        self.Title_label.setObjectName(u"Title_label")
        self.Title_label.setMinimumSize(QSize(0, 40))
        self.Title_label.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setFamilies([u"Tahoma"])
        font2.setPointSize(18)
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
        self.frame.setMinimumSize(QSize(100, 0))
        self.frame.setFont(font1)
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 9, 0)
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        font3 = QFont()
        font3.setFamilies([u"Tahoma"])
        font3.setPointSize(10)
        font3.setBold(False)
        font3.setItalic(False)
        self.label_2.setFont(font3)

        self.verticalLayout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font3)
        self.label_3.setStyleSheet(u"")

        self.verticalLayout_2.addWidget(self.label_3)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)


        self.horizontalLayout_5.addWidget(self.frame)

        self.frame_2 = QFrame(self.frame_Search)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.line_ID = QLineEdit(self.frame_2)
        self.line_ID.setObjectName(u"line_ID")
        self.line_ID.setMinimumSize(QSize(0, 22))
        self.line_ID.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_3.addWidget(self.line_ID)

        self.line_Suppl1 = QComboBox(self.frame_2)
        self.line_Suppl1.setObjectName(u"line_Suppl1")
        self.line_Suppl1.setMinimumSize(QSize(0, 22))
        self.line_Suppl1.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_3.addWidget(self.line_Suppl1)

        self.line_Suppl2 = QComboBox(self.frame_2)
        self.line_Suppl2.setObjectName(u"line_Suppl2")
        self.line_Suppl2.setMinimumSize(QSize(0, 22))
        self.line_Suppl2.setMaximumSize(QSize(16777215, 22))

        self.verticalLayout_3.addWidget(self.line_Suppl2)


        self.horizontalLayout_5.addWidget(self.frame_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer)

        self.frame_3 = QFrame(self.frame_Search)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(130, 0))
        self.frame_3.setMaximumSize(QSize(120, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.frame_3)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 9, 0, -1)
        self.btn_find_suppl = QPushButton(self.frame_3)
        self.btn_find_suppl.setObjectName(u"btn_find_suppl")
        self.btn_find_suppl.setMinimumSize(QSize(130, 30))
        self.btn_find_suppl.setMaximumSize(QSize(92, 16777215))
        icon = QIcon()
        icon.addFile(u":/icon/icon/search \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_find_suppl.setIcon(icon)

        self.verticalLayout_4.addWidget(self.btn_find_suppl)


        self.horizontalLayout_5.addWidget(self.frame_3)

        self.horizontalSpacer_3 = QSpacerItem(400, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)


        self.verticalLayout_6.addWidget(self.frame_Search)

        self.table = QTableWidget(self.widget)
        self.table.setObjectName(u"table")
        self.table.setMinimumSize(QSize(0, 0))
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
        self.Title_label.setText(QCoreApplication.translate("Form", u"\u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0438", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u041a\u043e\u0434 1\u0421", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0437\u0432. \u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u041d\u0430\u0437\u0432. \u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0430 2", None))
        self.line_ID.setText(QCoreApplication.translate("Form", u"-", None))
        self.btn_find_suppl.setText(QCoreApplication.translate("Form", u"Search Supplier", None))
        self.label_Supplier_File.setText(QCoreApplication.translate("Form", u"\u0412\u044b\u0431\u0435\u0440\u0438 \u0444\u0430\u0439\u043b \u0438\u043b\u0438 \u043d\u0430\u0436\u043c\u0438 Upload, \u0444\u0430\u0439\u043b \u0431\u0443\u0434\u0435\u0442 \u0432\u0437\u044f\u0442 \u0438\u0437 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u043f\u0430\u043f\u043a\u0438", None))
        self.btn_open_file.setText(QCoreApplication.translate("Form", u"Open", None))
        self.btn_upload_file.setText(QCoreApplication.translate("Form", u"Upload", None))
    # retranslateUi

