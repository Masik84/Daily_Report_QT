import os
import pandas as pd
from PySide6.QtWidgets import QApplication, QMainWindow, QApplication, QGraphicsDropShadowEffect, QSizeGrip
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve

from db import Base, engine
from pages_functions.home import Home
from pages_functions.product import Product
from pages_functions.managers import Managers
from pages_functions.customer import Customer
from pages_functions.plans import Plans
from pages_functions.cost import Costs
from pages_functions.supplier import SupplierWidget
from pages_functions.add_costs import AddSupplCosts

from pages_functions.move import MovesPage
from pages_functions.marketplace import MarketplacePage

from pages_functions.dashboard import Dashboard

from pages_functions.invoice import Rep_Invoices
from pages_functions.order import Rep_Orders

from wind.main_window_ui import Ui_MainWindow


# alembic revision --autogenerate -m "fixed_naming"
# alembic upgrade head
# pyside6-rcc -o resource_rc.py resource.qrc

WINDOW_SIZE = 0


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.centralwidget.setGraphicsEffect(self.shadow)

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())
        # MAXIMIZE/RESTORE
        self.ui.maximizeRestoreAppBtn.clicked.connect(lambda: self.maximize_restore())
        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())
        # SLIDE MENU
        self.ui.toggleButton.clicked.connect(lambda: self.toggleMenu())
        self.ui.search_widget.mouseMoveEvent = self.MoveWindow
        
        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")
        # APPLY DROPSHADOW TO FRAME
        self.ui.frame_size_grip.setGraphicsEffect(self.shadow)
        
        ## =======================================================================================================
        ## Get all the objects in windows
        ## =======================================================================================================
        self.home_btn = self.ui.btn_Home
        self.dashboard_btn = self.ui.btn_Dashboard
        self.btn_managers = self.ui.btn_Managers
        self.btn_customer = self.ui.btn_Customers
        self.btn_product = self.ui.btn_Products
        self.btn_plans = self.ui.btn_Plans
        self.btn_cost = self.ui.btn_Costs
        self.btn_supplier = self.ui.btn_Supplier
        self.btn_addcosts = self.ui.btn_AddCosts
        
        self.btn_moves = self.ui.btn_Moves
        self.btn_MP = self.ui.btn_MarketPlace
        
        self.btn_order = self.ui.btn_Cust_Orders
        self.btn_sales = self.ui.btn_Sales
        


        ## =======================================================================================================
        ## Create dict for menu buttons and tab windows
        ## =======================================================================================================
        self.menu_btns_list = {
            self.home_btn: Home(),
            self.dashboard_btn: Dashboard(),
            self.btn_managers: Managers(),
            self.btn_customer: Customer(),
            self.btn_product: Product(),
            self.btn_plans: Plans(),
            self.btn_cost: Costs(),
            self.btn_supplier: SupplierWidget(),
            self.btn_addcosts: AddSupplCosts(),
            
            self.btn_moves: MovesPage(),
            self.btn_MP: MarketplacePage(),
            
            self.btn_order: Rep_Orders(),
            self.btn_sales: Rep_Invoices(),

        }

        ## =======================================================================================================
        ## Show home window when start app
        ## =======================================================================================================
        self.show_home_window()

        ## =======================================================================================================
        ## Connect signal and slot
        ## =======================================================================================================
        self.ui.tabWidget.tabCloseRequested.connect(self.close_tab)

        self.home_btn.clicked.connect(self.show_selected_window)
        self.dashboard_btn.clicked.connect(self.show_selected_window)
        self.btn_managers.clicked.connect(self.show_selected_window)
        self.btn_customer.clicked.connect(self.show_selected_window)
        self.btn_product.clicked.connect(self.show_selected_window)
        self.btn_plans.clicked.connect(self.show_selected_window)
        self.btn_cost.clicked.connect(self.show_selected_window)
        self.btn_supplier.clicked.connect(self.show_selected_window)
        self.btn_addcosts.clicked.connect(self.show_selected_window)
        
        self.btn_moves.clicked.connect(self.show_selected_window)
        self.btn_MP.clicked.connect(self.show_selected_window)
        
        self.btn_order.clicked.connect(self.show_selected_window)
        self.btn_sales.clicked.connect(self.show_selected_window)
        


        ## =======================================================================================================

    def show_home_window(self):
        """
        Function for showing home window
        :return:
        """
        result = self.open_tab_flag(self.home_btn.text())
        self.set_btn_checked(self.home_btn)

        if result[0]:
            self.ui.tabWidget.setCurrentIndex(result[1])
        else:
            title = self.home_btn.text()
            curIndex = self.ui.tabWidget.addTab(Home(), title)
            self.ui.tabWidget.setCurrentIndex(curIndex)
            self.ui.tabWidget.setVisible(True)

    def show_selected_window(self):
        """
        Function for showing selected window
        :return:
        """
        button = self.sender()

        result = self.open_tab_flag(button.text())
        self.set_btn_checked(button)

        if result[0]:
            self.ui.tabWidget.setCurrentIndex(result[1])
        else:
            title = button.text()
            curIndex = self.ui.tabWidget.addTab(self.menu_btns_list[button], title)
            self.ui.tabWidget.setCurrentIndex(curIndex)
            self.ui.tabWidget.setVisible(True)

    def close_tab(self, index):
        """
        Function for close tab in tabWidget
        :param index: index of tab
        :return:
        """
        self.ui.tabWidget.removeTab(index)

        if self.ui.tabWidget.count() == 0:
            self.ui.toolBox.setCurrentIndex(0)
            self.show_home_window()

    def open_tab_flag(self, tab):
        """
        Check if selected window showed or not
        :param tab: tab title
        :return: bool and index
        """
        open_tab_count = self.ui.tabWidget.count()

        for i in range(open_tab_count):
            tab_name = self.ui.tabWidget.tabText(i)
            if tab_name == tab:
                return True, i
            else:
                continue

        return False,

    def set_btn_checked(self, btn):
        """
        Set the status of selected button checked and set other buttons' status unchecked
        :param btn: button object
        :return:
        """
        for button in self.menu_btns_list.keys():
            if button != btn:
                button.setChecked(False)
            else:
                button.setChecked(True)

    def maximize_restore(self):
        global WINDOW_SIZE
        status = WINDOW_SIZE
        if status == 0:
            WINDOW_SIZE = 1
            self.showMaximized()

            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_restore.png"))
        else:
            WINDOW_SIZE = 0
            self.showNormal()

            self.resize(self.width() + 1, self.height() + 1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(QIcon(u":/icons/images/icons/icon_maximize.png"))

    def mousePressEvent(self, event):
        self.oldPos = self.window().mapFromGlobal(event.globalPosition())

    def MoveWindow(self, event):
        if self.isMaximized() == False:
            delta = self.window().mapFromGlobal(event.globalPosition()) - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = self.window().mapFromGlobal(event.globalPosition())
    
    def toggleMenu(self):
        width = self.ui.menu_widget.width()
        maxExtend = 220
        standard = 60

        # SET MAX WIDTH
        if width == 60:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QPropertyAnimation(self.ui.menu_widget, b"minimumWidth")
        self.animation.setDuration(500)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()


if __name__ == '__main__':
    import sys
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_QPA_PLATFORM"] = "windows"
    # Uncomment the following line if the above doesn't work
    # QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    

    app = QApplication(sys.argv)
    Base.metadata.create_all(bind=engine)

    window = MyWindow()
    window.show()

    sys.exit(app.exec())
