# coding: utf-8
# Версия 0.2a
# upd: 20-12-2015
# upd: 22-12-2015 v 0.2a
# upd: 11-01-2015 v 0.1b

import sys
import socket
from urllib import request
import json
import configparser
import logging
import threading
from datetime import datetime
from PyQt5 import QtWidgets, QtGui

logging.basicConfig(format='%(levelname)-4s [%(asctime)s] %(message)s', level=logging.DEBUG, filename='.//debug.log')


class SystemTray(QtWidgets.QSystemTrayIcon):

    _about_str = u'''
Версия 0.2a
Overdese
2015-2016 год
    '''

    _stat_str = u'''
Имя компьютера: %s

Скачано/Квота:
Неделя %0.2f MB/%0.2f MB
Месяц %0.2f MB/%0.2f MB

Обновлено в %s
'''

    _stat_warn_str = u'''
Имя компьютера: %s

Произошла ошибка при обновлении информации.
Если это сообщение появляется постоянно - обратитесь к администратору.

'''

    def __init__(self, icon, parent=None):
        super(SystemTray, self).__init__(icon, parent)

        self._load_conf()

        menu = QtWidgets.QMenu(parent)
        self.menu_about_act = menu.addAction('О программе')
        self.menu_about_act.triggered.connect(self._app_about)
        self.menu_exit_act = menu.addAction('Выход')
        self.menu_exit_act.triggered.connect(self._app_exit)
        self.setContextMenu(menu)

        self.activated.connect(self._app_tray_clicked)

        self.update_error = True
        self.hostname = socket.getfqdn()
        self.ip = socket.gethostbyname(socket.getfqdn())
        self.quota_week = 0
        self.week_down = 0
        self.quota_month = 0
        self.month_down = 0
        self.dt_update = datetime.now()

        self._update_statistic()

    def _app_tray_clicked(self, reason):
        if reason == self.Trigger:
            if self.update_error:
                self.showMessage(u'Статистика пользования интернетом',
                                 self._stat_warn_str % self.hostname,
                                 self.Warning)
            else:
                self.showMessage(u'Статистика пользования интернетом',
                                 self._stat_str % (self.hostname,
                                                   self.week_down,
                                                   self.quota_week,
                                                   self.month_down,
                                                   self.quota_month,
                                                   self.dt_update.strftime('%H:%M'),
                                                   ))

    def _app_exit(self):
        logging.info('Stop app')
        sys.exit()

    def _app_about(self):
        mb = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                   'О программе',
                                   self._about_str)

        mb.setWindowIcon(QtGui.QIcon(mb.style().standardPixmap(QtWidgets.QStyle.SP_ArrowDown)))
        mb.exec()

    def _load_conf(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            self._site_url = config.get('general', 'site_url')
            self._update_time = config.getfloat('general', 'update_time')
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            logging.error('Error while load config file config.ini')
            logging.info('Stop app')
            sys.exit()

    def _update_statistic(self):
        try:
            data = request.urlopen('%s/api/client/%s/' % (self._site_url, self.ip)).read()
            json_data = json.loads(data.decode())
            if json_data['status'] == 'success':
                self.quota_week = int(json_data['data']['quota_week'])/1024/1024
                self.week_down = int(json_data['data']['week_down'])/1024/1024
                self.quota_month = int(json_data['data']['quota_month'])/1024/1024
                self.month_down = int(json_data['data']['month_down'])/1024/1024
            self.update_error = False
            self.dt_update = datetime.now()
        except Exception as e:
            self.update_error = True
            logging.error(e)
        timer = threading.Timer(self._update_time, self._update_statistic)
        timer.daemon = True
        timer.start()


def main():
    logging.info('Start app')
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    style = app.style()
    # w = QtWidgets.QWidget()
    # tray_icon = TrayIcon(QtGui.QIcon(style.standardPixmap(QtWidgets.QStyle.SP_ArrowDown)), w)
    tray_icon = SystemTray(QtGui.QIcon(style.standardPixmap(QtWidgets.QStyle.SP_ArrowDown)))
    tray_icon.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
