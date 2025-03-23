import requests
from bs4 import BeautifulSoup
import json

def get_baidu_hotsearch():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = 'https://top.baidu.com/board?tab=realtime'
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        items = soup.find_all('div', class_='category-wrap_iQLoo')
        
        results = []
        
        for item in items:
            # 提取标题
            title = item.find('div', class_='c-single-text-ellipsis').text.strip()
            
            # 提取图片链接（处理可能的懒加载）
            img_tag = item.find('img')
            img_url = img_tag.get('src') or img_tag.get('data-src')
            
            # 提取详细链接
            detail_url = item.find('a')['href'].strip()
            
            # 提取热搜指数
            hot_index = item.find('div', class_='hot-index_1Bl1a').text.strip()
            
            results.append({
                'title': title,
                'image_url': img_url,
                'detail_url': detail_url,
                'hot_index': hot_index
            })
        
        return results
        
    except Exception as e:
        print(f"抓取失败: {str(e)}")
        return []

if __name__ == '__main__':
    hot_searches = get_baidu_hotsearch()
    
    # 输出结果
    print(f"共抓取到 {len(hot_searches)} 条热搜：")
    for idx, item in enumerate(hot_searches, 1):
        print(f"\n【{idx}】{item['title']}")
        print(f"图片链接: {item['image_url']}")
        print(f"详情链接: {item['detail_url']}")
        print(f"热搜指数: {item['hot_index']}")
    
    # 保存为JSON文件
    with open('baidu_hotsearch.json', 'w', encoding='utf-8') as f:
        json.dump(hot_searches, f, ensure_ascii=False, indent=2)
    print("\n数据已保存到 baidu_hotsearch.json")