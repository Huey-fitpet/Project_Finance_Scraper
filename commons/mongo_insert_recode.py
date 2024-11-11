import pandas as pd

class connect_mongo:
    def insert_recode_in_mongo(client, dbname, collectionname, input_list):

        # 'mydatabase' 데이터베이스 선택 (없으면 자동 생성)
        db = client[dbname]
        # 'users' 컬렉션 선택 (없으면 자동 생성)
        collection = db[collectionname]

        # 데이터 입력
        # results = collection.insert_many(input_list)
        # data frame insert 시 to_dict 해야함. 아니면 아래 에러가 남
        # The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
        # results = collection.insert_many(input_list.to_dict(orient='records'))

        if isinstance(input_list, pd.DataFrame): # DataFrame인 경우
            results = collection.insert_many(input_list.to_dict(orient='records'))
        elif isinstance(input_list, list): # 리스트인 경우
            results = collection.insert_many(input_list)
        elif isinstance(input_list, dict): # 딕셔너리인 경우
            results = collection.insert_one(input_list)
        else:
            print("error")

        return results