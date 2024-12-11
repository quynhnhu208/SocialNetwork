import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import getpass
from datetime import datetime
import os

class FacebookGroupScraper:
    def __init__(self):
        print("\n====FACEBOOK GROUP MEMBER SCARPER=====")
        self.get_config()
        self.setup_driver()
        self.login()

    def get_config(self):
        try:
            # Thong tin dang nhap
            print("Nhap thong tin dang nhap:")
            self.email = input("Email/Username: ").strip()
            self.password = getpass.getpass("Password: ")     # An mat khau

            # Id Group
            print("\n Nhap ID group facebook:")
            self.group_id = input("Group ID: ").strip()

            # So lan scroll
            print("\nSo lan scroll de load them thanh vien")
            self.scroll_count = int(input("So lan scroll (mac dinh 5)") or "5")
        except Exception as e:
            print(f"Loi cau hinh: {e}")
            pass

    def setup_driver(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()    #Toan man hinh
        except Exception as e:
            print(f"Loi khoi tao trinh duyet: {e}")
            pass

    def login(self):
        try:
            self.driver.get("https://www.facebook.com")

            #Nhap email
            email_input = self.driver.find_element(By.ID, "email")
            email_input.send_keys(self.email)

            #Nhap password
            pass_input = self.driver.find_element(By.ID, "pass")
            pass_input.send_keys(self.password)

            #Click dang nhap
            login_button = self.driver.find_element(By.NAME, "login")
            login_button.click()

            time.sleep(120)
            print("Dang nhap thanh cong")
            return True
        except Exception as e:
            print(f"Loi dang nhap: {e}")
            return False
        
    def get_group_members(self):
        try:
            self.driver.get(f"https://www.facebook.com/groups/{self.group_id}/members")
            time.sleep(5)

            members = set()  # Dung set de khong bi trung lap

            for i in range(self.scroll_count):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)
                print(f"Scroll lan {i+1}/{self.scroll_count}")

                # Thu thap thong tin sau moi lan scroll
                user_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/user/']")
                
                # print(len(user_elements))
                for user in user_elements:
                    try:
                        href = user.get_attribute('href')
                        if '/user/' in href:
                            user_id = href.split('/user')[1].strip('/')
                            name = user.text
                            # members.add((user_id, name))
                            # print(user_id, " - ", name)

                        if name != '':
                            members.add((user_id, name))
                            print(user_id, "-", name)
                
                    except Exception:
                        continue
            return members

        except Exception as e:
            print(f"Loi thu thap thanh vien: {e}")
            pass
    
    def data_to_excel(self, data, excel_file=None):
        infos = []
        for info in data:
            info_data = {
                'id': info[0],
                'name': info[1]
            }
            infos.append(info_data)

        df = pd.DataFrame(infos)

        if not excel_file:
            timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            excel_file = f"facebook_infomations_{timestamp}.xlsx"

        try:
            df.to_excel(excel_file, index=True, engine='openpyxl')
            print(f"File Excel đã lưu tại: {excel_file}")
        except Exception as e:
            print(f"Lỗi khi lưu file Excel: {e}")
        return None
    
def main():
    scraper = None
    try:
        scraper = FacebookGroupScraper()
        data = scraper.get_group_members()
        scraper.data_to_excel(data)
    except Exception:
        pass

if __name__=="__main__":
    main()
