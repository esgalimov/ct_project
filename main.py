import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow

import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import gc

from window_error import ErrorWidget
from window_settings import SettingsWindow
from window_main import Ui_MainWindow
from window_about import AboutWindow
from window_added import AddedWindow

from constants import *
from calc import *

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Построить button - create matplotlib graphs from added params
        self.pushButton.clicked.connect(self.run)

        # Добавить button - calculate and save calculated trajectories
        self.add_planet.clicked.connect(self.add)

        # Сбросить добавленное - delete written in text inputs
        self.action_discard.triggered.connect(self.discard)

        # Cбросить (menu) - delete saved trajectories
        self.dis_added.clicked.connect(self.discard_added)

        # Text input fields list in 2D page
        self.fields = [self.velocity, self.x_coord,
                       self.y_coord, self.angle, self.koeff, self.koeff1, self.star_mass]
        
        # Same in 3D page
        self.fields_3d = [self.x_3d, self.y_3d, self.z_3d,
                          self.vx_3d, self.vy_3d, self.vz_3d,
                          self.koeff_3d, self.koeff1_3d]

        # Planets in menu (click on them to fill text fields with them orbit params)
        self.solar_system_planets = [self.earth, self.mercury, self.venus,
                                     self.mars, self.jupiter, self.saturn,
                                     self.uranus, self.neptune, self.pluto]
        
        # Connect to method to get info from db about each planet
        for planet in self.solar_system_planets:
            planet.triggered.connect(self.solar_system_input)

        # Initial fields filling
        for field in self.fields[:-1]:
            field.setText('0')
        for field in self.fields_3d:
            field.setText('0')
        
        # Windows
        self.about_window = AboutWindow()
        self.added_window = AddedWindow()
        self.error_widget = ErrorWidget()
        self.settings_window = SettingsWindow()

        # Connect them to methods
        self.action_about.triggered.connect(self.about)
        self.action_settings.triggered.connect(self.settings)
        self.action_added.triggered.connect(self.added_show)

        # lists to save calculated trajectories 
        self.to_draw_2d = []
        self.to_draw_3d = []

        # dict to save params to show them to user in menu
        self.added_list = {'2d': [], '3d': []}

        # data base connection
        self.con = sqlite3.connect('planets_db.db')
        self.cur = self.con.cursor()

        # get all stars names
        stars = self.cur.execute('select name from stars').fetchall()

        # put stars names to list with stars widget
        self.star_mass_box.addItems([star[0] for star in stars])

        # connect click to star to method to get star mass from db
        self.star_mass_box.activated.connect(self.star_mass_box_func)
        self.star_mass_box_func()

    # Calculate and save trajectory
    # if more than POINTS_LIMIT points - error
    # catch some exceptions and show error_widgets
    def add(self):
        gc.collect()
        if not plt.get_fignums():
            try:
                if sum([len(i[0]) + len(i[1]) for i in self.to_draw_2d]) +\
                            sum([len(i[0]) + len(i[1] + len(i[2])) for i in self.to_draw_3d]) + self.settings_window.get_N() > POINTS_LIMIT:
                    self.error_widget.label.setText('Ошибка: суммарно больше 20 000 000 точек')
                    self.error_widget.show()
                
                else:
                    if self.tabWidget.currentIndex() == 0:
                        self.parse_count_2d()      
                    else:
                        self.parse_count_3d()

            except ValueError:
                self.error_widget.label.setText('Ошибка: неверный формат ввода')
                self.error_widget.show()

            except ZeroDivisionError:
                self.error_widget.label.setText('Ошибка: неверный формат ввода')
                self.error_widget.show()

            except MemoryError:
                self.error_widget.label.setText('Ошибка: перегрузка памяти')
                self.error_widget.show()

    def parse_count_2d(self):
        # parse text fields
        x0 = float(self.x_coord.text()) * A_E
        y0 = float(self.y_coord.text()) * A_E
        v0 = float(self.velocity.text())
        alpha = float(self.angle.text())
        M = float(self.star_mass.text()) * SOLAR_MASS
        k = float(self.koeff.text())
        k1 = float(self.koeff1.text())

        # save params to added list
        self.added_list['2d'].append(f'x0: {self.x_coord.text()} y0: {self.y_coord.text()},'
                                        f' v0: {self.velocity.text()}, alpha: {self.angle.text()},'
                                        f' M: {self.star_mass.text()},'
                                        f' k1: {self.koeff1.text()}, k: {self.koeff.text()}')

        # calc trajectories (x and y - np arrays) and save them
        x, y = count_2d(x0, y0, v0, alpha, M, self.settings_window.get_N(), self.settings_window.get_DT(), k1, k)
        self.to_draw_2d.append([x, y])
    
    # 3D analog to 2D :)
    def parse_count_3d(self):
        x0 = float(self.x_3d.text()) * A_E
        y0 = float(self.y_3d.text()) * A_E
        z0 = float(self.z_3d.text()) * A_E
        vx0 = float(self.vx_3d.text())
        vy0 = float(self.vy_3d.text())
        vz0 = float(self.vz_3d.text())
        k = float(self.koeff_3d.text())
        k1 = float(self.koeff1_3d.text())
        M = float(self.star_mass.text()) * SOLAR_MASS
        # print(x0, y0, z0, vx0, vy0, vz0, k, k1, M)

        self.added_list['3d'].append(f'x0: {self.x_3d.text()} y0: {self.y_3d.text()},'
                                        f' z0: {self.z_3d.text()}, vx0: {self.vx_3d.text()},'
                                        f' vy0: {self.vy_3d.text()}, vz0: {self.vz_3d.text()},'
                                        f' M: {self.star_mass.text()}, k1: {self.koeff1_3d.text()},'
                                        f' k: {self.koeff_3d.text()}')

        x, y, z = count_3d(x0, y0, z0, vx0, vy0, vz0, M, self.settings_window.get_N(), self.settings_window.get_DT(), k1, k)
        self.to_draw_3d.append([x, y, z])

    # draw saved or if not saved draw with params in fields
    def run(self):
        if not plt.get_fignums():
            if self.tabWidget.currentIndex() == 0:
                if self.to_draw_2d == []:
                    self.add()
                if 0 < len(self.to_draw_2d) <= 3:
                    draw_2d(self.to_draw_2d, self.settings_window.get_N())
                elif len(self.to_draw_2d) > 3:
                    self.error_widget.label.setText('Ошибка: больше 3 графиков')
                    self.error_widget.show()
            else:
                if self.to_draw_3d == []:
                    self.add()
                if 0 < len(self.to_draw_3d) <= 3:
                    draw_3d(self.to_draw_3d, self.settings_window.get_N())
                elif len(self.to_draw_2d) > 3:
                    self.error_widget.label.setText('Ошибка: больше 3 графиков')
                    self.error_widget.show()

    # show window about
    def about(self):
        self.about_window.show()

    # show settings window
    def settings(self):
        self.settings_window.show()

    # show added list in special window
    def added_show(self):
        self.added_window.show()
        self.added_window.textEdit.clear()
        self.added_window.textEdit.append('2D')
        for i in self.added_list['2d']:
            self.added_window.textEdit.append(i)
        self.added_window.textEdit.append('3D')
        for i in self.added_list['3d']:
            self.added_window.textEdit.append(i)

    # delete written in text input fields
    def discard(self):
        self.star_mass_box_func()
        for field in self.fields[:-1]:
            field.setText('0')
        for field in self.fields_3d:
            field.setText('0')

    # delete saved trajectories
    def discard_added(self):
        self.to_draw_2d.clear()
        self.to_draw_3d.clear()
        self.added_list['2d'].clear()
        self.added_list['3d'].clear()

    # get from db and write to field star mass
    def star_mass_box_func(self):
        star_name = self.star_mass_box.currentText()
        
        result = self.cur.execute('select * from stars where name = ?', (star_name, )).fetchone()
        self.star_mass.setText(str(result[2]))

    # get from db and write to field star mass
    def solar_system_input(self):
        planet = self.solar_system_planets.index(self.sender()) + 1
        result = self.cur.execute('select * from planets where id = ?', (planet, )).fetchone()

        self.velocity.setText(str(result[4]))
        self.x_coord.setText(str(result[2]))
        self.y_coord.setText(str(result[3]))
        self.angle.setText(str(result[5]))
        self.star_mass.setText(str(result[6]))

# decode exit code if programm finished with non-catched exception
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
