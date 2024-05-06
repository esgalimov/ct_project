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
        self.pushButton.clicked.connect(self.run)
        self.add_planet.clicked.connect(self.add)
        self.action_discard.triggered.connect(self.discard)
        self.dis_added.clicked.connect(self.discard_added)
        # списки полей ввода
        self.fields = [self.velocity, self.x_coord,
                       self.y_coord, self.angle, self.koeff, self.koeff1, self.star_mass]
        self.fields_3d = [self.x_3d, self.y_3d, self.z_3d,
                          self.vx_3d, self.vy_3d, self.vz_3d,
                          self.koeff_3d, self.koeff1_3d]

        self.solar_system_planets = [self.earth, self.mercury, self.venus,
                                     self.mars, self.jupiter, self.saturn,
                                     self.uranus, self.neptune, self.pluto]
        for planet in self.solar_system_planets:
            planet.triggered.connect(self.solar_system_input)

        for field in self.fields[:-1]:
            field.setText('0')
        for field in self.fields_3d:
            field.setText('0')
        self.star_mass_box.addItems(STARS_DICT.keys())
        self.star_mass_box.activated.connect(self.star_mass_box_func)
        self.star_mass_box_func()
        # окна
        self.about_window = AboutWindow()
        self.added_window = AddedWindow()
        self.error_widget = ErrorWidget()
        self.settings_window = SettingsWindow()

        self.action_about.triggered.connect(self.about)
        self.action_settings.triggered.connect(self.settings)
        self.action_added.triggered.connect(self.added_show)

        self.to_draw_2d = []
        self.to_draw_3d = []

        self.added_list = {'2d': [], '3d': []}

    def add(self):
        global N, DT
        gc.collect()
        if not plt.get_fignums():
            try:
                if self.tabWidget.currentIndex() == 0:
                    if sum([len(i[0]) + len(i[1]) for i in self.to_draw_2d]) +\
                            sum([len(i[0]) + len(i[1] + len(i[2])) for i in self.to_draw_3d]) + N > POINTS_LIMIT:
                        self.error_widget.label.setText('Ошибка: суммарно больше 20 000 000 точек')
                        self.error_widget.show()
                    else:
                        x0 = float(self.x_coord.text()) * A_E
                        y0 = float(self.y_coord.text()) * A_E
                        v0 = float(self.velocity.text())
                        alpha = float(self.angle.text())
                        M = float(self.star_mass.text()) * SOLAR_MASS
                        k = float(self.koeff.text())
                        k1 = float(self.koeff1.text())

                        x, y, vx, vy = count_2d(x0, y0, v0, alpha, M, N, DT, k1, k)
                        self.added_list['2d'].append(f'x0: {self.x_coord.text()} y0: {self.y_coord.text()},'
                                                     f' v0: {self.velocity.text()}, alpha: {self.angle.text()},'
                                                     f' M: {self.star_mass.text()},'
                                                     f' k1: {self.koeff1.text()}, k: {self.koeff.text()}')

                        self.to_draw_2d.append([x, y])

                else:
                    if sum([len(i[0]) + len(i[1] + len(i[2])) for i in self.to_draw_3d]) +\
                            sum([len(i[0]) + len(i[1]) for i in self.to_draw_2d]) + N > 20_000_000:
                        self.error_widget.label.setText('Ошибка: суммарно больше 20 000 000 точек')
                        self.error_widget.show()
                    else:
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

                        x, y, z, vx, vy, vz = count_3d(x0, y0, z0, vx0, vy0, vz0, M, N, DT, k1, k)
                        self.added_list['3d'].append(f'x0: {self.x_3d.text()} y0: {self.y_3d.text()},'
                                                     f' z0: {self.z_3d.text()}, vx0: {self.vx_3d.text()},'
                                                     f' vy0: {self.vy_3d.text()}, vz0: {self.vz_3d.text()},'
                                                     f' M: {self.star_mass.text()}, k1: {self.koeff1_3d.text()},'
                                                     f' k: {self.koeff_3d.text()}')

                        self.to_draw_3d.append([x, y, z])

            except ValueError:
                self.error_widget.label.setText('Ошибка: неверный формат ввода')
                self.error_widget.show()

            except ZeroDivisionError:
                self.error_widget.label.setText('Ошибка: неверный формат ввода')
                self.error_widget.show()

            except MemoryError:
                self.error_widget.label.setText('Ошибка: перегрузка памяти')
                self.error_widget.show()

    def run(self):
        if not plt.get_fignums():
            if self.tabWidget.currentIndex() == 0:
                if self.to_draw_2d == []:
                    self.add()
                if 0 < len(self.to_draw_2d) <= 3:
                    draw_2d(self.to_draw_2d)
                elif len(self.to_draw_2d) > 3:
                    self.error_widget.label.setText('Ошибка: больше 3 графиков')
                    self.error_widget.show()
            else:
                if self.to_draw_3d == []:
                    self.add()
                if 0 < len(self.to_draw_3d) <= 3:
                    draw_3d(self.to_draw_3d)
                elif len(self.to_draw_2d) > 3:
                    self.error_widget.label.setText('Ошибка: больше 3 графиков')
                    self.error_widget.show()

    def about(self):
        self.about_window.show()

    def settings(self):
        self.settings_window.show()

    def added_show(self):
        self.added_window.show()
        self.added_window.textEdit.clear()
        self.added_window.textEdit.append('2D')
        for i in self.added_list['2d']:
            self.added_window.textEdit.append(i)
        self.added_window.textEdit.append('3D')
        for i in self.added_list['3d']:
            self.added_window.textEdit.append(i)

    def discard(self):
        self.star_mass_box_func()
        for field in self.fields[:-1]:
            field.setText('0')
        for field in self.fields_3d:
            field.setText('0')

    def discard_added(self):
        self.to_draw_2d.clear()
        self.to_draw_3d.clear()
        self.added_list['2d'].clear()
        self.added_list['3d'].clear()

    def star_mass_box_func(self):
        self.star_mass.setText(str(STARS_DICT[self.star_mass_box.currentText()]))

    def solar_system_input(self):
        planet = self.solar_system_planets.index(self.sender()) + 1
        con = sqlite3.connect('planets_db.db')
        cur = con.cursor()
        result = cur.execute('select * from planets where id = ?', (planet, )).fetchone()
        self.velocity.setText(str(result[4]))
        self.x_coord.setText(str(result[2]))
        self.y_coord.setText(str(result[3]))
        self.angle.setText(str(result[5]))
        self.star_mass.setText(str(result[6]))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
