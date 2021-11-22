import random

# 调入相应的库
from selenium import webdriver
from time import sleep

# 从第几个视频开始刷
begin_video = 16

# 警告框处理
# 提交的答案出错跳出警告框的处理
def alert_handle(browser):
    try:
        browser.switch_to.alert().accept()
    except:
        pass

# 回答问题
# 如果跳出答题框，一般是只有两个选项的选择题
# 曾经尝试过一个一个点击提交，但是失败了
# 现在改成了随机答案，然后点击
def answer_question(browser):
    try:
        ans_opts = browser.find_elements_by_name('ans-videoquiz-opt')
        print(len(ans_opts))
        index = random.randint(0, len(ans_opts) - 1)
        print(index)
        ans_opts[index].click()
        browser.find_element_by_class_name('ans-videoquiz-submit').click()
        # 如果回答错误，解决警告框
        alert_handle(browser)
    except:
        pass

# 判断视频是否播放完毕
# 原理：看已播放的时长和总时长是否相等
# 每隔五秒调用一次该函数
def is_finished(browser):
    sleep(5)
    try:
        answer_question(browser)
        current_time = browser.find_element_by_class_name('vjs-current-time-display').get_attribute('textContent')
        end_time = browser.find_element_by_class_name('vjs-duration-display').get_attribute('textContent')
        return current_time == end_time
    except:
        pass

# 播放视频
def play_videos(browser):
    # 切换frame
    browser.switch_to.frame('iframe')
    Iframes = browser.find_elements_by_class_name('ans-attach-online.ans-insertvideo-online')
    iframesNum = len(Iframes)
    for i in range(iframesNum):
        browser.switch_to.frame(Iframes[i])

        # 点击开始播放
        button = browser.find_element_by_xpath('//*[@id="video"]/button')
        button.click()

        # 开始二倍速，一次提升0.5倍，点击三次（很笨的办法）
        two_speed = browser.find_element_by_xpath('//*[@id="video"]/div[5]/div[1]/button')
        two_speed.click()
        two_speed.click()
        two_speed.click()

        # 静音
        no_sound = browser.find_element_by_xpath('//*[@id="video"]/div[5]/div[6]/button').click()

        # 等待视频播放完毕
        while not is_finished(browser):
            sleep(5)
        # ##############
        browser.switch_to.default_content()
        browser.switch_to.frame('iframe')
    browser.switch_to.default_content()

# 课程的切换和播放
def class_switch_and_play_videos(browser):
    # 定位所有视频
    elements = browser.find_elements_by_class_name('clearfix')

    # 获取视频数量
    videos_num = len(elements)
    for i in range(begin_video, videos_num):
        # 寻找该网页内的视频
        elements = browser.find_elements_by_class_name('clearfix')
        # 点击开始播放
        elements[i].click()
        sleep(2)
        # 该函数定义见上面
        play_videos(browser)
        # 播放完毕回到主课程
        but = browser.find_element_by_link_text('回到课程')
        but.click()
        sleep(2)

# 登陆
def log_in(browser):
    # 定位元素（手机号输入框，密码输入框，登陆按钮）
    phone = browser.find_element_by_id('phone')
    password = browser.find_element_by_id('pwd')
    log_in = browser.find_element_by_id('loginBtn')

    #输入手机号和密码
    phone.send_keys('手机号')
    password.send_keys('密码')
    #点击登录
    log_in.click()

    sleep(1)

# 进入我的空间
def enter_chaoxing(browser):
    sleep(1)
    # 点击登录按钮
    browser.find_element_by_link_text('登录').click()

    log_in(browser)

    # 点击课程按钮
    sleep(1)
    browser.find_element_by_name('课程').click()

    sleep(1)
    # 进入内层结构，点击相应课程名称
    browser.switch_to.frame('frame_content')
    browser.find_element_by_link_text('课程名称').click()
    browser.switch_to.default_content()

    # 点击过后转到最外层的frame
    sleep(1)
    all_windows = browser.window_handles
    browser.switch_to.window(all_windows[1])


# 以下为浏览器配置，填写chromedriver的路径
browser = webdriver.Chrome(executable_path = r"D:（路径）\chromedriver.exe")

# 超星网站
browser.get('https://www.chaoxing.com/')

# 窗口最大化
browser.maximize_window()

# 进入超星
enter_chaoxing(browser)

# 开始播放视频
class_switch_and_play_videos(browser)








