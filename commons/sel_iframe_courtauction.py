
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import pandas as pd
import re
import time

class iframe_test : 
    
    def get_data(browser: webdriver.Chrome) -> pd.DataFrame:
        # tag 목록 나중에 빼서 관리 할 수 있도록 
        case_id_tag = f'#contents > div.table_contents > form:nth-child(1) > table > tbody > tr > td:nth-child(2)'
        property_address_tag = f'#contents > div.table_contents > form > table > tbody > tr > td:nth-child(4)'
        estimated_value_tag = f'#contents > div.table_contents > form > table > tbody > tr > td.txtright'
        
        # get data : return data 
        case_id_list = browser.find_elements(by=By.CSS_SELECTOR, value=case_id_tag)
        property_address_list = browser.find_elements(by=By.CSS_SELECTOR, value=property_address_tag)
        estimated_value_list = browser.find_elements(by=By.CSS_SELECTOR, value=estimated_value_tag)
        
        case_data = {
            "case_id" : [],
            "property_address" : [],
            "estimated_value" : []
        }

        for number, row in enumerate(case_id_list):
            print(f'number:{number}, title : {row.accessible_name}')
            case_data["case_id"].append(row.accessible_name)
        
        for number, row in enumerate(property_address_list): # 한 번호당 여러개
            print(f'number:{number}, title : {row.accessible_name}')
           # 정규 표현식을 사용하여 데이터 자르기
            # 대괄호([])로 묶인 부분을 기준으로 자르기
            pattern = r'([^\[]*\[[^\]]*\])'
            matches = re.findall(pattern, row.accessible_name)

            # 결과를 리스트에 담기
            result_list = [match.strip() for match in matches]
            case_data["property_address"].append(result_list)

        for number, row in enumerate(estimated_value_list): # 한 번호당 여러개
            print(f'number:{number}, title : {row.accessible_name}')
            case_data["estimated_value"].append(row.accessible_name)

        return pd.DataFrame(case_data)
    
    def select_court(browser: webdriver.Chrome) -> webdriver.Chrome:
                
        target_url = f'https://www.courtauction.go.kr/'
        btn_tag = f'#main_btn > a'
        sel_list_tag = f'#idJiwonNm1'

        # - 주소 입력(https://www.w3schools.com/)
        browser.get(target_url)
        
        # frame 선택 - 이게 되야 element 접근 가능
        browser.switch_to.frame("indexFrame")
        time.sleep(1)

        # 리스트 선택
        element_select = browser.find_element(by=By.CSS_SELECTOR, value=sel_list_tag)
        # Select 객체 생성
        select = Select(element_select)
        index = 8 # 인천 지방 법원
        select.select_by_index(index)
        time.sleep(1)

        # 클릭 넣기 
        element_btn = browser.find_element(by=By.CSS_SELECTOR, value=btn_tag)
        element_btn.click()
        time.sleep(1)

        return browser


    # 쓸 때 browser 관리 
    def run(browser: webdriver.Chrome) -> pd.DataFrame:
        iframe_test.select_court(browser) 
        return iframe_test.get_data(browser)