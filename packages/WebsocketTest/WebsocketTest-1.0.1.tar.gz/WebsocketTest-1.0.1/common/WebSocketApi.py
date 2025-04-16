import _thread as thread
import logging
import websocket  # 使用websocket_client
from common.utils import *

class WebSocketApi:
    def __init__(self, url, request):
        self.url = url
        self.request = request
        self.answer_text = ""
        self.errcode = ""
        self.response = {}
        self.ws = None
        
    def on_error(self, ws, error):
        """处理WebSocket错误"""
        logging.error(f"### error: {error}")
        self.errcode = str(error)
        self.ws.close()

    def on_close(self, ws, close_status_code, close_msg):
        """处理WebSocket关闭"""
        logging.info(f"### ws closed with status {close_status_code} and message {close_msg}")

    def on_open(self, ws):
        """处理WebSocket连接建立"""
        thread.start_new_thread(self.run, (ws,))

    def run(self, ws, *args):
        """发送请求"""
        ws.send(self.request)

    def on_message(self, ws, message: str):
        """处理WebSocket消息"""
        try:
            msg = json.loads(message)
            code = safe_get(msg, ["header","code"])
            if code != 0:
                logging.error(f'请求错误: {code}, {msg}')
                err_msg = safe_get(msg, ["header","message"])
                self.errcode = f"{code}, error msg: {err_msg}"
                self.ws.close()
            else:
                answer = safe_get(msg, ["payload","results","text","intent","answer"])
                answerText = safe_get(answer, ["text"])
                if answerText:
                    self.answer_text += answerText
                if msg['header']['status']=="2" or msg['header']['status']=="3":  # 返回结果接收完成
                    if self.answer_text:
                        answer["text"] = self.answer_text     
                    self.response = msg
                    self.ws.close()
        except json.JSONDecodeError as e:
            logging.error(f"JSON解码错误: {e}")
            self.errcode = f"JSON解码错误: {e}"
            self.ws.close()

    def start(self):
        """启动WebSocket客户端"""
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(self.url,
                                        on_open=self.on_open,
                                        on_error=self.on_error,
                                        on_message=self.on_message,
                                        on_close=self.on_close)
        self.ws.run_forever()


def main(Spark_url, request: str):
    """主函数，启动WebSocket客户端并返回响应"""
    client = WebSocketApi(Spark_url, request)
    client.start()
    return client.response