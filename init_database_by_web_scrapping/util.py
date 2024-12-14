import re

import pickle
import pandas as pd

from tqdm.auto import tqdm

class JobDictToExcel:
    def __init__(self, data):
        self.data = data

    def sanitize_data(self, value):
        if isinstance(value, str):
            illegal_characters = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]", re.UNICODE)
            return illegal_characters.sub("", value)
        elif isinstance(value, set):
            return str(list(value))
        elif value is None:
            return None
        else:
            return str(value)

    def convert_to_excel(self, file_name):
        processed_data = []
        for key, value in tqdm(self.data.items(), desc="데이터 변환 중"):
            row = {"id": key}
            for k, v in value.items():
                row[k] = self.sanitize_data(v)
            processed_data.append(row)
        print("변환 완료")
        print("변환된 데이터를 판다스 객체로 저장합니다.")
        self.df = pd.DataFrame(processed_data)
        print(f"변환된 객체를 '{file_name}' 위치에 저장합니다.")
        self.df.to_excel(file_name, index=False)
        print("저장완료")

class ExcelToJobDict:
    @staticmethod
    def convert_to_dict(file_name):
        df = pd.read_excel(file_name)
        result = {}

        for _, row in tqdm(df.iterrows(), total=len(df), desc="Excel을 딕셔너리로 변환 중"):
            id_value = row["id"]
            result[id_value] = {}
            for col in df.columns:
                if col == "id":
                    continue
                value = row[col]
                if pd.isna(value):
                    result[id_value][col] = None
                elif isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                    result[id_value][col] = set(eval(value))
                else:
                    result[id_value][col] = value

        return result

def save_to_pickle(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)
    print(f"데이터가 {filename}에 성공적으로 저장되었습니다.")

def load_from_pickle(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    print(f"{filename}에서 데이터를 성공적으로 불러왔습니다.")
    return data