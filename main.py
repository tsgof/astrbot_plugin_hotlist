from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import *
from astrbot.api import logger
from .searchbhot import searchbhot
from .searchbaidu import get_baidu_hotsearch
@register("hotlist", "Tsgof", "获取B站热门榜单", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    
    @filter.command("bhot")
    async def b_hot(self, event: AstrMessageEvent):
        '''发送B站热门视频榜单''' 

        message_chain = event.get_messages() 
        logger.info(message_chain)

        results = searchbhot()
        # At 消息发送者
        
        for i, item in enumerate(results, 1):
            chain = [] 
            str1 = f'【{i}】标题：{item["标题"]}\t'
            str2 = f'作者：{item["作者"]}\t播放量：{item["播放量"]}\t链接：{item["链接"]}\n'
            chain.extend([
                Plain(str1),
                Image.fromURL(item["封面"]),
                Plain(str2)
            ])
            yield event.chain_result(chain)
    
    @filter.command("baiduhot")
    async def baidu_hot(self, event: AstrMessageEvent):
        '''发送B站热门视频榜单''' 

        message_chain = event.get_messages() 
        logger.info(message_chain)

        results = get_baidu_hotsearch()
        # At 消息发送者
        
        for i, item in enumerate(results, 1):
            chain = [] 
            str1 = f'【{i}】标题：{item["title"]}\t'
            str2 = f'热搜指数：{item["hot_index"]}\t链接：{item["detail_url"]}\n'
            chain.extend([
                Plain(str1),
                Image.fromURL(item["image_url"]),
                Plain(str2)
            ])
            yield event.chain_result(chain)
    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
