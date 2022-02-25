import requests
import os
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
from config import *
from requests.exceptions import Timeout
import time


def main():
    LOGGER.info('処理開始')
    # 定義ファイルから読み込み
    save_path = SAVE_PATH
    soup = BeautifulSoup(open(FILE_NAME), 'lxml')
    # ファイルIDを取得
    arr_file_id = get_file_id_list(soup)
    # [開発用]ファイルIDを表示
    pp.pprint(arr_file_id)

    for index, list_id in enumerate(arr_file_id):
        # ファイルダウンロードのURLを取得処理
        file_info_json = get_file_info(arr_file_id[index])
        if file_info_json == "":
            continue
        # 保存先のパス、画像ページのURL、画像一覧の番号
        save_images(save_path, file_info_json)

    # after_exec()
    LOGGER.info('処理終了')


def get_file_info(file_id: str) -> str:
    # Chatwork APIでファイルダウンロードURLを取得
    api_url = FILE_INFO_API.replace(REPLACE_WORD, file_id)
    LOGGER.info(api_url)

    time.sleep(1)
    req = request_get(api_url)
    if req.status_code != 200:
        LOGGER.warn(req)
        return ""
    else:
        response_json = req.json()
        LOGGER.info(str(response_json))
        return response_json


def request_get(url: str) -> requests:
    for i in range(3):
        try:
            # connect timeoutが3.0秒、read timeoutが7.5秒
            return requests.get(url, headers=CONFIG_HEADER, timeout=(3.0, 7.5))
        except Timeout:
            LOGGER.warning('Timed out: ' + url)
            i += 1
    # リトライ処理をしてもTimeoutの場合は終了
    return requests


def get_soup(url: str) -> BeautifulSoup:
    req = request_get(url)
    return BeautifulSoup(req.text, 'lxml')


# ファイルID一覧返却
def get_file_id_list(soup: BeautifulSoup) -> list:
    # 画像ファイルのタグを取得
    arr_page_img = soup.find_all("img", class_="sc-jgrJph")

    arr_img_url = []
    for img in arr_page_img:
        if img['data-file-id'] is not None:
            file_id = img['data-file-id']
            arr_img_url.append(file_id)
    return arr_img_url


def is_exist_url_in_file(list_url: str, path: str, isFile: bool) -> bool:
    chk = False
    if os.path.isfile(path):
        # すでに読み込み済みのURLかどうかチェック
        with open(path, 'r') as ro_files:
            for file_url in ro_files:
                file_url = file_url.strip()
                # 既に一覧全ての画像をDL済みの場合は次のループへ
                if list_url == file_url:
                    chk = True
                    message = 'skipped：' + file_url
                    if isFile:
                        # ログを見やすくするためにインデント追加
                        message = '  ' + message
                    LOGGER.info(message)

                    break
    return chk


def save_images(save_path: str, file_info_json: str) -> bool:
    file_name = str(file_info_json['file_id']) + "_" + file_info_json['filename']
    file_path = '{}/{}'.format(save_path, file_name)
    LOGGER.info(file_name)
    if os.path.isfile(file_path):
        LOGGER.info('exist: ' + file_path)
    else:
        response = request_get(file_info_json['download_url'])
        time.sleep(1)
        LOGGER.info('status_code: ' + str(response.status_code))
        if response.status_code == 200:
            i = Image.open(BytesIO(response.content))
            if i.mode != "RGB":
                i = i.convert("RGB")
            i.save(file_path, 'JPEG', quality=100)
            LOGGER.info('Saved! ' + file_name)


if __name__ == '__main__':
    main()
