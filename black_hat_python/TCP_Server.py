import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip,bind_port))
server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip,bind_port))

#클라이언트 처리 스레드
def handle_client(client_socket):
    #클라이언트가 전송한 내용을 출력
    request = client_socket.recv(1024)
    print("[*] Received : %s" % request)
    #응답 패킷 전송
    text = "My name is kpk"
    text_en = text.encode('utf-8')
    client_socket.send(text_en)
    client_socket.close()
    
while True:
    client,addr = server.accept()
    print("[*] Accepted Connection from: %s:%d" % (addr[0],addr[1]))
    #입력데이터를 처리할 클라이언트 스레드 생성
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
        

