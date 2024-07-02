# 파이썬으로 익명 FTP 스캐너 만들기
import ftplib

def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        ftp.login('anonymous', 'me@your.com')
        print('\n[*] ' + str(hostname) + ' FTP Anonymous Logon Succeeded.')
        ftp.quit()
        return True
    
    except Exception as e:
        print('\n[-] ' + str(hostname) + ' FTP Anonymous Logon Failed.')
        return False

host = '127.0.0.1'
anonLogin(host)    
        
        
    
    