from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api.message_components import *
from astrbot.api import logger
from .searchbhot import searchbhot
from .searchbaidu import get_baidu_hotsearch
from .searchepic import get_free_games
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
        chain = []
        for i, item in enumerate(results, 1):
             
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
        '''发送百度热搜榜单''' 

        message_chain = event.get_messages() 
        logger.info(message_chain)

        results = get_baidu_hotsearch()
        # At 消息发送者
        chain = [] 
        for i, item in enumerate(results, 1):
            
            str1 = f'【{i}】标题：{item["title"]}\t'
            str2 = f'热搜指数：{item["hot_index"]}\t链接：{item["detail_url"]}\n'
            chain.extend([
                Plain(str1),
                Image.fromURL(item["image_url"]),
                Plain(str2)
            ])
        yield event.chain_result(chain)
        
    @filter.command("epic")
    async def epic_free_games(self, event: AstrMessageEvent):  # ✅ 重命名方法
        '''发送epic免费游戏榜单'''
        message_chain = event.get_messages() 
        logger.info(message_chain)
        results = get_free_games()  # ✅ 添加括号调用函数
    
        for i, game in enumerate(results, start=1):  # ✅ 正确起始索引
            chain = []
        # 使用双引号包裹字符串 ✅
            str1 = f"\n【免费游戏 {i}】\n"
            str2 = f"标题：{game['标题']}\n"
            str3 = f"描述：{game['描述'][:80]}...\n"  # 限制描述长度
            str4 = f"价格：{game['原价']} → {game['现价']}\n"
        
        # 处理促销信息 ✅
            promo_info = []
            if game['当前促销']:
                promo_info.append(f"当前免费期：{game['当前促销'][0]}")
            if game['即将到来促销']:
                promo_info.append(f"即将到来：{game['即将到来促销'][0]}")
            str5 = "\n".join(promo_info) if promo_info else "暂无促销信息"
        
        # 添加缩略图 ✅
            chain.extend([
                Plain(str1),
                Image.fromURL(game['缩略图']) if game['缩略图'] else Plain(""),
                Plain(str2 + str3 + str4 + str5)
            ])
        
        yield event.chain_result(chain)
    async def terminate(self):
        '''可选择实现 terminate 函数，当插件被卸载/停用时会调用。'''
