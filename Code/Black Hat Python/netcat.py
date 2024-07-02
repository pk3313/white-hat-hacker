# 넷켓 대체하기

import sys
import socket
import getopt
import threading
import subprocess

#전역변수 정의 
listen = False
command = False
upload = False
execute = " "
target = " "
upload_destination = " "
port = 0

def usage():
    print("BHP Net Tool")
    print
    print("Usage: bhpnet.py -t target_host -p port")
    print("-l --listen - listen on [host] : [port] for incoming connections")
    print("-e --execute = file_to_run - execute the given file upon receiving a connection")
    print("-c --command - initialize a command shell")
    print("-u --upload=destination - upon receiving connection upload a file and write to [destination]")
    print
    print
    print("Example: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\'cat /etc/passwd\'")
    print("echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135")
    sys.exit(0)
    
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
    
    #커멘드라인 옵션 처리
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu",["help","listen","execute","target","port","command","upload"])
    
    except getopt.GetoptError as err:
        print(str(err))
        usage()
    
    for o, a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-u","--upload"):
            upload_destination = a
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False, "Unhandled Option"
            
    # 리스닝과 stdin으로부터 데이터 전송 중 무엇을 수행할 것인가?
    if not listen and len(target) and port > 0:
        
        #커맨드 라인에서 버퍼 읽기 
        #이는 블록되므로 입력을 stdin으로 전송하지 않는 경우에는 ctrl -D를 전송해야함
        buffer = sys.stdin.read()
        
        #데이터 전송
        client_sender(buffer)
        
        # 리스닝 수행. 커맨드라인 옵션에 따라 
        # 파일업로드, 명령실행, 셸 실행 등을 수행할 수 있음
        if listen:
            server_loop()
main()

def client_sender(buffer):
    client= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 타깃 호스트에 연결
        client.connect((target,port))
        
        if len(buffer):
            client.send(buffer)
        while True:
            # 데이터 대기
            recv_len = 1
            response = " "
            
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response+= data
                
                if recv_len < 4096:
                    break
            print(response)
            
            # 추가 입력 대기 
            buffer = raw_input("")
            buffer += "\n"
            #전송
            client.send(buffer)
    except:
        print("[*] Exception ! Exiting.")
        
        # 연결 종료 
        client.close()            
                    
                                                                   
    