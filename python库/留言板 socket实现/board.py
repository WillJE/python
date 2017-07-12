import socket
from urllib import parse
class Request(object):
    def __init__(self):
        self.path = ''
        self.query = {}
        self.method = 'GET'
        self.body = ''

    # 定义函数解析body
    def form(self):
        # url编码是ASCII码，不能用中文
        body = parse.unquote(self.body)
        print('body:',body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f



 #定义一个Request实例存储数据
request = Request()
messagelist = []

class Message(object):
    def __init__(self):
        self.message = ''
        self.author = ''

    def __repr__(self):
        return '{}:{}'.format(self.author, self.message)

def run(host='',port=3000):
    # 创建socket实例
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            # listen监听请求,3表示建立连接的握手次数
            s.listen(3)
            connection, address = s.accept()
            # 用recv接收浏览器发送的请求数据
            r = connection.recv(1024)
            # 网络上传输的数据都是bytes类型，这里将bytes转成str
            r = r.decode('utf-8')
            try:
                # 'Accept:image/webp,image/*,*/*;q=0.8'
                request.method = r.split()[0]
                request.body = r.split('\r\n\r\n')[1]
                path = r.split()[1]
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                print('error', e)
            connection.close()

def route_index():
    header = 'HTTP/1.1 220 NOT OK\r\nContent-Type:text/html\r\n'
    body = '<h1> hello world! </h1>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_shine():
    header = 'HTTP/1.1 220 NOT OK\r\nContent-Type:text/html\r\n'
    body = '<h1> hello world!<img src = "img/shine.gif"/> </h1>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_image_shine():
    with open('img/shine.gif', 'rb') as f:
        header = b'HTTP/1.1 220 NOT OK\r\nContent-Type:image/gif\r\n\r\n'
        img = header + f.read()
        return img

def route_laugh():
    header = 'HTTP/1.1 220 NOT OK\r\nContent-Type:text/html\r\n'
    body = '<h1> hello world!<img src = "img/laugh.gif"/> </h1>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_image_laugh():
    with open('img/laugh.gif', 'rb') as f:
        header = b'HTTP/1.1 220 NOT OK\r\nContent-Type:image/gif\r\n\r\n'
        img = header + f.read()
        return img

def route_all():
    header = 'HTTP/1.1 220 NOT OK\r\nContent-Type:text/html\r\n'
    body = '<h1> hello world!<img src = "img/laugh.gif"/><img src = "img/shine.gif"/></h1>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')

def route_message():
    if request.method == 'POST':
        msg = Message()
        form = request.form()
        msg.author = form.get('author', '')
        msg.message = form.get('message', '')
        # 把留言类加入留言列表里
        messagelist.append(msg)

    header = 'HTTP/1.1 210 VERY OK\r\n Content-Type:text/html\r\n'
    body = template('message.html')
    # 把所有留言取出来放在列表中
    msgs = '<br>'.join([str(m) for m in messagelist])
    body = body.replace('{{message}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def template(filename):
    with open('templates/' + filename, 'r', encoding='utf-8') as f:
        return f.read()


def error(code = 404):
    error_dict = {
        404: b'HTTP/1.1 404 NOT FOUNT\r\n<h1> 404 NOT FOUND</h1>',
    }

def response_for_path(path):
    path, query = parse_path(path)
    request.path = path
    request.query = query
    print('path and query', path, query)
    r = {
        '/': route_index,
        '/shine': route_shine,
        '/laugh': route_laugh,
        '/img/shine.gif': route_image_shine,
        '/img/laugh.gif': route_image_laugh,
        '/all': route_all,
        '/message': route_message,
    }
    response = r.get(path, error)
    return response()


def parse_path(path):
    index = path.find('?')
    if index == -1:
        return path, {}
    else:
        path, query_s = path.split('?', 1)
        args = query_s.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)