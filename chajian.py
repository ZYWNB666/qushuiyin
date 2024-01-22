# encoding:utf-8

import json
import re

import requests

import plugins
from bridge.context import ContextType
from bridge.reply import Reply, ReplyType
from plugins import *


@plugins.register(
    name="qushuiyin",
    desire_priority=100,
    hidden=True,
    desc="取水印插件",
    version="0.1",
    author="lanvent",
)
class qushuiyin(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.on_handle_context
        logger.info("[chajian] inited")
        self.config = super().load_config()

    def on_handle_context(self, e_context: EventContext):
        if e_context["context"].type != ContextType.TEXT:
            return
        content = e_context["context"].content.strip()
        if content.startswith("去水印"):
            url_pattern = r'https?://\S+'
            urls = re.findall(url_pattern, content)
            print(urls)
            if urls:
                for payload in urls:
                    print(payload)
                dsp_url = 'http://api.xtaoa.com/api/video_v1.php?&url=' + payload
                headers = {
                    'Content-Type': "application/x-www-form-urlencoded"
                }
                response = requests.request("GET", dsp_url, data=payload, headers=headers)
                if response.status_code != 200:
                    text = (f"请求失败，状态码：{response.status_code}!")
                    print(text)
                    reply = Reply(ReplyType.ERROR, text)
                    return reply
                response_json = json.loads(response.text)
                video_url = response_json['video']
                reply = Reply(ReplyType.VIDEO_URL, video_url)
            else:
                reply = Reply(ReplyType.ERROR, "请发送短视频分享的内容")

            e_context["reply"] = reply
            e_context.action = EventAction.BREAK_PASS  # 事件结束，并跳过处理context的默认逻辑
            # return

    def get_help_text(self, **kwargs):
        help_text = "输入 去水印+抖音链接，即可获取无水印视频\n比如：\n@ChatGPT 去水印 6.66 复制打开抖音，看看【子杭的作品】《晕倒是你的谎言》# 迷惑行为大赏 # 意想不到的... https://v.douyin.com/iLDK86rp/ Pkp:/ 12/24 W@Z.Zm "
        return help_text
