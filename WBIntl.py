# -*- encoding=utf8 -*-
__author__ = "zxh"
import argparse
from airtest.core.api import *
from airtest.core.android import Android
from airtest.core.android.minitouch import *
import time
from poco.drivers.android.uiautomation import AndroidUiautomationPoco 
from setting import writelog,setup_poco

poco, _ =setup_poco(state = 'usb')
WBInt = "com.weico.international:id/"
#back = [86,154] #resolution
top_sp =[0.5, 0.14] #percent
UN = {}
UN['Toolbar']       = WBInt + "toolbar"
UN['SendOK']        = WBInt + "send_ok"
UN['TL_sp']         = WBInt + "item_timeline_sp"
UN['TL_user']       = WBInt + "item_timeline_user"
UN['TL_tool_']      = WBInt + "item_timeline_toolbar_"
UN['TL_tool_num']   = WBInt + "item_timeline_toolbar_num"
UN['TL_status']     = WBInt + "item_timeline_status"
UN['TL_time']       = WBInt + "item_timeline_time"
UN['scr2top']       = WBInt+"act_article_scroll2top"

def back_home():
    while not poco(WBInt+"frg_index_group_title").exists():
        #click(back)
        try:
            poco(name = '转到上一层级').click()
        except:
            poco(WBInt+"tab_icons_home_layout").click()

@writelog()
def main_intWB():
    home() 
    poco(text = "微博国际版").click()
    back_home()
    poco(WBInt+"tab_icons_home_layout").click()
    refresh_my_timeline()
    time.sleep(1)
    
@writelog()
def get_current_user(back=True):
    back_home()
    if poco("确定").exists():
        poco("确定").click()
    username = poco(WBInt+"drawer_header_username").get_text()
    #poco.swipe([0.5,0.5],direction = [-0.5,0],duration = 0.5)
    if back:
        poco.click([0.8,0.5])
    return username

@writelog()
def switch2user(name):
    CurName = get_current_user(back = False)
    if not CurName == name:
        poco(WBInt + "drawer_header_arrow").click()
        if poco(WBInt + "userName", text = name).exists():
            poco(WBInt + "userName", text = name).click()
            return "success"
        else:
            return "fail"
    poco.click([0.8,0.5])
    return "success"

@writelog()        
def send_weibo(newmsg):
    back_home()
    new = poco(WBInt+"frg_index_new")
    new.wait_for_appearance()
    new.click()
    new.wait_for_appearance()
    new.click()
    blank = poco(WBInt+"act_compose_input")
    blank.wait_for_appearance()
    blank.set_text(newmsg)
    #poco(WBInt+"compose_location").click() #set location
    send_ok = poco(UN['SendOK'])
    send_ok.wait_for_appearance()
    send_ok.click()
    sleep(1)

@writelog()
def opt_wb(idx=0,*cmt,opt = '赞'):
    dic = {'赞':'1','评论':'2','转发':'3','快转':'3'}
    while not poco(UN['TL_tool_']+dic[opt]).exists():
        swipe_a_bit('up')
    if poco(UN['TL_status'])[0].get_position()[1]>poco(UN['TL_tool_']+'1')[0].get_position()[1]:
        idx = 1
    ui = poco(UN['TL_tool_']+dic[opt])[idx]
    if opt =='快转':
        ui.long_click()
        sleep(0.3)
    elif opt =='转发':
        ui.click()
        if cmt:
            text(cmt[0])
        poco(UN['SendOK']).click()
        sleep(0.3)
    elif opt =='评论':
        ui.click()
        poco(WBInt+"act_detail_bottom_comment").set_text(cmt)
        poco(WBInt+"send_option_layout").click()
        poco("转到上一层级").click()
    else:
        ui.click()
    print(opt)

def get_timeline_pop(idx = 0):
    while not poco(UN['TL_tool_']+'1').exists():
        swipe_a_bit('up')
    while poco(UN['TL_status'])[0].get_position()[1]>poco(UN['TL_tool_']+'1')[0].get_position()[1]:
        swipe_a_bit('up')
    order = ['赞','评论','转发']
    num = {}
    for i in range(3):
        t = poco(UN['TL_tool_num']+str(i+1))[idx].get_text() 
        num[order[i]] = t if t else '0'
    for k,v in num.items(): num[k]=int(float(v.strip('万'))*10000) if '万' in v else int(v)
    return num

def get_repost_pop(idx = 0):
    num = {'赞':0,'评论':0,'转发':0}
    if poco(WBInt+'item_timeline_repost_nums').exists():
        a = poco(WBInt+'item_timeline_repost_nums')[idx].get_text()
        a = [i for i in a.split(' ') if i]
        for i in range(int(len(a)/2)):
            k = a[2*i]
            v = a[2*i+1]
            num[k]=int(float(v.strip('万'))*10000) if '万' in v else int(v)
        return num
    else:
        print('This is an original post.')
        return num

@writelog()
def scroll_user_timeline(number,show=False):
    logstatus =[]
    for i in range(number):
        if show ==True:
            time.sleep(0.3)
            logstatus.append(get_cur_Timeline(idx = 0, show = show))
        next = 0
        while (not poco(UN['TL_sp']).exists()) or (len(poco(UN['TL_sp']))==1 and poco(UN['TL_sp']).get_position()[1]<0.2 ): # 
            swipe_a_bit('up')
        if (len(poco(UN['TL_sp']))>1) and poco(UN['TL_sp']).get_position()[1]<0.2:
            next = 1
        poco(UN['TL_sp'])[next].start_gesture().to(top_sp).hold(0.1).up()
        time.sleep(0.1)
        # if drag over
        while not poco(UN['TL_sp']).exists() or poco(UN['TL_sp'])[0].get_position()[1]>0.5:
            swipe_a_bit('down') 
    return logstatus
            

