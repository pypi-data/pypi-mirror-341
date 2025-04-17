from ll_kugou_lyric_api.core import KugouApi

if __name__ == "__main__":
   # api =  KugouApi("朵","赵雷")
   # api =  KugouApi("Kids","Two Door Cinema Club")
   # api =  KugouApi("Пятница (星期五)","Дела Поважнее")
   # api =  KugouApi("You Make My Dreams (Come True)","Daryl Hall & John Oates")
   api =  KugouApi("Пятница (星期五)","Дела Поважнее")
   print(api.get_kugou_lrc()) 
   
   