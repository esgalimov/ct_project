import scipy.constants as constants


# stars masses
STARS_DICT = {'Солнце': 1, 'Альфа Центавра': 0.9, 'Бетельгейзе': 11,
              'Сириус': 2, 'Арктур': 1.3, 'Ригель': 18, 'Альдебаран': 2.5}
# astronomical unit in meterы
A_E = 1.5 * (10 ** 11)
# Solar mass in kg
SOLAR_MASS = 1.989 * (10 ** 30)
# Gravity constant
G = constants.G
# time delay between points
DT = 30
# points number
N = 2000000
# infinity number
INF = 10 ** 16