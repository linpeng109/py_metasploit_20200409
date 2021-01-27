import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QScrollArea, QVBoxLayout
from pymetasploit3.msfrpc import MsfRpcClient

from py_config import ConfigFactory
from py_logging import LoggerFactory


class Arping:
    def get_arping_data(self):
        client = MsfRpcClient(server='192.168.1.119', username='msf', password='msf', port=55552)
        exploit = client.modules.use(mtype='auxiliary', mname='scanner/discovery/arp_sweep')
        exploit['RHOSTS'] = '192.168.1.100-200'
        exploit['THREADS'] = 5
        cid = client.consoles.console().cid
        console = client.consoles.console(cid)
        result = console.run_module_with_output(exploit)
        print(result)
        console.destroy()
        return result


if __name__ == '__main__':
    arping = Arping()
    result = arping.get_arping_data()

    config = ConfigFactory(config_file='py_metasploit.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    mainWindow.setWindowTitle('软件机器人抓取数据')
    mainWindow.resize(640, 480)

    labal = QLabel(str(result))
    labal.setWordWrap(True)

    scroll_label = QScrollArea()
    scroll_label.setFixedSize(640, 480)

    layout = QVBoxLayout()
    layout.addWidget(labal)

    scroll_label.setLayout(layout)
    mainWindow.setCentralWidget(scroll_label)
    mainWindow.show()
    sys.exit(app.exec_())
