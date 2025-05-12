from pathlib import Path 
import sys
from build_stats import process_district
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QGridLayout 
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont 

from gui import Ui_MainWindow
from house_stats_gui import Ui_Form

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.title_label = self.ui.title_label
        self.title_label.setText("Меню")
        font = QFont()
        font.setBold(True)
        font.setPixelSize(26)
        self.title_label.setFont(font)

        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only = self.ui.listWidget_icon_only
        self.side_menu_icon_only.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.side_menu_icon_only.hide()

        self.menu_btn = self.ui.pushButton
        self.menu_btn.setObjectName("menu_btn")
        self.menu_btn.setText("")
        self.menu_btn.setIcon(QIcon("./icon/close.svg"))
        self.menu_btn.setIconSize(QSize(30, 30))
        self.menu_btn.setCheckable(True)
        self.menu_btn.setChecked(False)

        self.main_content = self.ui.stackedWidget 

        self.menu_list = [
            {
                "name": "Отсканировать новый регион",
                "icon": "./icon/plagiarism.png"
            },
            {
                "name": "Показать статистику домов",
                "icon": "./icon/house.png"
            },
            {
                "name": "Посмотреть сколько отсканировано",
                "icon": "./icon/scan_count.png"
            },
            {
                "name": "Дополнительная информация",
                "icon": "./icon/info.png"
            }
        ]

        self.init_list_widget()
        self.init_signal_slot()
        self.init_stackwidget()

    def init_signal_slot(self):
        self.menu_btn.toggled["bool"].connect(self.side_menu.setHidden)
        self.menu_btn.toggled["bool"].connect(self.title_label.setHidden)
        self.menu_btn.toggled["bool"].connect(self.side_menu_icon_only.setVisible)  

        self.side_menu.currentRowChanged["int"].connect(self.main_content.setCurrentIndex)
        self.side_menu_icon_only.currentRowChanged["int"].connect(self.main_content.setCurrentIndex)
        self.side_menu.currentRowChanged['int'].connect(self.side_menu_icon_only.setCurrentRow)
        self.side_menu_icon_only.currentRowChanged['int'].connect(self.side_menu.setCurrentRow) 

        self.menu_btn.toggled.connect(self.button_icon_change) 

    def button_icon_change(self, status):
        if status:
            self.menu_btn.setIcon(QIcon("./icon/open.svg"))
        else:
            self.menu_btn.setIcon(QIcon("./icon/close.svg"))

    def init_list_widget(self):   
        self.side_menu.clear()
        self.side_menu_icon_only.clear()

        for menu in self.menu_list:
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setSizeHint(QSize(40, 40))
            self.side_menu_icon_only.addItem(item)
            self.side_menu_icon_only.setCurrentRow(0)

            item_new = QListWidgetItem()
            item_new.setIcon(QIcon(menu.get("icon")))
            item_new.setText(menu.get("name"))
            self.side_menu.addItem(item_new)
            self.side_menu.setCurrentRow(0)

    def init_stackwidget(self):
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
            self.main_content.removeWidget(widget)

        for index, menu in enumerate(self.menu_list):
            if menu.get("name") == "Показать статистику домов":
            # Подключаем форму из house_stats_gui.py
                new_page = HouseStatsWidget()
            else:
            # Заглушка для остальных
                layout = QGridLayout()
                label = QLabel(text=menu.get("name"))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont()
                font.setPixelSize(20)
                label.setFont(font)
                layout.addWidget(label)
                new_page = QWidget()
                new_page.setLayout(layout)
        
            self.main_content.addWidget(new_page)


class HouseStatsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

def gui_launch():   
    app = QApplication(sys.argv)
    
    with open("./CSS/style.css") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)
    
    window = MainWindow()
    window.showMaximized()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    gui_launch()