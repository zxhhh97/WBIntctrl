__author__ = "zxh"
from airtest.core.api import *
from airtest.core.android import Android
from airtest.core.android.minitouch import *
import datetime,time,logging
from functools import wraps
from poco.drivers.android.uiautomation import AndroidUiautomationPoco 

ongoing = False
ip_address = "127.0.0.1:62001" #夜神nox

def opt_lock():
    def decorator(func):
        @wraps(func)  #内置函数使新建的函数属性不变
        def wrapper(*args, **kw):
            global ongoing
            # before
            while ongoing:
                sleep(0.1)
            ongoing = True
            f = func(*args, **kw)
            ongoing = False
            return f
        return wrapper
    return decorator

def writeinto(*log_content):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    log_content = "{}---->{},{} {}".format(time_now,log_content[0],log_content[1],os.linesep)
    fp = open('history.log','a+')
    fp.write(log_content)
    fp.close()

def writelog(*text):
    def decorator(func):
        @wraps(func)  #内置函数使新建的函数属性不变
        def wrapper(*args, **kw):
            msg = '===={} {} :{}===='.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),func.__name__,'Begin')
            print(msg)
            if text:
                msg = '===={} {} :{}===='.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),func.__name__,text[0])
                print(msg)
            f = func(*args, **kw)
            msg = '===={} {} :{}===='.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),func.__name__,'end')
            print(msg)
            if not kw:
                kw =={}
            writeinto(func.__name__,kw)
            return f
        return wrapper
    return decorator

@writelog()
def setup_poco(state = 'usb', srl = None):
    global poco
    if state == 'usb':
        srl = 'KWG7N17210000966' if not srl else srl
        device = build_device(usb = srl)
    elif state == 'nox':
        srl = "127.0.0.1:62001" if not srl else srl
        device = build_device(ip = srl)
    elif state == 'direct':
        device = None
    poco = build_poco(device)
    return poco,device


def build_device(ip=None,usb='KWG7N17210000966'):
    if ip:
        print(ip)
        dev = connect_device('android:///{}?cap_method=javacap&touch_method=adb'.format(ip))
    elif usb:
        print(usb)
        dev = connect_device('android:///{}'.format(usb)) 
    return dev

def build_poco(device):
    if device:
        poco = AndroidUiautomationPoco(device,use_airtest_input=True, screenshot_each_action=False)
    else:
        poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    return poco