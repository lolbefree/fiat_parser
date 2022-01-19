from selenium import webdriver, common
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from datetime import datetime
import urllib3
import os
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

class Parser:
    def __init__(self, vin):
        self.alert = ""
        self.vin = vin
        self.list_with_1 = list()
        self.list_with_2 = list()
        self.list_with_3 = list()
        self.res_list = list()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        self.data = {"data": True}

        self.cnt_1 = 1
        self.cnt_2 = 1
        self.cnt_3 = 1
        self.len_list_with_2 = int()
        self.len_list_with_3 = int()
        self.end_file = BaseException("Закончились пункты меню")
        self.session_expire = BaseException("ОБРЫВ СЕССИИ")

    def open_site(self):
        PROCNAME = "chromedriver.exe"

        hostname = 'linkentry-euro.fiat.com/pages/home/'
        proxy_username = 'proxy_username'
        proxy_password = "proxy_password"

        self.driver.get(f"https://{proxy_username}:{proxy_password}@{hostname}/")
        time.sleep(5)
        user = self.driver.find_element_by_xpath('//*[@id="userNameInput"]') #user
        user.send_keys(proxy_username)
        pw = self.driver.find_element_by_xpath('//*[@id="passwordInput"]') #pw
        pw.send_keys(proxy_password)
        self.driver.find_element_by_xpath('//*[@id="submitButton"]').click() #ok
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="ext-gen18"]').click()
        Link = self.driver.find_element_by_xpath('//*[@id="menu6362"]')
        webdriver.ActionChains(self.driver).move_to_element(Link).perform()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="ext-gen194"]').click()
        time.sleep(5)
        self.driver.get('https://aftersales.fiat.com/tempario/home.aspx?mercatoID=IT&languageID=ru-RU')
        time.sleep(5)


        vincode = self.driver.find_element_by_id("id_cerca_vin-inputEl")
        time.sleep(3)
        vincode.send_keys(f"{self.vin}")
        time.sleep(2)
        try:
            self.alert = self.driver.switch_to.alert
        except:
            print("no error message")
        if self.alert:
            print("iam here")
            raise ValueError



    def create_list(self, what_list):

        for row in self.driver.find_elements_by_css_selector("#gridview-1026-table"):
            for item in row.find_elements_by_tag_name("td"):
                if what_list == 'list_with_1':
                    self.list_with_1.append(item.text)
                elif what_list == 'list_with_2':
                    self.list_with_2.append(item.text)
                elif what_list == 'list_with_3':
                    self.list_with_3.append(item.text)

        time.sleep(10)

    def last_click(self):
        time.sleep(2)
        for item in self.driver.find_elements_by_tag_name("td"):
            if item.text != "":
                self.res_list.append(item.text)

    def step0(self):

        print(self.vin)
        print(self.cnt_1)
        time.sleep(2)
        if len(self.list_with_1) == 0:
            self.create_list("list_with_1")
            print(self.cnt_1)
        if self.cnt_1 > len(self.list_with_1) / 2:
            raise ValueError
        style = self.driver.find_element_by_xpath(
            f"/html/body/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/table/tbody/tr[{self.cnt_1}]/td[2]").get_attribute('style')
        if 'color' in style:
            print('unselectable="on"')
            self.cnt_1 += 1
            self.step0()
        else:
            if self.cnt_1 > len(self.list_with_1) / 2:
                print("where here")
                self.data["data"] = False
                raise ValueError
            if self.data["data"]:
                print(f"dlinna l1 = {len(self.list_with_1) / 2}")
                time.sleep(2)

            # style = self.driver.find_element_by_xpath(
            #     f"/html/body/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/table/tbody/tr[{self.cnt_1}]/td[2]").get_attribute('style')
            # if 'color' in style:
            #     print('unselectable="on"')
            #     self.cnt_1 += 1
                # self.step0()
            self.driver.find_element_by_xpath(
                f'/html/body/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/table/tbody/tr[{self.cnt_1}]/td[2]/div').click()
            self.data["data"] = False
            time.sleep(2)
            self.step1()
        print(self.data["data"] and self.cnt_1 <= len(self.list_with_1) / 2, self.cnt_1 > len(self.list_with_1) / 2, len(self.list_with_1) == 0)


    def step1(self):


        if len(self.list_with_2) == 0:
            self.create_list("list_with_2")
        if not self.list_with_2:
            print("pusto")

            self.driver.find_element_by_css_selector('#button_gruppi-btnIconEl').click()
            self.data["data"] = True
            self.cnt_1 += 1
            self.step0()
        self.len_list_with_2 = len(self.list_with_2) / 2
        time.sleep(2)
        self.driver.find_element_by_xpath(
            f'/html/body/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/table/tbody/tr[{self.cnt_2}]/td[2]/div').click()
        time.sleep(2)

        self.step2()

    def step2(self):
        print(f"len list2 {len(self.list_with_2)} len list3 {len(self.list_with_3)}")
        self.list_with_3.clear()
        time.sleep(2)
        self.create_list("list_with_3")
        self.len_list_with_3 = int(len(self.list_with_3) / 2)
        for item in range(1, self.len_list_with_3 + 1):
            self.driver.find_element_by_xpath(
                f'/html/body/div[3]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/table/tbody/tr[{item}]/td[2]/div').click()
            time.sleep(2)

            #  self.driver.find_element_by_css_selector('#button_sottogruppi-btnIconEl').click()
            self.last_click()
            self.driver.find_element_by_css_selector('#button_1_ssgruppi-btnIconEl').click()
            time.sleep(2)
        self.driver.find_element_by_css_selector('#button_sottogruppi-btnIconEl').click()
        self.cnt_2 += 1

        if self.cnt_2 >= int(self.len_list_with_2):
            self.driver.find_element_by_css_selector('#button_gruppi-btnIconEl').click()
            self.cnt_1 += 1
            self.data["data"] = True
            self.list_with_2.clear()
            self.cnt_2 = 1
            self.cnt_3 = 1
            self.step0()
        self.step1()



    def write_into_file(self, data_from_site):
        string = ''''''
        vin = self.vin[:-1]
        if not os.path.isfile(f"vin_result_{vin}.txt"):
            open(f"vin_result_{vin}.txt", "w", encoding="utf-8").close()
        with open(f"vin_result_{vin}.txt", "a", encoding="utf-8") as vin_result:
            if data_from_site:
                vin_result.write(vin + "\n")

                code = 0
                work_name = 1
                normative = 2

                dlinna = len(data_from_site)

                while dlinna != 0:
                    string += data_from_site[code] + ";" + data_from_site[work_name] + ";" + data_from_site[
                        normative] + "\n"
                    code += 4
                    normative += 4
                    work_name += 4
                    dlinna -= 4
                vin_result.write(string)
            else:
                vin_result.write(f"{self.vin} Session expired \n")

    def main_work(self):
        try:
            self.open_site()
            time.sleep(2)
            self.step0()
            time.sleep(5)
        except ValueError:
            self.write_into_file(self.res_list)
            print("next model")
        except:
            self.driver.quit()
            self.__init__(self.vin)
            self.main_work()
        finally:
            self.driver.quit()


print(f"start time is : {datetime.now()}")

with open('./vin.txt', 'r') as file_with_vincode:
    for line in file_with_vincode:
        child = Parser(f'{line}').main_work()
print("Программа заершена")
print("DONE!!!", datetime.now())
