import time
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait#设置最多等多久,时间内出现就下一步,超时也下一步
# import selenium
from selenium.webdriver.common.keys import Keys
import multiprocessing#进程:主进程和子进程,start,join(阻塞)


# 获得app窗口长和宽
def get_windows(driver):
  x = driver.get_window_size()['width']
  y = driver.get_window_size()['height']
  return (x,y)

# 输入id
def handle_douyin(driver):
    try:
      if WebDriverWait(driver,3).until(lambda x:x.find_element_by_id('com.ss.android.ugc.aweme:id/aia')):
        driver.find_element_by_id('com.ss.android.ugc.aweme:id/aia').send_keys('191433445',Keys.ENTER)
    except:
      pass
    # 体验抖音浅色模式
    try:
      if WebDriverWait(driver,2).until(lambda x:x.find_element_by_id('com.ss.android.ugc.aweme:id/tv_ok')):
        driver.find_element_by_id('com.ss.android.ugc.aweme:id/tv_ok').click()
    except:
      pass

    try:
      if WebDriverWait(driver,3).until(lambda x:x.find_element_by_class_name('android.widget.ImageView')):
        driver.find_element_by_class_name('android.widget.ImageView').click()
    except:
      pass

    # 点粉丝
    try:
      if WebDriverWait(driver,4).until(lambda x:x.find_element_by_id('com.ss.android.ugc.aweme:id/cud')):
        driver.find_element_by_id('com.ss.android.ugc.aweme:id/cud').click()
    except:
      pass

    while True:
      if '暂时没有更多了' in driver.page_source:
          break
      elif 'TA还没有粉丝' in driver.page_source:
          break
      else:
          l = get_windows(driver)
          x1 = int(l[0] * 0.5)
          y1 = int(l[1] * 0.9)
          y2 = int(l[1] * 0.15)
          driver.swipe(x1, y1, x1, y2)
          time.sleep(0.5)

# 运用appium启动运行多个模拟器的app
def handle_appiun(device,port):
    cap = {
        "platformName": "Android",
        "platformVersion": "5.1.1",
        "deviceName": device,
        "udid": device,
        # 打开夜神模拟器的app后,cmd下输入adb shell后再输入dumpsys activity | grep mFocusedActivity即可获得app的appPackage和appActivity
        "appPackage": "com.ss.android.ugc.aweme",
        "appActivity": "com.ss.android.ugc.aweme.splash.SplashActivity",
        "noREset": True,
        "unicodekeyboard": True,
        "resetkeyboard": True,
        # "automationName": "UiAutomator1"
    }
    driver = webdriver.Remote('http://localhost:'+str(port)+'/wd/hub', cap)
    # 个人信息保护
    try:
      if WebDriverWait(driver,8).until(lambda x:x.find_element_by_id('com.ss.android.ugc.aweme:id/bco')):
        driver.find_element_by_id('com.ss.android.ugc.aweme:id/bco').click()
    except:
      pass
    time.sleep(2)
    l = get_windows(driver)
    x1 = int(l[0] * 0.5)
    y1 = int(l[1] * 0.9)
    y2 = int(l[1] * 0.15)
    driver.swipe(x1, y1, x1, y2)
    time.sleep(0.5)
    # 青少年模式
    try:
      if WebDriverWait(driver,5).until(lambda x:x.find_element_by_id('com.ss.android.ugc.aweme:id/eeh')):
        driver.find_element_by_id('com.ss.android.ugc.aweme:id/eeh').click()
    except:
      pass
    # 首页点搜索
    try:
      if WebDriverWait(driver,3).until(lambda x:x.find_element_by_id('com.ss.android.ugc.aweme:id/dy3')):
        driver.find_element_by_id('com.ss.android.ugc.aweme:id/dy3').click()
    except:
      pass
    # 调用handle_douyin(driver)
    handle_douyin(driver)

if __name__ == '__main__':
    m_list = []#创建一个进程队列
    divice_list = ['127.0.0.1:62028','127.0.0.1:62029']#创建一个机器队列
    for divice in range(len(divice_list)):
        port = 4723 + 2*divice
        m_list.append(multiprocessing.Process(target=handle_appiun,args=(divice_list[divice],port,)))#将app进程放入队列
    for m1 in m_list:
        m1.start()#子进程运行
    for m2 in m_list:
        m2.join()#主进程等待阻塞













