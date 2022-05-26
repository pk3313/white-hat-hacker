import socket
from urllib import response

target_host = "127.0.0.1"
target_port = 9999 
#소켓 객체 생성
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#클라이언트 연결
client.connect((target_host,target_port))
#데이터 전송
text = "My name is Bae"
text_en = text.encode('utf-8')
client.send(text_en)
#데이터 수신
response= client.recv(4096)

print(response)
