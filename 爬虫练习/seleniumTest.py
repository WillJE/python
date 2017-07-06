# -* encoding:utf-8 -*-
from selenium import webdriver
#python + selenium + phantomjs
from time import sleep
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException


def open_url(url, keys):
    driver = webdriver.Chrome()
    #进入网站
    driver.get(url)
    print('进入...' + driver.title)
    #找到搜索框
    elem = driver.find_element_by_id('kwdselectid')
    #清楚搜索框之前内容
    elem.clear()
    #设置搜索内容
    elem.send_keys(keys)
    #设置城市
    elem.find_element_by_xpath('//*[@id="work_position_input"]').click()
    elem.find_element_by_xpath('//*[@id="work_position_click_multiple_selected_each_020000"]').click()
    #找到确定键
    elem.find_element_by_xpath('//*[@id="work_position_click_bottom_save"]').click()
    #找到搜索键
    elem.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/button').click()

    #获取所有窗口
    # for handle in driver.window_handles:
    #     driver.switch_to(handle)
    return driver

#匹配数据
def search_job(driver):
    data = driver.page_source
    content = BeautifulSoup(data, 'lxml')
    #两种写法一样
    position = content.find_all('p', class_='t1')
    company = content.find_all('span', {"class": "t2"})
    workplace =content.find_all('span', class_='t3')
    slary = content.find_all('span', class_='t4')
    publis_time = content.find_all('span', class_='t5')

    i = 1
    for each in position:
        try:
            print('#################'+str(i) +'个job#################')
            print('职位名 '+each.a.get('title'))
            print('职位链接 ' +each.a.get('href'))
            print('公司名 '+company[i-1].string)
            print('工作地点 '+workplace[i-1].string)
            print('薪资 '+slary[i-1].string)
            print('发布时间 '+publis_time[i-1].string)
            print('\n') #换行
            i += 1
        except Exception as e:
            continue
    return driver

#翻页
def next_page(driver):
    try:
        page_num = driver.find_element_by_link_text('下一页')
        page_num.click()
    except NoSuchElementException:
        print('搜索完毕')
        flag = 0
        return flag


if __name__ == '__main__':
    url = 'http://www.51job.com/?from=baidupz'
    keys = input('请输入关键字:')
    num = 1
    driver = open_url(url, keys)
    while True:
        print('##########' + u'第{}页信息'.format(num) + '##########')
        driver = search_job(driver)
        flag = next_page(driver)
        num += 1
        if flag == 0:
            break
    driver.close()