from tools_hjh.Chrome import Chrome
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from tools_hjh import HTTPTools, Tools, Log
import json
import re
import os
import sys

try:
    sys_argv_1 = sys.argv[1]
except:
    sys_argv_1 = ''
    
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/",
    "cookie":"buvid3=77CE9384-58A9-6FA8-2887-43BDFB8FB13153775infoc; b_nut=1738808053; _uuid=5AFD7B76-F3D5-9556-81044-310CEEB28FFBA54661infoc; buvid_fp=a707572b4a023295611d25377e5200ba; enable_web_push=DISABLE; home_feed_column=5; buvid4=B9CC925B-E9EC-FCF6-521D-CDB4DB42924F57462-025020602-nod6mU0ldP+etlR5l7OO+w==; DedeUserID=84131551; DedeUserID__ckMd5=15aa2aee95cb2c8f; hit-dyn-v2=1; header_theme_version=CLOSE; rpdid=|(JJml)mJJ~)0J'u~Jmklu~~J; enable_feed_channel=ENABLE; LIVE_BUVID=AUTO3917413704698685; PVID=4; bsource=search_bing; bmg_af_switch=1; bmg_src_def_domain=i1.hdslb.com; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDM0MjAyNjQsImlhdCI6MTc0MzE2MTAwNCwicGx0IjotMX0.hR5CWBt08cSgh5kpRlXn-lktrgPEOprhIU1mfcuY7Is; bili_ticket_expires=1743420204; SESSDATA=f46dd477,1758713389,a02d4*32CjBFIxZez9Yw4EsHKfFeEW3KUxe8ntUHbCx-84Bm5AMojY1_LZtsPCUonLkXDN8Ndf0SVkpfMmJTUGZGbXdtcG5vd29CNWhqRUZ5Y1FwckxkTW95MXlXQjl3clZkRExiNWNVb3FZU21vVXAtdkllNHBjRlhkbkpma3VBVWxCanJPdW1kWUZEellRIIEC; bili_jct=b369a500c36834d6d00fc406677d9de9; sid=7sivgz0o; b_lsid=DFCEEA9E_195DCD22A42; CURRENT_QUALITY=32; bp_t_offset_84131551=1049386541933133824; CURRENT_FNVAL=2000; browser_resolution=1536-190"
}

date = Tools.locatdate()
log = Log(date + '.log')


def main():
    chrome_path = r'D:\MyApps\CentBrowser\App\chrome.exe'
    chromedriver_path = r'D:\MyApps\CentBrowser\chromedriver.exe'
    
    cp = Chrome(chrome_path=chrome_path, chromedriver_path=chromedriver_path, is_hidden=False, is_display_picture=False, headers=headers)
    page = cp.get('https://www.bilibili.com/video/' + sys_argv_1)
    volumes = cp.chrome.find_elements(By.CLASS_NAME, 'slide-item')
    
    all_list = []
    for volume in volumes:
        try:
            volume.click()
        except:
            continue
        page = cp.chrome.page_source
        bs = BeautifulSoup(page, features="lxml")
        videos = bs.find('div', class_='video-pod__body').find_all('div', class_='pod-item video-pod__item simple')
        for video in videos:
            url = 'https://www.bilibili.com/video/' + video['data-key'] + '?t=16.9'
            title = video.find('div', class_='title-txt').text.replace(' ', '_')
            all_list.append((url, title))
    cp.close()

    i = 1
    for one in all_list:
        if i < 9:
            tt = '0' + str(i)
        else:
            tt = str(i)
        url = one[0]
        title = tt + '_' + one[1]
        v_page = HTTPTools.get(url, headers=headers)
        script_content = re.search(r'<script>window\.__playinfo__=(.*?)</script>', v_page).group(1)
        Tools.echo(script_content, 'd:/1.txt', 'w')
        video_info = json.loads(script_content)
        video_url = ''
        if len(video_info['data']['dash']['video']) == 1:
            video_url = video_info['data']['dash']['video'][0]['baseUrl']
        for v in video_info['data']['dash']['video']:
            if v['height'] == 1080:
                continue
            if v['height'] == 720:
                video_url = v['baseUrl']
                break
            if v['height'] == 480 and video_url == '':
                video_url = v['baseUrl']
                break
            if v['height'] == 360 and video_url == '':
                video_url = v['baseUrl']
                break
        if video_url == '':
            video_url = video_info['data']['dash']['video'][0]['baseUrl']
        audio_url = video_info['data']['dash']['audio'][0]['baseUrl']
        
        mp4_size_1 = HTTPTools.get_size(video_url, headers=headers)
        mp3_size_1 = HTTPTools.get_size(audio_url, headers=headers)
        
        mp4 = title + '_a.mp4'
        mp3 = title + '_b.mp4'
        
        if os.path.exists(mp4):
            mp4_size_2 = os.path.getsize(mp4)
        else:
            mp4_size_2 = 0
            
        if os.path.exists(mp3):
            mp3_size_2 = os.path.getsize(mp3)
        else:
            mp3_size_2 = 0
        
        if mp4_size_1 > mp4_size_2:
            log.info(mp4, 'begin', 'src=' + str(round(mp4_size_1 / 1024 / 1024, 2)) + 'MB', 'dst=' + str(round(mp4_size_2 / 1024 / 1024, 2)) + 'MB')
            Tools.rm(mp4)
            try:
                HTTPTools.download(video_url, mp4, headers)
                log.info(mp4, 'begin', 'src=' + str(round(mp4_size_1 / 1024 / 1024, 2)) + 'MB', 'dst=' + str(round(os.path.getsize(mp4) / 1024 / 1024, 2)) + 'MB')
            except:
                Tools.rm(mp4)
        else:
            log.warning(mp4 + ' exists')
        
        if mp3_size_1 > mp3_size_2:
            log.info(mp3, 'begin', 'src=' + str(round(mp3_size_1 / 1024 / 1024, 2)) + 'MB', 'dst=' + str(round(mp3_size_2 / 1024 / 1024, 2)) + 'MB')
            Tools.rm(mp3)
            try:
                HTTPTools.download(audio_url, mp3, headers)
                log.info(mp3, 'begin', 'src=' + str(round(mp3_size_1 / 1024 / 1024, 2)) + 'MB', 'dst=' + str(round(os.path.getsize(mp3) / 1024 / 1024, 2)) + 'MB')
            except:
                Tools.rm(mp3)
        else:
            log.warning(mp3 + ' exists')
            
        i = i + 1
    

if __name__ == '__main__':
    main()
