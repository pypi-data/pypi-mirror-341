# coding:utf-8
import sys
from tools_hjh import DBConn, Chrome
from bs4 import BeautifulSoup
from tools_hjh.HTTPTools import HTTPTools
from selenium.webdriver.common.by import By
import json
import re

chrome_path = r'D:\MyApps\CentBrowser\App\chrome.exe'
chromedriver_path = r'D:\MyApps\CentBrowser\chromedriver.exe'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/",
    "cookie":"buvid3=77CE9384-58A9-6FA8-2887-43BDFB8FB13153775infoc; b_nut=1738808053; _uuid=5AFD7B76-F3D5-9556-81044-310CEEB28FFBA54661infoc; buvid_fp=a707572b4a023295611d25377e5200ba; enable_web_push=DISABLE; home_feed_column=5; buvid4=B9CC925B-E9EC-FCF6-521D-CDB4DB42924F57462-025020602-nod6mU0ldP+etlR5l7OO+w==; DedeUserID=84131551; DedeUserID__ckMd5=15aa2aee95cb2c8f; hit-dyn-v2=1; header_theme_version=CLOSE; rpdid=|(JJml)mJJ~)0J'u~Jmklu~~J; enable_feed_channel=ENABLE; LIVE_BUVID=AUTO3917413704698685; PVID=4; bsource=search_bing; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM0MjAyNjQsImlhdCI6MTc0MzE2MTAwNCwicGx0IjotMX0.hR5CWBt08cSgh5kpRlXn-lktrgPEOprhIU1mfcuY7Is; bili_ticket_expires=1743420204; SESSDATA=f46dd477,1758713389,a02d4*32CjBFIxZez9Yw4EsHKfFeEW3KUxe8ntUHbCx-84Bm5AMojY1_LZtsPCUonLkXDN8Ndf0SVkpfMmJTUGZGbXdtcG5vd29CNWhqRUZ5Y1FwckxkTW95MXlXQjl3clZkRExiNWNVb3FZU21vVXAtdkllNHBjRlhkbkpma3VBVWxCanJPdW1kWUZEellRIIEC; bili_jct=b369a500c36834d6d00fc406677d9de9; sid=7sivgz0o; b_lsid=DFCEEA9E_195DCD22A42; CURRENT_QUALITY=32; bp_t_offset_84131551=1049386541933133824; CURRENT_FNVAL=2000; browser_resolution=1536-190"
}

path = 'D:/小说视频下载/'

metadata = []
# metadata.append(('一周一次买下同班同学的那些事（有字）', 'BV1f34y1c7AM', 'MP4', '没有奶茶的世界'))
# metadata.append(('我怎么可能成为你的恋人，不行不行（有字）', 'BV1Xb4y1M7th', 'MP4', '没有奶茶的世界'))
metadata.append(('安达与岛村', 'BV1mM4y1H77M', 'MP3', '没有奶茶的世界'))
# metadata.append(('家里蹲吸血姬的郁闷', 'BV1tF411Z7BM', 'MP3', '没有奶茶的世界'))
# metadata.append(('转生王女与天才千金的魔法革命', 'BV1oN411a7oW', 'MP3', '没有奶茶的世界'))
# metadata.append(('将放言说女生之间不可能的女孩子，在百日之内彻底攻陷的百合故事', 'BV1yk4y1Z7G7', 'MP3', '没有奶茶的世界'))

try:
    sys_argv_1 = sys.argv[1]
except:
    sys_argv_1 = 'get'
    sys_argv_1 = 'print'
    sys_argv_1 = 'rename'
    sys_argv_1 = 'get'
try:
    sys_argv_2 = sys.argv[2]
except:
    sys_argv_2 = None
try:
    sys_argv_3 = sys.argv[3]
except:
    sys_argv_3 = 32
    

def main(): 
    db = DBConn('sqlite', db='D:/MyFiles/MyPy/data/bilibili.db')
    createDatabase(db, rebuild=True)
    if  sys_argv_1 == 'get':
        get(db)

    
def createDatabase(db, rebuild=False):
    if rebuild:
        db.run('drop table if exists t_m')

    t_m = '''
        create table if not exists t_m(
            name_ text,
            uploader text,
            url text, 
            title text,
            definition text,
            downloaded text
        )
    '''
    
    db.run(t_m)

    
def get(db):
    insert_sql = 'insert into t_m select ?,?,?,?,?,? where not exists(select 1 from t_m where url = ?)'
    cp = Chrome(chrome_path=chrome_path, chromedriver_path=chromedriver_path, is_hidden=False, is_display_picture=False, headers=headers)
    for meta in metadata:
        name_ = meta[0]
        id_ = meta[1]
        type_ = meta[2]
        up_ = meta[3]
        
        page = cp.get('https://www.bilibili.com/video/' + id_)
        volumes = cp.chrome.find_elements(By.CLASS_NAME, 'slide-item')
        
        i = 1
        params = []
        for volume in volumes:
            try:
                volume.click()
            except:
                continue
            page = cp.chrome.page_source
            bs = BeautifulSoup(page, features="lxml")
            videos = bs.find('div', class_='video-pod__body').find_all('div', class_='pod-item video-pod__item simple')
            for video in videos:
                if i <= 9:
                    tt = '0' + str(i)
                else:
                    tt = str(i)
                url = 'https://www.bilibili.com/video/' + video['data-key']
                title = tt + '_' + video.find('div', class_='title-txt').text.replace(' ', '_')
                
                v_page = HTTPTools.get(url, headers=headers)
                script_content = re.search(r'<script>window\.__playinfo__=(.*?)</script>', v_page).group(1)
                video_info = json.loads(script_content)
                
                audio_url = video_info['data']['dash']['audio'][0]['baseUrl']
                params.append((name_, up_, audio_url, title + '.mp3', '0P', '0', url))
                print(audio_url)
                
                if type_ == 'MP4':
                    
                    param = {}
                    for v in video_info['data']['dash']['video']:
                        if v['height'] == 720:
                            param['720'] = (name_, up_, v['baseUrl'], title + '.mp4', '720P', '0', url)
                        elif v['height'] == 480:
                            param['480'] = (name_, up_, v['baseUrl'], title + '.mp4', '480P', '0', url)
                        elif v['height'] == 1080:
                            param['1080'] = (name_, up_, v['baseUrl'], title + '.mp4', '1080P', '0', url)
                        elif v['height'] == 360:
                            param['360'] = (name_, up_, v['baseUrl'], title + '.mp4', '360P', '0', url)
                            
                    if '720' in param:
                        params.append(param['720'])
                        print(name_, title + '.mp4', '720P')
                    elif '720' not in param and '480' in param:
                        params.append(param['480'])
                        print(name_, title + '.mp4', '480P')
                    elif '720' not in param and '480' not in param and '1080' in param:
                        params.append(param['1080'])
                        print(name_, title + '.mp4', '1080P')
                    else:
                        params.append((name_, up_, video_info['data']['dash']['video'][0]['baseUrl'], title + '.mp4', str(video_info['data']['dash']['video']['height']) + 'P', '0', url))
                        print(name_, title + '.mp4', '360P')

                i = i + 1
                db.run(insert_sql, params)
                params.clear()
    cp.close()
    
    
if __name__ == '__main__':
    main()

