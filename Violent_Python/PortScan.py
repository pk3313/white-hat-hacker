import optparse
import socket
from socket import *
from threading import *

# Semaphore - 함수가 화면에 대한 완전한 통제권을 가지도록 해줌 
# 다른 스레드가 진행되지 못하도록 Lock를 걸 수 있음
screenLock = Semaphore(value=1)
  

# 각 포트에 연결을 시도하는 함수 
def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)
        connSkt.connect((tgtHost, tgtPort))
        connSkt.send('ViolentPython\r\n')
        results = connSkt.recv(100)
        
        # screenLock.acquire() = 하나의 스레드만 화면에 출력하기 위함
        screenLock.acquire()
        print('[+]%d/tcp open'% tgtPort)
        print('[+]' + str(results))
        connSkt.close()
    except:
        screenLock.acquire()
        print('[-]%d/tcp close'% tgtPort)
    finally:
        screenLock.release()
        connSkt.close()

# 입력받은 Host, Port를 가져오는 함수 
def portScan(tgtHost, tgtPorts):
    try:
        tgtIp = gethostbyname(tgtHost)
    except:
        print("[-] cannot resolve '%s' : Unknown host" %tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIp)
        print('\n[+] Scan Results for: ' + tgtName[0])
    except:
        print('\n[+] Scan results for:' + tgtIp)
    
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost,int(tgtPort)))
        t.start()

# optparse - 커맨드에 옵션을 추가하는 함수          
def main():           
    parser = optparse.OptionParser('Usage %prog -H' + \
        '<target host> -p <targetport')

    parser.add_option('-H', dest='tgtHost', type='string',\
        help= 'specify target host')

    parser.add_option('-p', dest='tgtPort', type='int', \
        help='specify target port')

    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if (tgtHost == None) | (tgtPorts[0] == None):
        print('[-] You must specify a target host and port[s].')
        exit(0)
        
    portScan(tgtHost, tgtPorts)                      
if __name__ == '__main__':
    main()    