# step 1: 在终端中切换到此文件夹 <cd /Users/xiada/Downloads/python/red_book_extract>
# step 2: 打开一个浏览器对象并添加调试代码 <open -a 'Google Chrome' --args --remote-debugging-port=9222>
# step 3: 运行脚本，登录小红书

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import random
import pandas as pd
import os

def search_keyword(keyword):
    # 模拟人类搜索，将鼠标移动到搜索框
    search_input = driver.find_element(By.ID, "search-input")
    actions = ActionChains(driver)
    actions.move_to_element(search_input)
    # 模拟人类搜索，点击搜索框
    actions.click(search_input)
    time.sleep(2)
    # 模拟人类搜索，输入关键词
    actions.send_keys(keyword)
    # 模拟人类搜索，按回车搜索
    actions.send_keys(Keys.ENTER)
    actions.perform()

def scrape_articles():
    count = 0
    article_index = []
    visited_index = set()
    # 根据实际情况修改下拉次数
    while count < 3:
        driver.execute_script("window.scrollTo(0, 10000)")
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for i in soup.find_all('section', class_ = 'note-item'):
            next_a_tag = i.find_next('a', style = 'display: none;')
            if next_a_tag is not None:
                index = next_a_tag.get('href')
                if index not in visited_index:
                    visited_index.add(index)
                    article_index.append(index)
        count += 1
        time.sleep(random.uniform(1, 3))
    return article_index

def scrape_each_article(article_index):
    contents = []
    likes = []
    collects = []
    titles = []
    tags = []
    for index in article_index:
        url = f"https://www.xiaohongshu.com{index}"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find('div', id = 'detail-title')
        if title_tag is not None:
            titles.append(title_tag.text)
        else:
            titles.append("")
        content_tag = soup.find('div', class_ = 'desc')
        # 除了标签为None的情况，还存在标签值为空的情况，需一同处理
        if content_tag is not None and content_tag.text.strip() != "":
            desc_tag = content_tag.find_next('span')
            contents.append(desc_tag.text)
            all_tags = content_tag.find_all_next('a', id = 'hash-tag')
            if all_tags is not None and len(all_tags) > 0:
                tag_string =','.join(map(str, [i.string for i in all_tags if i.string is not None]))
                tags.append(tag_string)
            else:
                tags.append("")
        else:
            contents.append("")
            tags.append("")
        engagements = soup.find('div', class_ = 'buttons engage-bar-style')
        if engagements:
            like_icon = engagements.find('svg', class_ = 'reds-icon like-icon')
            if like_icon:
                like_num = like_icon.find_next('span').text
                likes.append(like_num)
            else:
                likes.append("0")
            collect_icon = engagements.find('svg', class_ = 'reds-icon collect-icon')
            if collect_icon:
                collect_num = collect_icon.find_next('span').text
                collects.append(collect_num)
            else:
                collects.append("0")
        else:
            likes.append("0")
            collects.append("0")
        time.sleep(random.uniform(1, 3))
    data = {"笔记标题": titles,
            "点赞数": likes,
            "收藏数": collects,
            "笔记内容": contents,
            "笔记标签": tags}
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # 设置远程调试地址
    remote_debugging_address = 'localhost:9222'

    # 创建Chrome选项
    chrome_options = Options()
    chrome_options.add_experimental_option('debuggerAddress', remote_debugging_address)

    # 连接到已经启动的Chrome实例
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.xiaohongshu.com')

    # 输入笔记关键词
    keyword = input("请输入关键词：")
    search_keyword(keyword)
    print("笔记正在搜索中……")
    article_index = scrape_articles()
    print("笔记已储存完成，正在提取笔记信息……")
    df = scrape_each_article(article_index)
    article_link = ["https://www.xiaohongshu.com"+i for i in article_index]
    df.insert(0, "笔记链接", article_link)
    if os.path.isfile(f"小红书_{keyword}_笔记内容.csv"):
        os.remove(f"小红书_{keyword}_笔记内容.csv")
    df.to_csv(f"小红书_{keyword}_笔记内容.csv", mode='w', index=False)
    print("笔记信息已提取完成")
