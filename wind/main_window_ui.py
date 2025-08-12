# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowVVAVeM.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QSplitter, QTabWidget, QToolBox,
    QVBoxLayout, QWidget)
from wind import resource_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1400, 820)
        MainWindow.setMinimumSize(QSize(1400, 820))
        MainWindow.setWindowTitle(u"Phoenix Report Program")
        icon = QIcon()
        icon.addFile(u":/image/logo/\u043b\u043e\u0433\u043e_\u043a\u0430\u043f\u043b\u044f.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"QToolTip {\n"
"	background-color: #f8f8f2;\n"
"	border: 1px solid #CCC;\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid #f28223;\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"QTabWidget {\n"
"	background-color: #f8f8f2;\n"
"}\n"
"\n"
"#main_widget {\n"
"	background-color: #f8f8f2; \n"
"}\n"
"\n"
"#search_widget {\n"
"	background-color: #f8f8f2; \n"
"	color: 262626; \n"
"	border: 2px solid #f28223;\n"
"	border-radius: 5px;\n"
"}\n"
"#frame_AppBtn {background-color: transparent}\n"
"\n"
"#bottomWidget {\n"
"	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(244, 113, 32, 255), stop:1 rgba(243, 143, 61, 255));\n"
"}\n"
"\n"
"#label_prog_name.QLabel {\n"
"	color: #262626;\n"
"}\n"
"\n"
"#label_produced.QLabel {\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"QPushButton {\n"
"	border: 2px solid #f09d54;\n"
"	border-radius: 5px;\n"
"	background-color: #f8f8f2"
                        ";\n"
"	color: #262626;\n"
"	font: 10pt \"Tahoma\";\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"	background-color: #f09d54;\n"
"	color: #262626;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"	background-color: #f28223;\n"
"	border: 2px solid #f28223;\n"
"	color: #262626;\n"
"}\n"
"\n"
"#toggleButton {\n"
"	border: 2px solid #f09d54;\n"
"	border-radius: 5px;\n"
"	background-color: #f8f8f2;\n"
"	color: #262626;\n"
"\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: #f09d54;\n"
"	color: #262626;\n"
"}\n"
"\n"
"#toggleButton:pressed {	\n"
"	background-color: #f28223;\n"
"	border: 2px solid #f28223;\n"
"	color: #262626;\n"
"}\n"
"\n"
"#docs_page {	\n"
"	background-color: #ffb472;\n"
"}\n"
"\n"
"#updater_page {	\n"
"	background-color: #ffb472;\n"
"}\n"
"\n"
"#general_page {	\n"
"	background-color: #ffb472;\n"
"}\n"
"\n"
"#bonus_page {	\n"
"	background-color: #ffb472;\n"
"}\n"
"\n"
"#toolBox {\n"
"	border: 3px solid #f28223;\n"
"	border-radius: 5px;\n"
"	background-color: #ffb472;\n"
"	color: #262626;\n"
"}\n"
"\n"
"#toolB"
                        "ox::tab {\n"
"	padding-left:5px;\n"
"	border-radius: 3px;\n"
"	text-align: left;\n"
"	color: #262626;\n"
"}\n"
"\n"
"\n"
"#toolBox::tab:selected {\n"
"	background-color: #f28223;\n"
"	font-weight: bold;\n"
"	color: #ffffff;\n"
"}\n"
"\n"
"#toolBox QPushButton {\n"
"	padding:5px 0px 5px 20px;\n"
"	border-radius: 5px;\n"
"	text-align: left;\n"
"	background-color: #ffffff;\n"
"	color: #ba5706;\n"
"}\n"
"\n"
"#toolBox QPushButton:hover {\n"
"	background-color: #f28223;\n"
"	color: #ffffff;\n"
"}\n"
"")
        self.appMargins = QGridLayout(self.centralwidget)
        self.appMargins.setSpacing(0)
        self.appMargins.setObjectName(u"appMargins")
        self.appMargins.setContentsMargins(10, 10, 10, 10)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(0)
        self.menu_widget = QWidget(self.splitter)
        self.menu_widget.setObjectName(u"menu_widget")
        self.menu_widget.setMinimumSize(QSize(0, 0))
        self.menu_widget.setMaximumSize(QSize(220, 16777215))
        self.menu_widget.setStyleSheet(u"#menu_widget {	\n"
"	background-color: #f09d54;\n"
"}")
        self.gridLayout = QGridLayout(self.menu_widget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(4, 4, 4, 15)
        self.toolBox = QToolBox(self.menu_widget)
        self.toolBox.setObjectName(u"toolBox")
        font = QFont()
        font.setFamilies([u"Tahoma"])
        font.setPointSize(12)
        self.toolBox.setFont(font)
        self.toolBox.setStyleSheet(u"")
        self.toolBox.setLineWidth(2)
        self.general_page = QWidget()
        self.general_page.setObjectName(u"general_page")
        self.general_page.setGeometry(QRect(0, 0, 206, 643))
        self.verticalLayout = QVBoxLayout(self.general_page)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 0, 5, 5)
        self.btn_Home = QPushButton(self.general_page)
        self.btn_Home.setObjectName(u"btn_Home")
        self.btn_Home.setMinimumSize(QSize(0, 25))
        font1 = QFont()
        font1.setFamilies([u"Tahoma"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        self.btn_Home.setFont(font1)
        self.btn_Home.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_Home.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_Home.setStyleSheet(u"")
        self.btn_Home.setCheckable(True)
        self.btn_Home.setChecked(True)

        self.verticalLayout.addWidget(self.btn_Home)

        self.btn_Dashboard = QPushButton(self.general_page)
        self.btn_Dashboard.setObjectName(u"btn_Dashboard")
        self.btn_Dashboard.setMinimumSize(QSize(0, 25))
        self.btn_Dashboard.setFont(font1)
        self.btn_Dashboard.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_Dashboard.setStyleSheet(u"")
        self.btn_Dashboard.setCheckable(True)

        self.verticalLayout.addWidget(self.btn_Dashboard)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        icon1 = QIcon()
        icon1.addFile(u":/icon/icon/home \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolBox.addItem(self.general_page, icon1, u"General")
        self.updater_page = QWidget()
        self.updater_page.setObjectName(u"updater_page")
        self.updater_page.setGeometry(QRect(0, 0, 206, 643))
        self.verticalLayout_3 = QVBoxLayout(self.updater_page)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 0, 5, 5)
        self.btn_Managers = QPushButton(self.updater_page)
        self.btn_Managers.setObjectName(u"btn_Managers")
        self.btn_Managers.setMinimumSize(QSize(0, 0))
        self.btn_Managers.setFont(font1)

        self.verticalLayout_3.addWidget(self.btn_Managers)

        self.btn_Customers = QPushButton(self.updater_page)
        self.btn_Customers.setObjectName(u"btn_Customers")
        self.btn_Customers.setFont(font1)
        self.btn_Customers.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_Customers.setCheckable(True)

        self.verticalLayout_3.addWidget(self.btn_Customers)

        self.btn_Products = QPushButton(self.updater_page)
        self.btn_Products.setObjectName(u"btn_Products")
        self.btn_Products.setMinimumSize(QSize(0, 0))
        self.btn_Products.setFont(font1)
        self.btn_Products.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_Products.setCheckable(True)

        self.verticalLayout_3.addWidget(self.btn_Products)

        self.btn_Plans = QPushButton(self.updater_page)
        self.btn_Plans.setObjectName(u"btn_Plans")
        self.btn_Plans.setFont(font1)

        self.verticalLayout_3.addWidget(self.btn_Plans)

        self.btn_Costs = QPushButton(self.updater_page)
        self.btn_Costs.setObjectName(u"btn_Costs")
        self.btn_Costs.setFont(font1)
        self.btn_Costs.setCheckable(True)

        self.verticalLayout_3.addWidget(self.btn_Costs)

        self.btn_Supplier = QPushButton(self.updater_page)
        self.btn_Supplier.setObjectName(u"btn_Supplier")

        self.verticalLayout_3.addWidget(self.btn_Supplier)

        self.btn_AddCosts = QPushButton(self.updater_page)
        self.btn_AddCosts.setObjectName(u"btn_AddCosts")

        self.verticalLayout_3.addWidget(self.btn_AddCosts)

        self.btn_CustDelivery = QPushButton(self.updater_page)
        self.btn_CustDelivery.setObjectName(u"btn_CustDelivery")

        self.verticalLayout_3.addWidget(self.btn_CustDelivery)

        self.btn_Price = QPushButton(self.updater_page)
        self.btn_Price.setObjectName(u"btn_Price")
        self.btn_Price.setMinimumSize(QSize(0, 0))
        self.btn_Price.setFont(font1)

        self.verticalLayout_3.addWidget(self.btn_Price)

        self.verticalSpacer_3 = QSpacerItem(20, 388, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        icon2 = QIcon()
        icon2.addFile(u":/icon/icon/list \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolBox.addItem(self.updater_page, icon2, u"\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0438")
        self.docs_page = QWidget()
        self.docs_page.setObjectName(u"docs_page")
        self.docs_page.setGeometry(QRect(0, 0, 206, 643))
        self.docs_page.setStyleSheet(u"")
        self.verticalLayout_2 = QVBoxLayout(self.docs_page)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 0, 5, 5)
        self.btn_Purchases = QPushButton(self.docs_page)
        self.btn_Purchases.setObjectName(u"btn_Purchases")
        self.btn_Purchases.setMinimumSize(QSize(0, 30))
        self.btn_Purchases.setFont(font1)
        self.btn_Purchases.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_Purchases.setCheckable(True)

        self.verticalLayout_2.addWidget(self.btn_Purchases)

        self.btn_Purch_Orders = QPushButton(self.docs_page)
        self.btn_Purch_Orders.setObjectName(u"btn_Purch_Orders")
        self.btn_Purch_Orders.setMinimumSize(QSize(0, 30))
        self.btn_Purch_Orders.setFont(font1)
        self.btn_Purch_Orders.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_Purch_Orders.setCheckable(True)

        self.verticalLayout_2.addWidget(self.btn_Purch_Orders)

        self.btn_Sales = QPushButton(self.docs_page)
        self.btn_Sales.setObjectName(u"btn_Sales")
        self.btn_Sales.setMinimumSize(QSize(0, 30))
        self.btn_Sales.setFont(font1)
        self.btn_Sales.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_Sales.setCheckable(True)

        self.verticalLayout_2.addWidget(self.btn_Sales)

        self.btn_Cust_Orders = QPushButton(self.docs_page)
        self.btn_Cust_Orders.setObjectName(u"btn_Cust_Orders")
        self.btn_Cust_Orders.setFont(font1)

        self.verticalLayout_2.addWidget(self.btn_Cust_Orders)

        self.btn_MarketPlace = QPushButton(self.docs_page)
        self.btn_MarketPlace.setObjectName(u"btn_MarketPlace")

        self.verticalLayout_2.addWidget(self.btn_MarketPlace)

        self.btn_Complect = QPushButton(self.docs_page)
        self.btn_Complect.setObjectName(u"btn_Complect")

        self.verticalLayout_2.addWidget(self.btn_Complect)

        self.verticalSpacer_2 = QSpacerItem(20, 350, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        icon3 = QIcon()
        icon3.addFile(u":/icon/icon/file \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolBox.addItem(self.docs_page, icon3, u"\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b")
        self.bonus_page = QWidget()
        self.bonus_page.setObjectName(u"bonus_page")
        self.bonus_page.setGeometry(QRect(0, 0, 206, 643))
        font2 = QFont()
        font2.setFamilies([u"Tahoma"])
        self.bonus_page.setFont(font2)
        self.verticalLayout_4 = QVBoxLayout(self.bonus_page)
        self.verticalLayout_4.setSpacing(10)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 0, 5, 5)
        self.btn_Scheme = QPushButton(self.bonus_page)
        self.btn_Scheme.setObjectName(u"btn_Scheme")
        self.btn_Scheme.setMinimumSize(QSize(0, 30))
        self.btn_Scheme.setFont(font1)

        self.verticalLayout_4.addWidget(self.btn_Scheme)

        self.btn_Plan = QPushButton(self.bonus_page)
        self.btn_Plan.setObjectName(u"btn_Plan")
        self.btn_Plan.setMinimumSize(QSize(0, 30))
        self.btn_Plan.setFont(font1)

        self.verticalLayout_4.addWidget(self.btn_Plan)

        self.verticalSpacer_4 = QSpacerItem(20, 412, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_4)

        icon4 = QIcon()
        icon4.addFile(u":/icon/icon/trello \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toolBox.addItem(self.bonus_page, icon4, u"\u041e\u0442\u0447\u0435\u0442")

        self.gridLayout.addWidget(self.toolBox, 0, 0, 1, 1)

        self.splitter.addWidget(self.menu_widget)
        self.main_widget = QWidget(self.splitter)
        self.main_widget.setObjectName(u"main_widget")
        self.gridLayout_2 = QGridLayout(self.main_widget)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.search_widget = QWidget(self.main_widget)
        self.search_widget.setObjectName(u"search_widget")
        self.search_widget.setStyleSheet(u"")
        self.horizontalLayout = QHBoxLayout(self.search_widget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(10, 0, 0, 0)
        self.toggleButton = QPushButton(self.search_widget)
        self.toggleButton.setObjectName(u"toggleButton")
        self.toggleButton.setMinimumSize(QSize(40, 40))
        icon5 = QIcon()
        icon5.addFile(u":/icon/icon/chevrons-left \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.toggleButton.setIcon(icon5)
        self.toggleButton.setIconSize(QSize(25, 25))
        self.toggleButton.setCheckable(True)

        self.horizontalLayout.addWidget(self.toggleButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.widget = QWidget(self.search_widget)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(70, 0))
        self.verticalLayout_5 = QVBoxLayout(self.widget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(50, 50))
        self.label.setMaximumSize(QSize(50, 60))
        self.label.setPixmap(QPixmap(u":/image/logo/\u043b\u043e\u0433\u043e_\u043a\u0430\u043f\u043b\u044f.ico"))
        self.label.setScaledContents(True)

        self.verticalLayout_5.addWidget(self.label)


        self.horizontalLayout.addWidget(self.widget)

        self.label_prog_name = QLabel(self.search_widget)
        self.label_prog_name.setObjectName(u"label_prog_name")
        self.label_prog_name.setMinimumSize(QSize(150, 0))
        self.label_prog_name.setMaximumSize(QSize(16777215, 16777215))
        font3 = QFont()
        font3.setFamilies([u"Tahoma"])
        font3.setPointSize(22)
        font3.setBold(True)
        self.label_prog_name.setFont(font3)
        self.label_prog_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.label_prog_name, 0, Qt.AlignmentFlag.AlignHCenter)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.frame_AppBtn = QFrame(self.search_widget)
        self.frame_AppBtn.setObjectName(u"frame_AppBtn")
        self.frame_AppBtn.setStyleSheet(u"")
        self.frame_AppBtn.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_AppBtn.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_AppBtn)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.minimizeAppBtn = QPushButton(self.frame_AppBtn)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        icon6 = QIcon()
        icon6.addFile(u":/icon/icon/minus \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon6)
        self.minimizeAppBtn.setIconSize(QSize(18, 18))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.frame_AppBtn)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        icon7 = QIcon()
        icon7.addFile(u":/icon/icon/maximize-2 \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon7)
        self.maximizeRestoreAppBtn.setIconSize(QSize(18, 18))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.frame_AppBtn)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        icon8 = QIcon()
        icon8.addFile(u":/icon/icon/x \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.closeAppBtn.setIcon(icon8)
        self.closeAppBtn.setIconSize(QSize(18, 18))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.frame_AppBtn)


        self.gridLayout_2.addWidget(self.search_widget, 0, 0, 1, 2)

        self.tabWidget = QTabWidget(self.main_widget)
        self.tabWidget.setObjectName(u"tabWidget")
        font4 = QFont()
        font4.setPointSize(10)
        self.tabWidget.setFont(font4)
        self.tabWidget.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.tabWidget.setStyleSheet(u"\n"
"#tabWidget {\n"
"	background-color: #f8f8f2;\n"
"}\n"
"\n"
"QTabBar::close-button {\n"
"	margin-left: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:selected  {\n"
"    background-color: #f09d54;\n"
"	color: #ffffff;\n"
"}  \n"
"QTabBar::tab:!selected {\n"
"    background-color: #f8f8f2; \n"
"	color: #ba5706\n"
"}")
        self.tabWidget.setIconSize(QSize(10, 10))
        self.tabWidget.setTabsClosable(True)

        self.gridLayout_2.addWidget(self.tabWidget, 1, 0, 1, 1)

        self.bottomWidget = QWidget(self.main_widget)
        self.bottomWidget.setObjectName(u"bottomWidget")
        self.bottomWidget.setMinimumSize(QSize(0, 20))
        self.bottomWidget.setMaximumSize(QSize(16777215, 20))
        self.horizontalLayout_3 = QHBoxLayout(self.bottomWidget)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(9, 0, 0, 0)
        self.label_produced = QLabel(self.bottomWidget)
        self.label_produced.setObjectName(u"label_produced")

        self.horizontalLayout_3.addWidget(self.label_produced)

        self.frame_size_grip = QWidget(self.bottomWidget)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 20))
        self.frame_size_grip.setMaximumSize(QSize(20, 20))
        self.frame_size_grip.setStyleSheet(u"image: url(:/icon/icon/more-horizontal \u2014 \u043a\u043e\u043f\u0438\u044f \u2014 \u043a\u043e\u043f\u0438\u044f.svg);")

        self.horizontalLayout_3.addWidget(self.frame_size_grip)


        self.gridLayout_2.addWidget(self.bottomWidget, 2, 0, 1, 2)

        self.splitter.addWidget(self.main_widget)

        self.appMargins.addWidget(self.splitter, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.toggleButton.toggled.connect(self.menu_widget.setHidden)

        self.toolBox.setCurrentIndex(0)
        self.toolBox.layout().setSpacing(6)
        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        self.btn_Home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_Dashboard.setText(QCoreApplication.translate("MainWindow", u"Dashboard", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.general_page), QCoreApplication.translate("MainWindow", u"General", None))
        self.btn_Managers.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u044b", None))
        self.btn_Customers.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043b\u0438\u0435\u043d\u0442\u044b", None))
        self.btn_Products.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0434\u0443\u043a\u0442\u044b", None))
        self.btn_Plans.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043b\u0430\u043d\u044b", None))
        self.btn_Costs.setText(QCoreApplication.translate("MainWindow", u"Tax / Fees", None))
        self.btn_Supplier.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u0438", None))
        self.btn_AddCosts.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043f \u0420\u0430\u0441\u0445\u043e\u0434\u044b (\u0417\u0430\u043a\u0443\u043f)", None))
        self.btn_CustDelivery.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0434\u043e \u043a\u043b\u0438\u0435\u043d\u0442\u0430", None))
        self.btn_Price.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0430\u0439\u0441-\u043b\u0438\u0441\u0442\u044b", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.updater_page), QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043e\u0447\u043d\u0438\u043a\u0438", None))
        self.btn_Purchases.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043a\u0443\u043f\u043a\u0438", None))
        self.btn_Purch_Orders.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043a\u0430\u0437\u044b \u043f\u043e\u0441\u0442\u0430\u0432\u0449\u0438\u043a\u043e\u0432", None))
        self.btn_Sales.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u043e\u0434\u0430\u0436\u0438", None))
        self.btn_Cust_Orders.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043a\u0430\u0437\u044b \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432", None))
        self.btn_MarketPlace.setText(QCoreApplication.translate("MainWindow", u"\u041c\u0430\u0440\u043a\u0435\u0442 \u041f\u043b\u0435\u0439\u0441\u044b", None))
        self.btn_Complect.setText(QCoreApplication.translate("MainWindow", u"\u041a\u043e\u043c\u043f\u043b\u0435\u043a\u0442\u0430\u0446\u0438\u0438", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.docs_page), QCoreApplication.translate("MainWindow", u"\u0414\u043e\u043a\u0443\u043c\u0435\u043d\u0442\u044b", None))
        self.btn_Scheme.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u043e\u0442\u0447\u0435\u0442", None))
        self.btn_Plan.setText(QCoreApplication.translate("MainWindow", u"\u041e\u0417\u041e\u041d", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.bonus_page), QCoreApplication.translate("MainWindow", u"\u041e\u0442\u0447\u0435\u0442", None))
        self.toggleButton.setText("")
        self.label.setText("")
        self.label_prog_name.setText(QCoreApplication.translate("MainWindow", u"Phoenix Lubricants Report Program", None))
        self.minimizeAppBtn.setText("")
        self.maximizeRestoreAppBtn.setText("")
        self.closeAppBtn.setText("")
        self.label_produced.setText(QCoreApplication.translate("MainWindow", u"By: Fokina Maria", None))
        pass
    # retranslateUi

