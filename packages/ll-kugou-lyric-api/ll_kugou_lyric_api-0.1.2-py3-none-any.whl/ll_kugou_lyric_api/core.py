import base64
import requests
import urllib.parse
import re

class KugouApi:
    def __init__(self,title,artist): 
        self.title = title
        self.artist = artist
    
    def get_kugou_lrc(self):
        """
        通过歌曲名称+作者。模糊匹配歌词
        :return: 未找到返回None.找到返回解析后的LRC文本
        """
        # TODO 需要keyword进行url进行编码。否则有些符号会出问题
        keyword =  self.artist + " - "+self.title
        url = f'http://krcs.kugou.com/search?ver=1&man=yes&client=mobi&keyword={urllib.parse.quote(keyword)}&duration=&hash=&album_audio_id='
        res = requests.get(url)
        if res.status_code == 200:
            json_data = res.json()
            if len(json_data["candidates"])==0:
                if self.has_brackets(self.title):
                    print('检测到标题有括弧内容。重新请求中')
                    self.title=self.clean_char(self.title)
                    return self.get_kugou_lrc()
                if self.has_brackets(self.artist):
                    print('检测到作者有括弧内容。重新请求中')
                    self.artist=self.clean_char(self.artist)
                    return self.get_kugou_lrc()
            url = f'https://lyrics.kugou.com/download?ver=1&client=pc&id={json_data["candidates"][0]["id"]}&accesskey={json_data["candidates"][0]["accesskey"]}&fmt=lrc&charset=utf8'
            res = requests.get(url).json()
            res = base64.b64decode(res['content']).decode("utf-8")
        else:
            res = None
        return res
    
    def clean_char(self,str):
        """
        删除括号及括号内内容，支持(), （）,【】,〔〕,｛｝等
        """
        return re.sub(r'[\(\（\[\【\〔\{｛][^)\）\]\】\〕\}｝]*[\)\）\]\】\〕\}｝]', '', str)
    
    def has_brackets(self,text):
        """ 
        判断是否包含任意一种括号对
        """
        return re.search(r'[\(\（\[\【\〔\{｛].*?[\)\）\]\】\〕\}｝]', text) is not None