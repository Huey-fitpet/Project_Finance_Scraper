import requests
import json

class ApiRequester:

    def send_api(base_url, params, keys = None):
        response = requests.get(base_url, params=params)
        print(response.status_code)
        if response.status_code == 200 :
            if response.text !='[]' :
                content = json.loads(response.content)

                if keys == None :
                    return content
                else :
                    ############################# 
                    result_list = []

                    # content가 리스트가 아닐 경우, 단일 항목을 처리
                    if not isinstance(content, list):
                        content = [content]  # 단일 항목을 리스트로 변환

                    # 모든 항목에 대해 키를 사용하여 ret_contents 생성
                    for con in content:
                        item_dict = {key: con[key] for key in keys}
                        result_list.append(item_dict)

                    return result_list
                # return {'lat' : int(content[0]['lat']), 'lon' : int(content[0]['lon'])}
                
            else :
                print(f"error : result empty {response.content}")
                return None
        else :
            print(f"error : {response.status_code}")
            return None       
        pass