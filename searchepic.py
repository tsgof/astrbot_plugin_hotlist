import requests
from datetime import datetime

def get_free_games():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=zh-CN&country=CN&allowCountries=CN'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # 增加数据有效性检查
        if not data or 'data' not in data or 'Catalog' not in data['data']:
            print("API返回数据结构异常")
            return []
        
        elements = data['data']['Catalog']['searchStore'].get('elements', [])
        results = []
        
        for game in elements:
            try:
                # 基础信息（增加空值处理）
                title = game.get('title') or '未知标题'
                game_id = game.get('id', '')
                description = game.get('description', '暂无描述').strip()

                # 价格信息（多层安全访问）
                price = game.get('price', {}) or {}
                total_price = price.get('totalPrice', {}) or {}
                fmt_price = total_price.get('fmtPrice', {}) or {}
                
                original_price = fmt_price.get('originalPrice', '')
                discount_price = fmt_price.get('discountPrice', '')
                currency = total_price.get('currencyCode', 'CNY')

                # 促销信息（安全访问嵌套结构）
                promotions = game.get('promotions', {}) or {}
                promotional_offers = promotions.get('promotionalOffers', []) or []
                upcoming_offers = promotions.get('upcomingPromotionalOffers', []) or []

                # 图片信息（安全访问）
                images = [
                    img['url'] 
                    for img in game.get('keyImages', []) 
                    if img.get('type') == 'Thumbnail'
                ] if game.get('keyImages') else []

                # 时间处理（带异常捕获）
                def safe_parse(time_str):
                    try:
                        return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d %H:%M")
                    except:
                        return "时间解析失败"

                # 当前免费判断（增加类型检查）
                try:
                    is_free = float(total_price.get('discountPrice', 1)) == 0 \
                            and float(total_price.get('originalPrice', 0)) > 0
                except:
                    is_free = False

                # 构建结果字典
                game_data = {
                    '标题': title,
                    '游戏ID': game_id,
                    '描述': description,
                    '原价': original_price,
                    '现价': discount_price,
                    '货币': currency,
                    '是否免费': is_free,
                    '缩略图': images[0] if images else '',
                    '当前促销': [],
                    '即将到来促销': []
                }

                # 处理促销信息（带空值检查）
                for offer in promotional_offers:
                    for sub_offer in offer.get('promotionalOffers', []):
                        start = safe_parse(sub_offer.get('startDate', ''))
                        end = safe_parse(sub_offer.get('endDate', ''))
                        if start and end:
                            game_data['当前促销'].append(f"{start} 至 {end}")

                for offer in upcoming_offers:
                    for sub_offer in offer.get('promotionalOffers', []):
                        start = safe_parse(sub_offer.get('startDate', ''))
                        end = safe_parse(sub_offer.get('endDate', ''))
                        if start and end:
                            game_data['即将到来促销'].append(f"{start} 至 {end}")

                results.append(game_data)
                
            except Exception as e:
                print(f"处理游戏数据时出错: {str(e)}")
                continue

        return [game for game in results if game['是否免费']]
            
    except Exception as e:
        print(f"请求失败: {str(e)}")
        return []

if __name__ == '__main__':
    free_games = get_free_games()
    for index, game in enumerate(free_games):
        print(f"\n【免费游戏 {index+1}】")
        print(f"标题：{game['标题']}")
        print(f"描述：{game['描述']}")
        print(f"价格：{game['原价']} → {game['现价']}")
        if game['当前促销']:
            print(f"当前免费期：{game['当前促销'][0]}")
        if game['即将到来促销']:
            print(f"即将到来：{game['即将到来促销'][0]}")
        print("=" * 60)