import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QScrollArea, QVBoxLayout
from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import ui

from py_config import ConfigFactory
from py_logging import LoggerFactory


class OssimWeb:
    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        self.config = config
        self.logger = logger
        self.CHROME_DRIVER_LOCATION = 'D:/chromedriver/chromedriver.exe'
        self.OSSIM_URL = 'https://118.144.88.37:12343/ossim/session/login.php'
        chrome_options = Options()
        chrome_options.headless = False
        self.chrome_driver = Chrome(executable_path=self.CHROME_DRIVER_LOCATION, options=chrome_options)
        # self.chrome_driver = Chrome(executable_path=self.CHROME_DRIVER_LOCATION)

    def get_data(self):
        self.chrome_driver.get(url=self.OSSIM_URL)
        self.chrome_driver.implicitly_wait(10)
        # 等待detail元素出现
        ui.WebDriverWait(driver=self.chrome_driver, timeout=5, poll_frequency=5).until(
            lambda driver: driver.find_element_by_id('details-button'))

        self.chrome_driver.find_element_by_id('details-button').click()
        self.chrome_driver.find_element_by_id('proceed-link').click()

        # 等等user元素出现
        ui.WebDriverWait(driver=self.chrome_driver, timeout=5, poll_frequency=5).until(
            lambda driver: driver.find_element_by_id('user'))

        # 提交表单
        self.chrome_driver.find_element_by_id('user').send_keys('admin')
        self.chrome_driver.find_element_by_id('passu').send_keys('P@ssw0Rd')
        self.chrome_driver.find_element_by_id('submit_button').click()

        # 等待m_show元素出现
        ui.WebDriverWait(driver=self.chrome_driver, timeout=5, poll_frequency=5).until(
            lambda driver: driver.find_element_by_id('sm_opt_analysis-security_events'))

        # 移动鼠标到li_analysis元素上
        ActionChains(self.chrome_driver).move_to_element(self.chrome_driver.find_element_by_id('li_analysis')).perform()

        # 单击按钮
        self.chrome_driver.find_element_by_id('sm_opt_analysis-security_events').click()

        # 等待h_opt_real_time元素出现
        ui.WebDriverWait(driver=self.chrome_driver, timeout=10, poll_frequency=5).until(
            lambda driver: driver.find_element_by_id('h_opt_real_time'))
        self.chrome_driver.find_element_by_id('h_opt_real_time').click()

        # 获取嵌套iframe页面'main'
        iframe = ui.WebDriverWait(driver=self.chrome_driver, timeout=10, poll_frequency=5).until(
            lambda driver: driver.find_element_by_id('main'))

        # 进入嵌套页面
        self.chrome_driver.switch_to.frame(iframe)

        # 等待网页上class=table_data的标签出现
        ui.WebDriverWait(driver=self.chrome_driver, timeout=10, poll_frequency=5).until(
            lambda driver: driver.find_element_by_class_name('table_data'))
        # 获取网页上class=table_data的标签
        table = self.chrome_driver.find_element_by_class_name('table_data')

        # 获取tbody的内容
        tbody = table.find_elements_by_tag_name('tbody')[0]

        # 获取table中的每一行，组成list
        trs = tbody.find_elements_by_tag_name('tr')
        # 初始化数据表
        self.data_list = []
        # 每一行形成一个list，table的每个字段是list中的一个元素
        for each in trs:
            # 取得第一个td标记的文本内容，即每一行的第一个字段的内容，以此类推
            DATE = each.find_elements_by_tag_name('td')[0].text
            EVENT_NAME = each.find_elements_by_tag_name('td')[1].text
            RISK = each.find_elements_by_tag_name('td')[2].find_elements_by_tag_name('span')[0].text
            DATA_SOURCE = each.find_elements_by_tag_name('td')[3].text
            SENSOR = each.find_elements_by_tag_name('td')[4].text
            OTX = each.find_elements_by_tag_name('td')[5].text
            SOURCE_IP = each.find_elements_by_tag_name('td')[6].text
            DEST_IP = each.find_elements_by_tag_name('td')[7].text
            # 填充二维数据表
            self.data_list.append([DATE, EVENT_NAME, RISK, DATA_SOURCE, SENSOR, OTX, SOURCE_IP, DEST_IP])
        # self.chrome_driver.close()
        # self.chrome_driver.quit()

        return self.data_list


if __name__ == '__main__':
    config = ConfigFactory(config_file='py_metasploit.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()
    ossim = OssimWeb(config=config, logger=logger)
    result = ossim.get_data()

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    mainWindow.setWindowTitle('软件机器人抓取数据')
    mainWindow.resize(320, 240)

    labal = QLabel(str(result))
    labal.setWordWrap(True)

    scroll_label = QScrollArea()
    scroll_label.setFixedSize(300, 200)

    layout = QVBoxLayout()
    layout.addWidget(labal)
    # label.setWordWrap(True)

    scroll_label.setLayout(layout)
    mainWindow.setCentralWidget(scroll_label)
    mainWindow.show()
    sys.exit(app.exec_())
