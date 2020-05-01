# MangaSpider (CLI)

从工口Manga网站18comic.vip下载指定漫画的项目。

## 环境需求
win10 + python3.7(64位)
未在Linux和mac下进行测试，理论上应该也可以跑得通

## 使用方法

1. 在18comic.vip找到你想下载的漫画的manga_id（就是网址中的那串编号）
![id](https://github.com/StoneForests/MangaSpider/blob/master/readme/id.png?raw=true "id")
2. 打开CMD:

```shell
git clone https://github.com/StoneForests/MangaSpider
pip install -r requirements.txt
python 18Comic.py -i <manga_id>
```

3. 等待下载完成

## 已知问题
1. 一次只能下载一部漫画
2. 未采用多进/线程，速度较慢
3. 未采用任何高端框架

## 下一步计划
1. 一次下载多部漫画，例如下载指定页面所有漫画
2. 加入多进/线程，加快速度
3. 试用通用框架改写，例如Scrapy
