import base64
import requests


class KugouApi:
    def __init__(self,title,artist): 
        self.title = title
        self.artist = artist
    
    def get_kugou_lrc(self):
        """
        通过歌曲名称+作者。模糊匹配歌词
        :return: 未找到返回None.找到返回解析后的LRC文本
        """
        keyword =  self.artist + " - "+self.title
        url = f'http://krcs.kugou.com/search?ver=1&man=yes&client=mobi&keyword={keyword}&duration=&hash=&album_audio_id='
        res = requests.get(url)
        if res.status_code == 200:
            json_data = res.json()
            url = f'https://lyrics.kugou.com/download?ver=1&client=pc&id={json_data["candidates"][0]["id"]}&accesskey={json_data["candidates"][0]["accesskey"]}&fmt=lrc&charset=utf8'
            res = requests.get(url).json()
            res = base64.b64decode(res['content']).decode("utf-8")
        else:
            res = None
        return res
        