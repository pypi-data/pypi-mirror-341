# Kugou Lyrics API

这是一个用于获取酷狗音乐歌词的 Python API 包。

## 安装

1. 克隆项目：

    ```bash
    git clone https://github.com/1053278842/kugou_lyric_api.git
    cd kugou_lyric_api
    ```

2. 安装本地开发模式：

    使用以下命令安装当前项目包（以便进行开发和修改）：

    ```bash
    pip install -e .
    ```

    这将会安装项目并使其可在本地环境中开发。

## 使用

在 Python 环境中使用本项目，以下是如何导入和使用该包的示例：

```python
from ll_kugou_lyric_api.core import KugouApi

if __name__ == "__main__":
    kugou_api = KugouApi("朵","赵雷")  # 创建实例

    lyrics = kugou_api.get_kugou_lrc()
    print(lyrics)  # 打印歌词
