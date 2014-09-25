import os
import platform
import ctypes

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
 
pid= "value"

if is_pid_running(pid)==False:
	#action for program running
else:
	#action for program not running