def if_share_show():
    if poco(WBInt+"title").exists(): # hold for too long “分享到” 
        click([550,531])

def if_ad_show():
    if poco("android.widget.LinearLayout")[0].poco(WBInt+"ad_timeline_header").exists():
        poco(WBInt+"ad_action").click()
        if poco(text="Have no interest").exists():
            poco(text="Have no interest").click()
        if poco(text="不感兴趣").exists():
            poco(text="不感兴趣").click()

@writelog()
def swipe_a_bit(direction = 'down'):
    if direction == 'down':
        swipe([540,500],[540,600],duration = 0.5)
    if direction == 'up':
        swipe([540,610],[540,500],duration = 0.5)
    time.sleep(0.1)


def get_timeline_repost(idx = 0):
    if poco(UN['TL_status'])[idx].parent().child(WBInt+"item_timeline_repost").exists():
        RepostStatus = poco(WBInt+"item_timeline_repost_status")[idx].get_text()
    else:
        RepostStatus = None
    return RepostStatus

@writelog()
def get_cur_Timeline(idx = 0,show = True,full=True):
    curName = poco(UN['TL_user'])[idx].get_text()
    curStatus = poco(UN['TL_status'])[idx].get_text()
    curTime = poco(UN['TL_time'])[idx].get_text()
    curPop = get_timeline_pop(idx=idx)
    RepostStatus = get_timeline_repost(idx = idx)
    RepostPop = get_repost_pop(idx = idx)
    if show == True:
        print('================================')
        print('##User:',curName)
        print('##Time:',curTime)
        print('##Text:\n',curStatus)
        print('##repost text:\n',RepostStatus)
        print('================================')
    TInfo = {'user':curName,'time':curTime,'status':curStatus,'population':curPop,'origin_status':RepostStatus,'origin_population':RepostPop}
    return TInfo

@writelog()
def scroll_my_timeline(number = 1, show = True): 
    #make sure #0 Seperate line exists and locates at top
    while not poco(UN['TL_sp']).exists():
        swipe_a_bit('down')
        if_share_show()
    logstatus =[]
    # Now #0 Seperate line is ready
    for i in range(number):
        if_ad_show()
        if show ==True:
            logstatus.append(get_cur_Timeline(idx = 0, show = show))
        #====if the current status is too long and exceeds one page:
        next = 0
        while (not poco(UN['TL_sp']).exists()) or (len(poco(UN['TL_sp']))==1 and poco(UN['TL_sp']).get_position()[1]<0.2 ): # 
            swipe_a_bit('up')
        if (len(poco(UN['TL_sp']))>1)and poco(UN['TL_sp']).get_position()[1]<0.2:
            next = 1
        poco(UN['TL_sp'])[next].start_gesture().to(top_sp).hold(0.1).up()
        time.sleep(0.1)
        # if drag over
        while not poco(UN['TL_sp']).exists() or poco(UN['TL_sp'])[0].get_position()[1]>0.5:
            swipe_a_bit('down')
    return logstatus
        
@writelog()  
def browse_user_timeline(username='清华大学',number=3,opt = 0, Before = True):
    back_home()
    if enter_userhome(username,blur = True):
        if poco(UN['scr2top']).exists():
            poco(UN['scr2top']).click()
        time.sleep(0.1)
        if poco(WBInt+"comments_filter_parent").exists()and poco(WBInt+"comments_filter_parent").get_position()[1]>0.4:
            poco(WBInt+"comments_filter_parent").start_gesture().to(top_sp).hold(0.1).up()
        logstatus = scroll_user_timeline(number=number-1,show = Before)
        logstatus.append(get_cur_Timeline(idx = 0,show=True))
        if opt:
            opt_wb(0,opt = opt)
    back_home()
    return logstatus


def enter_userhome(na,blur = True):
    back_home()
    poco(desc = '搜索').click()
    text(na,search = True)
    #poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
    #sleep(0.8)
    while not poco('用户').exists():
        sleep(0.1)
    poco('用户').click()
    if not poco(UN['TL_user']).exists():
        sleep(0.8)
    if not poco(UN['TL_user']).exists():
        print('cannot find user: {}'.format(na))
        return 0
    if blur or poco(UN['TL_user'])[0].get_text() == na:
        poco(UN['TL_user'])[0].click()
        return 1
    else:
        print('cannot find user: {}'.format(na))
        return 0
    
@writelog()
def follow(na, blur = True):
    if enter_userhome(na,blur = blur):
        if poco(WBInt+"profile_header_follow").get_text()=='关注':
            poco(WBInt+"profile_header_follow").click()
            poco(text = '保存').click()
            msg = 'success'
        else:
            msg = 'fail: already following'
    else:
        msg = 'fail: Cannot find the user'
    back_home()
    return msg

@writelog()
def unfollow(na, blur = True):
    if enter_userhome(na,blur = blur):
        if poco(WBInt+"profile_header_follow").get_text()=='已关注':
            poco(WBInt+"profile_header_follow").click()
            poco(text = '取消关注').click()
            poco(text = '取消关注').click()
            msg = 'success: remove following'
        else:
            msg = 'fail: not following'
    else:
        msg = 'fail: Cannot find the user'
    back_home()
    return msg

def refresh_my_timeline():
    poco(WBInt+"tab_icons_home_layout").click() #back to top
    poco("android:id/list").scroll(direction =u'vertical',percent =-0.6, duration=0.1) #refresh




if __name__ == '__main__':
    #send_weibo('测试～')
    poco,device = setup_poco()
    #refresh_my_timeline()
    #time.sleep(5*60)
    #auto_homeline()
    
  
  