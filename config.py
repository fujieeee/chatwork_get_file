import pprint
from logging import getLogger, INFO, basicConfig

API_TOKEN = "XXXX"

# chatworkのhtmlファイル(ここの部分は取得処理作ってない）
FILE_NAME = 'XXXX.html'
# chatworkのチャンネルごとのルームID
ROOM_ID = 'XXXX'
# 画像保存先のパス
SAVE_PATH = 'XXXXX'

# chatwork APIのURI
FILE_INFO_API = "https://api.chatwork.com/v2/rooms/" \
                + ROOM_ID \
                + "/files/CHATWORKFILEID?create_download_url=1"
REPLACE_WORD = "CHATWORKFILEID"
# なんでもいいと思う
USER_AGENT \
        = 'Mozilla/5.0 (Linux; Android 7.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) ' \
          'Chrome/92.0.4515.159 Mobile Safari/537.36 '
# APIのヘッダーを設定している。ここでTOKENを設定
CONFIG_HEADER = {
        'User-Agent': USER_AGENT,
        'X-ChatWorkToken': API_TOKEN
    }

basicConfig(level=INFO, format=' %(levelname)s - %(message)s')
LOGGER = getLogger(__name__)

pp = pprint.PrettyPrinter(indent=4)