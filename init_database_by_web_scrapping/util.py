import os
import re

import glob
import datetime

from datetime import datetime
from zoneinfo import ZoneInfo

import pickle
import pandas as pd

from tqdm.auto import tqdm

import base64

def base64_encode(s):
    """
    주어진 문자열을 base64로 인코딩합니다.
    
    Args:
    s: 인코딩할 문자열.
    
    Returns:
    base64로 인코딩된 문자열.
    """
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')


def base64_decode(s):
    """
    주어진 base64 문자열을 디코딩합니다.
    
    Args:
    s: 디코딩할 base64 문자열.
    
    Returns:
    디코딩된 문자열.
    """
    return base64.b64decode(s.encode('utf-8')).decode('utf-8')

def now_korea():
    return datetime.now(ZoneInfo("Asia/Seoul"))

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



def get_latest_file_paths(folder_path):
    """
    특정 폴더에서 조건에 맞는 가장 최근 파일 두 개의 경로를 반환합니다.

    Args:
        folder_path: 파일을 찾을 폴더 경로

    Returns:
        튜플: (codetable 파일 경로, data 파일 경로). 파일이 없으면 None을 반환합니다.
               두 파일 중 하나라도 찾지 못하면 None을 반환합니다.
        예외: 폴더 경로가 유효하지 않은 경우 FileNotFoundError를 발생시킵니다.
    """

    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"폴더 경로 '{folder_path}'가 존재하지 않습니다.")

    codetable_files = []
    data_files = []

    # 파일 목록 얻기 (glob 사용)
    for filename in glob.glob(os.path.join(folder_path, "*.pkl")):
        if "_codetable_data_" in filename:
            codetable_files.append(filename)
        elif "codetable" not in filename and "_data_" in filename:
            data_files.append(filename)

    if not codetable_files or not data_files:
        return None

    # 파일 수정 시간으로 정렬 (내림차순)
    codetable_files.sort(key=os.path.getmtime, reverse=True)
    data_files.sort(key=os.path.getmtime, reverse=True)

    codetable_file = codetable_files[0]
    data_file = data_files[0]

    if 'selected_codetable_data_backup.pkl' in data_files:
        codetable_file_file = 'selected_codetable_data_backup.pkl'

    if 'selected_data_backup.pkl' in data_files:
        data_file = 'selected_data_backup.pkl'

    return codetable_file, data_file