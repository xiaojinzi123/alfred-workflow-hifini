import argparse
import requests
import json
import os
from dataclasses import dataclass


@dataclass
class MusicSubUrl:
    # 绝对路径的 musicUrl
    absoluteMusicUrl: str | None = None
    value1: str | None = None
    value2: str | None = None


def getMusicSubUrl(htmlContent: str) -> MusicSubUrl | None:
    searchStartKeyword = "music: ["
    musicInfoListStartIndex = htmlContent.find(searchStartKeyword)
    if musicInfoListStartIndex == -1:
        return
    tempIndex1 = htmlContent.find("url: 'http", musicInfoListStartIndex)
    # 如果是绝对路径的
    if tempIndex1 != -1:
        tempIndex2 = htmlContent.find("',", tempIndex1)
        if tempIndex2 == -1:
            return
        return MusicSubUrl(
            absoluteMusicUrl=htmlContent[tempIndex1 + 6 : tempIndex2],
        )
    # 如果不是绝对路径的
    tempIndex1 = htmlContent.find("url: 'get_music", musicInfoListStartIndex)
    if tempIndex1 == -1:
        return
    tempIndex2 = htmlContent.find("'),", tempIndex1)
    if tempIndex2 == -1:
        return
    musicSubUrlValue = htmlContent[tempIndex1 + 6 : tempIndex2]
    tempKey = "' + generateParam('"
    tempIndex = musicSubUrlValue.find(tempKey)
    if tempIndex == -1:
        tempKey = "'+ generateParam('"
        tempIndex = musicSubUrlValue.find(tempKey)
    if tempIndex == -1:
        return
    musicSubUrlValue1 = musicSubUrlValue[:tempIndex]
    musicSubUrlValue2 = musicSubUrlValue[tempIndex + len(tempKey) :]

    return MusicSubUrl(
        value1=musicSubUrlValue1,
        value2=musicSubUrlValue2,
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url",
        type=str,
        help="Url",
    )

    args = parser.parse_args()

    response: requests.Response = requests.get(args.url)
    if response.status_code == 200:
        htmlContent = response.text
        musicSubUrlInfo = getMusicSubUrl(
            htmlContent=htmlContent,
        )
        # 如果是 None, 就默认是空字符串, 写法需要单行完成
        absoluteMusicUrl = (
            ""
            if musicSubUrlInfo.absoluteMusicUrl is None
            else musicSubUrlInfo.absoluteMusicUrl
        )
        # 输出到 alfred, 如果是 None, 就默认是空字符串
        print(
            f"{absoluteMusicUrl},{(""if musicSubUrlInfo.value1 is None else musicSubUrlInfo.value1)},{(""if musicSubUrlInfo.value2 is None else musicSubUrlInfo.value2)}",
        )

    # 读取当前目录下的 python/testMusicHtmlContent.txt 文件为字符串
    """ with open("./python/testMusicHtmlContent.txt", "r") as f:
        htmlContent = f.read()
        musicSubUrlInfo = getMusicSubUrl(
            htmlContent=htmlContent,
        )
        if musicSubUrlInfo is None:
            print("Can't get music sub url")
        else:
            print(
                f"{musicSubUrlInfo.value1},{musicSubUrlInfo.value2}",
            ) """


if __name__ == "__main__":
    main()
