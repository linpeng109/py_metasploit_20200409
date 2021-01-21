from selenium.webdriver import Chrome, ActionChains
from selenium.webdriver.support import ui

from py_config import ConfigFactory
from py_logging import LoggerFactory


class OssimWeb:
    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        self.config = config
        self.logger = logger
        self.CHROME_DRIVER_LOCATION = 'D:/chromedriver/chromedriver.exe'
        self.OSSIM_URL = 'https://118.144.88.37:12343/ossim/session/login.php'
        self.chrome_driver = Chrome(executable_path=self.CHROME_DRIVER_LOCATION)

    def get_data(self):
        self.chrome_driver.get(url=self.OSSIM_URL)
        # self.wait = ui.WebDriverWait(self.chrome_driver, 10)
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
            lambda driver: driver.find_element_by_id('h_opt_real_time')).click()

        # 获取嵌套iframe页面'main'
        iframe = ui.WebDriverWait(driver=self.chrome_driver, timeout=50, poll_frequency=5).until(
            lambda driver: driver.find_element_by_id('main'))
        self.logger.debug('main')
        # 进入嵌套页面
        self.chrome_driver.switch_to.frame(iframe)
        # 获取嵌套页面上的table内容
        target = self.chrome_driver.find_element_by_tag_name('tbody')
        # target=self.chrome_driver.find_element_by_id('viewer')
        # str = self.chrome_driver.execute_script("return arguments[0]", target)
        str = target.get_attribute(target.get_property())
        self.logger.debug(str)


if __name__ == '__main__':
    config = ConfigFactory(config_file='py_metasploit.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()
    ossim = OssimWeb(config=config, logger=logger)
    ossim.get_data()
# element = brower.find_element_by_id('m_show item-with-ul')
# ActionChains(brower).move_to_element(element).perform()
# brower.find_element_by_id('sm_opt_analysis-security_events').click()
