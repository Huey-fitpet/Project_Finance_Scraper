
# 공통 부분을 import 하여 구현
from commons.api_send_requester import ApiRequester

class api_test_class:
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