import requests
import json
def searchbhot():   
# 热门视频API地址
    url = 'https://api.bilibili.com/x/web-interface/popular'

# 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.bilibili.com/'
    }

    try:
    # 发送GET请求
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
    
    # 解析JSON数据
        data = response.json()
        video_list = data['data']['list']
    
    # 遍历视频列表提取信息
        results = []
        for video in video_list:
            title = video['title']                # 标题
            author = video['owner']['name']       # 作者
            play = video['stat']['view']          # 播放量
            bvid = video['bvid']                  # 视频BV号
            video_url = f'https://www.bilibili.com/video/{bvid}'  # 视频链接
        
            results.append({
                '标题': title,
                '作者': author,
                '播放量': play,
                '链接': video_url
            })
    
    
        
    except requests.exceptions.RequestException as e:
        print(f'请求出错：{e}')
    except json.JSONDecodeError:
        print('解析JSON数据失败')
    except KeyError:
        print('数据格式异常，请检查字段是否存在')
    return results