# step 1: 在终端中切换到此文件夹 <cd /Users/xiada/Downloads/python/red_book_extract>
# step 2: 打开一个浏览器对象并添加调试代码 <open -a 'Google Chrome' --args --remote-debugging-port=9222>
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# 设置远程调试地址
remote_debugging_address = 'localhost:9222'

# 创建Chrome选项
chrome_options = Options()
chrome_options.add_experimental_option('debuggerAddress', remote_debugging_address)

# 连接到已经启动的Chrome实例
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.xiaohongshu.com')
