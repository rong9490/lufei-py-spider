# web应用程序: 遵循http协议
# 网络概念: socket
import socket

# 实例对象
sock = socket.socket()

sock.bind(("127.0.0.1", 8080))
sock.listen(5)
while 1:
    # 全双工的管道
    conn, addr = sock.accept()  # 阻塞等待客户端连接

    # 取1k的数据
    data = conn.recv(1024)
    # 遵循http流程
    print("客户端发送的信息:\n", data)
    conn.send(b"HTTP/1.1 200 ok\r\nserver:yuan\r\ncontent-type:text/html\r\n\r\n<h1>Hello World</h1>")

    # 记得关闭管道
    conn.close()


# 会响应无效: 解析不了数据, 不符合http
# b 字节串
# postman urlencoded
# content-type: text/html
# 前后端分离/不分离: 职责
# 