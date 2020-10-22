import time

class Msg(object):
    def __init__(self):
        pass

    def send(self):
        return "success"

class TextMsg(Msg):
    def __init__(self, toUserName, fromUserName, content):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{0[ToUserName]}]]></ToUserName>
                <FromUserName><![CDATA[{0[FromUserName]}]]></FromUserName>
                <CreateTime>{0[CreateTime]}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{0[Content]}]]></Content>
            </xml>
            """
        return XmlForm.format(self.__dict)

class ImageMsg(Msg):
    def __init__(self, toUserName, fromUserName, mediaId):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['MediaId'] = mediaId

    def send(self):
        XmlForm = """
            <xml>
                <ToUserName><![CDATA[{0[ToUserName]}]]></ToUserName>
                <FromUserName><![CDATA[{0[FromUserName]}]]></FromUserName>
                <CreateTime>{0[CreateTime]}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                <MediaId><![CDATA[{0[MediaId]}]]></MediaId>
                </Image>
            </xml>
            """
        return XmlForm.format(self.__dict)