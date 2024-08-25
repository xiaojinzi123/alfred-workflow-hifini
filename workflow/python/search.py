import argparse
import json
import requests
from lxml import etree
from urllib import parse as urlParse
from dataclasses import dataclass


@dataclass
class SearchClassResultItem:
    subPath: str
    name: str


def main():
    parser = argparse.ArgumentParser()

    # 参数 keyword, 用于搜索, 类型是字符串, 需要用 --keyword 指定
    parser.add_argument(
        "--keyword",
        type=str,
        help="search keyword",
    )

    args = parser.parse_args()

    searchKeyword = args.keyword

    # 开始搜索
    search(searchKeyword)


def search(searchKeyword):
    """执行搜索"""

    # 休眠 5s
    # time.sleep(5)

    searchKeywordEncoded = urlParse.quote(
        f"search-{searchKeyword}.htm",
    )

    targetSearchUrl = f"https://www.hifini.com/{searchKeywordEncoded}"

    response = requests.get(targetSearchUrl)
    if response.status_code == 200:
        responseHtml = etree.fromstring(response.text, etree.HTMLParser())
        # 找出 class 是 "media-body" 所有元素
        resultItems: list[etree._Element] = responseHtml.xpath(
            "//div[@class='media-body']",
        )
        # 打印 resultItems 的类型
        # print(type(resultItems))
        # print(len(resultItems))

        # 声明 搜索结果
        searchClassResultItemList: list[SearchClassResultItem] = []

        # 循环 resultItems
        for resultItem in resultItems:
            subPath = None
            musicTitle = None
            try:
                aLebal: etree._Element = resultItem.getchildren()[0].getchildren()[0]
                # 提取 A 标签内的所有文本
                musicTitle = aLebal.xpath("string(.)")
                # 获取这个 A 标签中的 href 属性
                subPath = aLebal.attrib["href"]
            except Exception:
                pass

            # print(f"{subPath} {musicTitle}")
            searchClassResultItemList.append(
                SearchClassResultItem(
                    subPath=subPath,
                    name=f"{musicTitle}",
                ),
            )

        """ {
            # "uid": "xxxxx",
            # "type": "file",
            "title": f"{searchKeyword}",
            # "subtitle": "~/xxxxx",
            "arg": targetSearchUrl,
            # "icon": {"type": "fileicon", "path": "~/Desktop"},
        } """
        resultDict = {
            "items": [],
        }

        for searchClassResultItem in searchClassResultItemList:
            resultDict["items"].append(
                {
                    "title": searchClassResultItem.name,
                    "arg": f"https://www.hifini.com/{searchClassResultItem.subPath}",
                },
            )

        resultJson = json.dumps(resultDict)
        print(resultJson)

    else:  # 请求失败
        resultDict = {
            "items": [
                {
                    "title": f"请求失败",
                }
            ],
        }
        resultJson = json.dumps(resultDict)
        print(resultJson)


if __name__ == "__main__":
    # print(f"{datetime.now()}")
    main()
