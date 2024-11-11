
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
    result_cont = []
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
        # result_cont = ApiRequester.send_api(base_url, params_w)
        result_cont.append(ApiRequester.send_api(base_url, params_w))

        # print(result_cont)
    return result_cont


def register_job_with_mongo(client, ip_add, db_name, col_name, func, insert_data):
    
    result_data = func(*insert_data)

    try:
        if client is None:
            client = MongoClient(ip_add) # 관리 신경써야 함.

        result_list = connect_mongo.insert_recode_in_mongo(client, db_name, col_name, result_data)
        # print(f'insert id list count : {len(result_list.inserted_ids)}')
    except Exception as e :
        print(e)
    # finally:
    #     client.close()
    return 

import logging
def main(message):

    # ip url tag 등등 최대한 전달 할 수 있도록 

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

    # MongoDB 연결 설정
    mongo_client = MongoClient('mongodb://192.168.0.91:27017/')
    db = mongo_client['log_database']  # 사용할 데이터베이스 이름
    log_collection = db['logs']  # 사용할 컬렉션 이름

    # MongoDB에 로그 저장 함수
    def log_to_mongo(level, message):
        log_entry = {
            'level': level,
            'message': message,
            'timestamp': logging.Formatter('%(asctime)s').format(logging.LogRecord('', 0, '', 0, '', '', '', '')),
        }
        log_collection.insert_one(log_entry)

    # 로깅 설정
    class MongoDBHandler(logging.Handler):
        def emit(self, record):
            log_entry = self.format(record)
            log_to_mongo(record.levelname, log_entry)

    # 로깅 핸들러 추가
    mongo_handler = MongoDBHandler()
    mongo_handler.setLevel(logging.INFO)
    mongo_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(mongo_handler)


    # 스케쥴러 등록 
    # mongodb 가져올 수 있도록
    ip_add = f'mongodb://192.168.0.91:27017/'
    db_name = f'lotte_db_sanghoonlee'
    col_name = f'lotte_col_sanghoonlee'

    # MongoDB 서버에 연결 : Both connect in case local and remote
    client = MongoClient(ip_add) # 관리 신경써야 함.

    scheduler = BackgroundScheduler()
    
    check_flag = [] # 리스트가 나으려나?


    url = f'http://underkg.co.kr/news'

    insert_data = [url] # [val1,val2,val3]
    
    func_list = [
        {"func" : bs4_scrapping.do_scrapping, "args" : insert_data},
        {"func" : api_test_func,  "args" : insert_data}
    ]

    # working function 등록
    # id에 함수명 같은거 넣으면 나중에 어느 함수에서 문제 있었는지 알 수 있을 듯
    for func in func_list:
        scheduler.add_job(register_job_with_mongo, 
                        trigger='interval', 
                        seconds=10, 
                        coalesce=True, 
                        max_instances=1,
                        # args=[args_list]
                        args=[client, ip_add, db_name, col_name, func['func'], func['args']]
                        )

    # 등록된 함수들 상태 check function
    # 작업 상태 확인 함수
    def check_jobs(check_flag):
        jobs = scheduler.get_jobs()
        for job in jobs:
            check_flag.append(job)
            pass
            #logging.info(f"Job ID: {job.id}, Next Run Time: {job.next_run_time}, Trigger: {job.trigger}")

    # 상태 체크 작업 추가 (5초마다 실행)
    scheduler.add_job(check_jobs, 'interval', seconds=5, id='check_jobs_id', max_instances=1, coalesce=True, args=[check_flag])
    # 정제 function 등록

    # 스케쥴러 시작 밑 에러데이터 로거 
    # 어떤 시도가 성공 했는지 
    # 어떤 시도가 실패 했는지
    # 왜 실패 했는지
    # 다른 행동에 영향을 주는지 
    # check_flag = set_flag() <= add_job 안에서 셋되어야 함.
    try:
        scheduler.start()
        #logger.info("스케줄러가 시작되었습니다.")
        pass
        # 메인 루프
        while True:
            pass
            if check_flag :
                pass

    except Exception as e:
        # logger.error(f"스케줄러에서 오류 발생: {e}")
        pass

    finally:
        scheduler.shutdown()
        # logger.info("스케줄러가 종료되었습니다.")
        pass
        return True


if __name__ == '__main__':
    main(f'task forever!')
