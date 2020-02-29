__author__ = "zxh"
from flask import Flask,request
import json
from urllib import parse
import sys
import WBIntl as wb
from setting import setup_poco,writelog,opt_lock
app = Flask(__name__)

def to_jsonstr(json_data):
        json_obj = {}
        json_obj['data'] = json_data
        json_obj['code'] = 0
        json_obj['msg'] = 'ok'
        json_str = json.dumps(json_obj, ensure_ascii=False)
        return json_str

@app.route('/follow', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def follow():
    setup_poco()
    name = request.args.get('name')
    blur = int(request.args.get('blur'))
    print('To Follow: '+name+' blur: '+str(blur))
    msg = wb.follow(name,blur=blur)
    return to_jsonstr(msg)

@app.route('/switch2user', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def switch2user():
    setup_poco()
    name = request.args.get('name')
    msg = wb.switch2user(name)
    return to_jsonstr(msg)

@app.route('/who_am_i', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def get_my_name():
    setup_poco()
    name = wb.get_current_user()
    return to_jsonstr(name)

@app.route('/unfollow', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def unfollow():
    setup_poco()
    name = request.args.get('name')
    blur = int(request.args.get('blur'))
    msg = wb.unfollow(name,blur=blur)
    return to_jsonstr(msg)

@app.route('/browse', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def browse():  
    '''获取用户前n条微博信息'''
    setup_poco()
    name = request.args.get('name')
    number = int(request.args.get('num'))
    logstatus = wb.browse_user_timeline(number=number,opt = 0,username=name, Before = True)
    return to_jsonstr(logstatus)

@app.route('/wbintl', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def weibo_intl(): 
    setup_poco() 
    wb.main_intWB()
    logstatus = 'back to mainpage'
    return to_jsonstr(logstatus)

@app.route('/myhome', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def get_homeTL(): 
    '''获取用户前n条微博信息'''
    setup_poco() 
    #name = request.args.get('name')
    number = int(request.args.get('num'))
    wb.back_home()
    wb.refresh_my_timeline()
    logstatus = wb.scroll_my_timeline(number=number,show=True)
    return to_jsonstr(logstatus)

@app.route('/send', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def send():
    setup_poco()
    wb.back_home()
    content = request.args.get('content')
    print('')
    content = content.replace("#","%23")
    #content = parse.parse_qs(content
    #content = parse.unquote(content, encoding='utf-8', errors='replace').replace('#','%23')
    if not content:
        print('no content')
        state = 'Nothing Sent'
    else:
        wb.send_weibo(content)
        print(content)
        state = 'Sent: '+content
    return to_jsonstr(state)

@app.route('/like', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def like():
    setup_poco()
    name = request.args.get('name')
    number = int(request.args.get('num'))
    logstatus = wb.browse_user_timeline(number=number,opt = '赞', username=name, Before = False)
    content = logstatus[-1]['user']+':'+logstatus[-1]['status']
    state = 'like: '+ content
    return to_jsonstr(state)

@app.route('/quickrepost', methods=['POST', 'GET'])
@opt_lock()
@writelog()  
def quickrepost():
    setup_poco()
    name = request.args.get('name')
    number = int(request.args.get('num'))
    logstatus = wb.browse_user_timeline(number=number,opt = '快转', username=name, Before = False)
    content = logstatus[-1]['user']+':'+logstatus[-1]['status']
    state = 'repost: '+ content
    return to_jsonstr(state)

@app.route('/simulation')
@writelog()
def simulation():
    sys.path.append("../")
    import simulate.simulation as sm
    jsontree = sm.run()
    return jsontree #to_jsonstr(jsontree)


@app.route('/')
@writelog()
def index():
    return 'Hello KEGer, I am a bot.'


if __name__ == '__main__':
    app.debug = True 
    poco,_ = setup_poco()
    #app.run(host='0.0.0.0',  debug=True)
    app.run(
      host='0.0.0.0',
      port= 5700,
      debug=True
    )