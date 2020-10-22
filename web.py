from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import urllib.parse
import hashlib
import recive
import reply
import xml.etree.ElementTree
import requests
import threading
from basic import Basic
from media import Media
import database_operations as DB

def send_Message(accessToken, openId, content):#主动客服消息(text)
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % (accessToken)
    msg = {
    "touser":"%s" % openId,
    "msgtype":"text",
    "text":
    {
         "content":"{}".format(content)
    }
    }#微信官方API指定的消息格式
    requests.post(url, json=msg)
    DB.update_msg_times(openId)#主动向用户发送消息数量加1

def send_Image(accessToken, openId, image_path):#主动客服消息(images)
    ''' 上传临时素材后发送图片'''
    mediaId = myMedia.upload(accessToken, image_path, "image")["media_id"]
    url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % (accessToken)
    msg = {
    "touser":"%s" % openId,
    "msgtype":"image",
    "image":
    {
      "media_id":"%s" % mediaId
    }
    }#微信官方API指定的图片消息格式
    requests.post(url, json=msg)
    DB.update_msg_times(openId)#主动向用户发送消息数量加1

def clients_msg_handle(openId, content):#用户消息被动回复处理
    if DB.check_openId_exits(openId):
            DB.update_content(content, openId)
            DB.update_time(openId)
            return "您已输入: %s " % content
    else:
        if content.lower() == "id":
            return """ID: %s""" % DB.create_correspond_id(openId)
        else:
            return """输入"ID"获取ID"""

class Request(BaseHTTPRequestHandler):
    def do_GET(self):#解析微信服务器的url参数，若验证成功返回url参数里面的echostr，否则返回空字符
        try:
            query = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query))
            signature = query["signature"]
            timestamp = query["timestamp"]
            nonce = query["nonce"]
            echostr = query["echostr"]
            token = "" #这里填写你自己设置的token
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            sha1.update("".join(list).encode('utf-8'))
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(echostr.encode())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write("".encode())
        except Exception:
            pass

    def do_POST(self):#解析用户给微信公众号发送的消息
        datas = self.rfile.read(int(self.headers['content-length'])).decode()  # 解析发来的数据
        try:
            recMsg = recive.parse_xml(datas)
            if isinstance(recMsg, recive.Msg):  # 被动回复消息接口
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if DB.check_openId_exits(toUser):
                    DB.reset_msg_times(toUser)
                if recMsg.MsgType == 'text':
                    content = recMsg.Content.decode()
                    replyContent = clients_msg_handle(toUser, content)
                    replyMsg = reply.TextMsg(toUser, fromUser, replyContent)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/xml')
                    self.end_headers()
                    self.wfile.write(replyMsg.send().encode())
                elif recMsg.MsgType == "image":
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/xml')
                    self.end_headers()
                    self.wfile.write(replyMsg.send().encode())
                elif recMsg.MsgType == "event" and recMsg.Event == "subscribe":
                    content = '自定义内容'
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/xml')
                    self.end_headers()
                    self.wfile.write(replyMsg.send().encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/xml')
                    self.end_headers()
                    self.wfile.write(reply.Msg().send().encode())
            else:
                print("暂不处理")
                self.send_response(200)
                self.send_header('Content-type', 'application/x-www-form-urlencoded')
                self.end_headers()
                self.wfile.write("success".encode())
        except xml.etree.ElementTree.ParseError:#非微信公众号post请求处理
            pass

if __name__ == "__main__":
    DB.create_sql()
    myMedia = Media()
    basic = Basic()
    threading.Thread(target=basic.run).start()#多开一个线程计时access_token, 每隔一小时重新申请一次access_token, 使用basic.get_access_token()即可获取当前token
    host = ("0.0.0.0", 80)
    server = ThreadingHTTPServer(host, Request)#简单的http框架
    server.serve_forever()
