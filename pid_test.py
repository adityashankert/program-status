import os
import platform
import ctypes
import mysql.connector 
from mailer import Mailer
from mailer import Message

# GetExitCodeProcess uses a special exit code to indicate that the process is
# still running.
_STILL_ACTIVE = 259
 
def is_pid_running(pid):
    return (_is_pid_running_on_windows(pid) if platform.system() == "Windows"
        else _is_pid_running_on_unix(pid))
 
def _is_pid_running_on_unix(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True
 
def _is_pid_running_on_windows(pid):
    import ctypes.wintypes
 
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.OpenProcess(1, 0, pid)
    if handle == 0:
        return False
 
    # If the process exited recently, a pid may still exist for the handle.
    # So, check if we can get the exit code.
    exit_code = ctypes.wintypes.DWORD()
    is_running = (
        kernel32.GetExitCodeProcess(handle, ctypes.byref(exit_code)) == 0)
    kernel32.CloseHandle(handle)
 
    # See if we couldn't get the exit code or the exit code indicates that the
    # process is still running.
    return is_running or exit_code.value == _STILL_ACTIVE
 

cnx = mysql.connector.connect(user='root', password='',host='127.0.0.1',database='test')
							  
cursor = cnx.cursor()
query = ("SELECT queue_name,pid FROM queue_pid")
cursor.execute(query)
for (queue_name, pid) in cursor:
	if is_pid_running(pid)==False:
	
		message = Message(From="status@schoolcom.in",To="aditya@schoolcom.in,t.a.shanker@gmail.com",charset="utf-8")
		message.Subject = "SMS queue is not running !!!"
		message.Body = """Hi,\nSMS """+queue_name+""" is not running please look into it.\nRegards,\nStatus Team."""
		sender = Mailer('smtp.gmail.com',587,True,'status@schoolcom.in','schoolcom')
		sender.send(message)
	else:
		print "sdkfaj"

cursor.close()

cnx.close()
