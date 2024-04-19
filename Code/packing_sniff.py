import socket
import os

# 리스닝할 호스트 
host = "127.0.0.1"

# 로 소켓 생성 후 퍼블릿 인터페이스에 바인딩
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP
    
sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 0))    

# 캡처에 IP 헤더 포함
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# 윈도우이면 IOCTL을 전송해 무차별 모드 설정
if os.name=="nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
# 단일 패킷 읽기 
print(sniffer.recvfrom(65565))

# 윈도우이면 무차별 모드 해제
if os.name=="nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    
        