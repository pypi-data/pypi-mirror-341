from ll_kugou_lyric_api.core import KugouApi

if __name__ == "__main__":
   api =  KugouApi("朵","赵雷")
   print(api.get_kugou_lrc())
   
   api =  KugouApi("Kids","Two Door Cinema Club")
   print(api.get_kugou_lrc())