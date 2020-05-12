import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .Message import ft, CdutEmail
import time
import paramunittest
import yaml

# 将括号内的地址修改为你的data.yml存放地址
with open(r'D:\python3\健康打卡\data.yml', encoding='utf-8')as fp_stream:
    datalist = yaml.load(fp_stream, Loader=yaml.FullLoader)


@paramunittest.parametrized(*datalist)
class CdutHealth(unittest.TestCase):
    def setParameters(self, user, pwd, province=None, city=None, county=None, address=None, SCKEY=None,
                      mail_address=None, zzmm='团员', FDY=None, mentor=None, parent=None, messageType=2):
        self.username = user
        self.password = pwd
        self.province = province
        self.city = city
        self.county = county
        self.address = address
        self.SCKEY = SCKEY
        self.Mail_address = mail_address
        self.zzmm = zzmm
        self.FDY = FDY
        self.mentor = mentor
        self.parent = parent
        self.messageType = messageType

    def setUp(self):
        # 用哪个就把另一个注释掉
        # self.driver = webdriver.Chrome('F:\Chrome Driver\chromedriver_win32\chromedriver.exe')  # 括号内为你的Chromedriver存放路径
        self.driver = webdriver.Edge('F:\Edge Driver\edgedriver_win64\msedgedriver.exe')       # 括号内为你的MicrosoftEdge driver存放路径

    def test_python(self):
        driver = self.driver
        driver.get(
            'https://authserver.cdut.edu.cn/authserver/login?service=https%3A%2F%2Fehall.cdut.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.cdut.edu.cn%2Fnew%2Findex.html')
        username = driver.find_element_by_id("username")
        username.send_keys(self.username)
        passwd = driver.find_element_by_id("password")
        passwd.send_keys(self.password)
        driver.find_element_by_class_name('dl-button').click()
        time.sleep(3)
        try:
            driver.find_element_by_class_name('ampHeaderSearchFlag').click()
            element = driver.find_element_by_id('ampServiceSearchInput')
            element.clear()
            element.send_keys("学生健康状况信息采集系统")
            element.send_keys(Keys.RETURN)
            assert "No results found." not in driver.page_source
            time.sleep(2)  # 等待浏览器加载搜索元素
            health = driver.find_element_by_class_name('amp-service-search-color')
            health.click()
            time.sleep(2)  # 休眠两秒，等待浏览器加载表格
            allwindows = driver.window_handles
            curwinodw = driver.current_window_handle
            if (len(allwindows) > 1 and curwinodw == allwindows[0]):
                driver.switch_to.window(allwindows[1])
            iframe1 = driver.find_element_by_xpath(
                '/html/body/div[1]/div/div/div[2]/div/table/tbody/tr/td[2]/div[2]/div/iframe')  # 寻找第一个内嵌表格
            driver.switch_to.frame(iframe1)  # driver切换到第一个表格
            iframe2 = driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/table/tbody/tr/td[2]/div[2]/div/iframe')  # 寻找第二个内嵌表格
            driver.switch_to.frame(iframe2)  # 切换第二个表格
            driver.find_element_by_id('ZZMM$text').send_keys(self.zzmm)  # 政治面貌
            driver.find_element_by_id('mini-37').click()
            driver.find_element_by_id('FDY$text').send_keys(self.FDY)  # 辅导员名称
            driver.find_element_by_id('DSXM$text').send_keys(self.mentor)  # 导师姓名
            driver.find_element_by_id('JZLX$text').send_keys(self.parent)  # 父母联系方式
            driver.find_element_by_id('mini-2$0').click()  # 点击确认按钮
            print("开始寻找是否有黑龙江旅居史框")
            driver.find_element_by_id('mini-42$ck$1').click()  # 点击否
            # print("开始寻找是否有小区隔离史")
            # driver.find_element_by_id('mini-66$ck$1').click()  # 点击否
            print("开始寻找体温属性")
            temprature = driver.find_element_by_id('TW$text')  # 寻找体温属性
            temprature.send_keys('36.5')  # 输入体温
            print('填写当前地址')
            driver.find_element_by_id('SSQ21$text').send_keys(self.province)  # 填写省
            driver.find_element_by_id('mini-56').click()  # 点击下拉栏
            driver.find_element_by_id('SSQ22$text').send_keys(self.city)  # 填写市
            driver.find_element_by_id('mini-60').click()  # 点击市的下拉栏
            driver.find_element_by_id('SSQ23$text').send_keys(self.county)
            driver.find_element_by_id('mini-64').click()  # 点击县的下拉栏
            driver.find_element_by_id('SZDXXDZ$text').send_keys(self.address)
            driver.switch_to.default_content()  # 切换回顶层表单
            driver.switch_to.frame(iframe1)  # 切换为第一层表单
            driver.find_element_by_id('sendBtn').click()  # 寻找提交按钮并点击
            print('finished')
            time.sleep(1)
            element = driver.find_element_by_id('mini-17')  # 寻找弹出页面框的确认按钮
            element.click()
            print('Another test')

        except Exception as e:
            if self.messageType == 1:
                ft.sendft()
            else:
                CdutEmail.sendEmail()

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main(verbosity=2)
