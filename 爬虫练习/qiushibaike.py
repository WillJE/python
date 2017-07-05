import requests
from bs4 import BeautifulSoup

def getContent(url,headers):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    return r.text

def get_text(response):
    soup = BeautifulSoup(response, 'html.parser')
    content_list = soup.find_all('div', class_='article block untagged mb15')
    for i in range(0, len(content_list)):
        print(content_list[i].span.text)

if __name__ == '__main__':
    ArticleUrl = 'https://www.qiushibaike.com/text/%d'
    commentUrl = 'https://www.qiushibaike.com/article/%s'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'cookie': 'id=2255b7550b2800e6||t=1496478452|et=730|cs=002213fd488749467a1cb08420'
    }
    page = 0
while True:
    raw_input = input("输入enter查看下一页内容，输入exit退出:")
    if raw_input == 'exit':
        break
    else:
        page += 1
        url = ArticleUrl %page
        print("########"+"这是第" + str(page) + "页内容" +"########")
        print("########"+"地址为:" + str(url))
        articlePage = getContent(url, headers)
        soupArticle = BeautifulSoup(articlePage, 'html.parser')
        articleFloor = 1
        for string in soupArticle.find_all(attrs='article block untagged mb15'):
            commentId = str(string.get('id'))[11:].strip()
            print(articleFloor, '.', string.find(attrs='content').get_text().strip())
            articleFloor += 1
            commentPage = getContent(commentUrl %commentId, headers)
            if commentPage is None:
                continue
            soupComment = BeautifulSoup(commentPage, 'html.parser')
            commentFloor = 1
            for comment in soupComment.find_all(attrs='body'):
                print("  " + str(commentFloor) + "楼回复:" + comment.get_text())
                commentFloor += 1

