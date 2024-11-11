
# 스크래퍼 import 
from apscheduler.schedulers.background import BackgroundScheduler
# mongo DB 동작
from pymongo import MongoClient
# time.sleep
import time

# selenium driver 
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

# 직접 만든 class 
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
from commons.mongo_insert_recode import connect_mongo
from commons.api_send_requester import ApiRequester
from commons.sel_iframe_courtauction import iframe_test
from commons.bs4_do_scrapping import bs4_scrapping
# from get_classes import getfuctions as gf
# import webscraping_imglink_func as wf_img
# import webscraping_newscontent_func as wf_news


def api_test_func(test):
    # api
    city_list = ['도쿄','괌','모나코']
    key_list = ['lat', 'lon']
    pub_key = '39fb7b1c6d4e11e7483aabcb737ce7b0'
    for city in city_list:
        base_url = f'https://api.openweathermap.org/geo/1.0/direct'
        
        params={}
        params['q'] = city
        params['appid'] = pub_key

        result_geo = ApiRequester.send_api(base_url, params, key_list)

        base_url = f'https://pro.openweathermap.org/data/2.5/weather'
        
        params_w = {}
        for geo in result_geo:
            for key in key_list:
                params_w[key] = geo[key]
        params_w['appid'] = pub_key
        result_cont = ApiRequester.send_api(base_url, params_w)

        print(result_cont)


def register_job_with_mongo(client, ip_add, db_name, col_name, func, insert_data):
    client = MongoClient(ip_add) # 관리 신경써야 함.
    result_data = func(*insert_data)

    try:
        result_list = connect_mongo.insert_recode_in_mongo(client, db_name, col_name, result_data)
        # print(f'insert id list count : {len(result_list.inserted_ids)}')
    except Exception as e :
        print(e)
    finally:
        client.close()
    return 

def main(message):

    # ip url tag 등등 최대한 전달 할 수 있도록 
    # # api
    # city_list = ['도쿄','괌','모나코']
    # key_list = ['lat', 'lon']
    # pub_key = '39fb7b1c6d4e11e7483aabcb737ce7b0'
    # for city in city_list:
    #     base_url = f'https://api.openweathermap.org/geo/1.0/direct'
        
    #     params={}
    #     params['q'] = city
    #     params['appid'] = pub_key

    #     result_geo = ApiRequester.send_api(base_url, params, key_list)

    #     base_url = f'https://pro.openweathermap.org/data/2.5/weather'
        
    #     params_w = {}
    #     for geo in result_geo:
    #         for key in key_list:
    #             params_w[key] = geo[key]
    #     params_w['appid'] = pub_key
    #     result_cont = ApiRequester.send_api(base_url, params_w)

    #     print(result_cont)

    # # 아직 실행 안됨 
    # # selenium
    # webdriver_manager_directory = ChromeDriverManager().install() # 딱 한번 수행이라 밖에
    # # ChromeDriver 실행
    # browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
    # # try - finally 자원 관리 필요 
    # try:
    #     case_data = iframe_test.run(browser)
    # except Exception as e :
    #     print(e)
    # finally:
    #     browser.quit()

    # bs4
    # url = f'http://underkg.co.kr/news'
    # news_datas = bs4_scrapping.do_scrapping(url)

    # 스케쥴러 등록 
    # mongodb 가져올 수 있도록
    ip_add = f'mongodb://192.168.0.91:27017/'
    db_name = f'lotte_db_sanghoonlee'
    col_name = f'lotte_col_sanghoonlee'

    # MongoDB 서버에 연결 : Both connect in case local and remote
    client = MongoClient(ip_add) # 관리 신경써야 함. # 다시 닫히는거 로직 변경해야함.

    scheduler = BackgroundScheduler()
    
    url = f'http://underkg.co.kr/news'

    # scheduler.add_job(bs4_scrapping.do_scrapping, 
    #                   trigger='interval', 
    #                   seconds=10, 
    #                   coalesce=True, 
    #                   max_instances=1,
    #                   # args=[args_list]
    #                   args=[url]
    #                   )

    insert_data = [url] # [val1,val2,val3]
    scheduler.add_job(register_job_with_mongo, 
                      trigger='interval', 
                      seconds=10, 
                      coalesce=True, 
                      max_instances=1,
                      # args=[args_list]
                      args=[client, ip_add, db_name, col_name, bs4_scrapping.do_scrapping, insert_data]
                      )

    insert_data = [url] # [val1,val2,val3]
    scheduler.add_job(register_job_with_mongo, 
                      trigger='interval', 
                      seconds=10, 
                      coalesce=True, 
                      max_instances=1,
                      # args=[args_list]
                      args=[client, ip_add, db_name, col_name, api_test_func, insert_data]
                      )
    
    # ip_add = f'mongodb://192.168.0.63:27017/'
    # db_name = f'news_database_sanghoonlee'
    # col_name = f'news_collection_sanghoonlee'
    # #folder = f'./downloads'
    # #url = f'https://www.yna.co.kr/economy/all'

    # args_list = [ip_add,db_name,col_name,folder,url] # wf_news는 folder,url 적용 안됨

    # scheduler.add_job(wf_news.main, 
    #                   trigger='interval', 
    #                   seconds=5, 
    #                   coalesce=True, 
    #                   max_instances=1,
    #                   args=[args_list]
    #                   )
    
    scheduler.start()
    # 정지 예방
    count = 0
    while True:
        #time.sleep(3)
        #print(f'{message} : count - {count}')
        #count += 1

        pass
    
    return True


if __name__ == '__main__':
    main(f'task forever!')
