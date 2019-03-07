import requests
import re
from lxml import etree
import json

class ShenMa(object):
    def __init__(self, film_name):
        self.film_name = film_name
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        }

    # 返回视频播放地址和播放资源
    def film_play_url(self):
        se = requests.session()
        # 搜索界面的url
        url = 'http://www.4k4k.org/search.php'
        data = {
            'searchword': self.film_name
        }
        res = se.post(url, headers=self.headers, data=data).text
        page = etree.HTML(res)
        # print(res)
        url = page.xpath('//a[@class="link-hover"]/@href')
        # 搜索结果的url
        page_url = 'http://www.4k4k.org' + url[0]
        res = se.get(page_url).text.encode('ISO-8859-1').decode()
        # print(res)
        page = etree.HTML(res)
        # 可以有多个资源.
        url = page.xpath('//div[@id="vlink_1"]/ul/li/a/@href')
        title = page.xpath('//div[@id="vlink_1"]/ul/li/a/@title')
        # 获取影片的详细信息
        img_url = page.xpath('//img[@class="lazy"]/@data-original')
        film_name = page.xpath('//img[@class="lazy"]/@alt')
        actor_names = page.xpath('//div[@class="ct-c"]/dl/dt/a/text()')
        actor_name = ''
        for name in actor_names:
            actor_name = actor_name+" "+name
        type = page.xpath('//div[@class="ct-c"]/dl/dt[3]/text()')
        position = page.xpath('//div[@class="ct-c"]/dl/dd[2]/text()')
        year = page.xpath('//div[@class="ct-c"]/dl/dd[3]/text()')
        language = page.xpath('//div[@class="ct-c"]/dl/dd[4]/text()')
        context = page.xpath('//div[@class="ee"]/text()')
        # 播放界面的url
        page_url = 'http://www.4k4k.org' + url[0]
        res = se.get(page_url).text
        r = re.findall('VideoInfoList=(.*?)</script>', res)
        r = re.findall('https://(.*?).m3u8', r[0])
        # 视频的真实播放地址
        url_list = ['https://www.apiapi88.com/m3u8/?url=https://' + url + '.m3u8' for url in r]
        return (url_list,title,img_url[0],film_name[0],actor_name,type[0],position[0],year[0],language[0],context[0])


class Detail(object):
    def detail(self):
        # 获取神马电影主页面的推荐影视名称以及图片地址
        url = 'http://www.4k4k.org/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        }
        req = requests.get(url,headers=headers).text.encode('ISO-8859-1').decode()
        # print(req)
        page = etree.HTML(req)
        film_name = page.xpath('//div[@class="index-tj-l"]/ul/li/a/@title')
        img_url = page.xpath('//div[@class="index-tj-l"]/ul/li/a/img/@data-original')
        # 获取推荐影视的  名称以及图片地址
        film_urls = ['http://192.168.31.132:8000/mayi/?searchword='+na for na in film_name[0:12]]
        film_img_list = list(zip(img_url[0:12],film_urls[0:12]))
        recommend = json.dumps(dict(zip(film_name[0:6],film_img_list[0:6])))
        with open('recommend1.txt','w') as f:
            f.write(recommend)
        recommend = json.dumps(dict(zip(film_name[6:12], film_img_list[6:12])))
        with open('recommend2.txt', 'w') as f:
            f.write(recommend)
        name = page.xpath('//div[@class="index-area clearfix"]/ul/li/a/@title')
        img = page.xpath('//div[@class="index-area clearfix"]/ul/li/a/img/@data-original')
        #  获取电影的 名称以及地址
        film_urls = ['http://192.168.31.132:8000/mayi/?searchword='+na for na in name[0:18]]
        # print(film_urls)
        film_img_list = list(zip(img[0:18],film_urls[0:18]))
        # print(film_img_list)
        film = json.dumps(dict(zip(name[0:6],film_img_list[0:6])))
        with open('film.txt','w') as f:
            f.write(film)
        TV = json.dumps(dict(zip(name[6:12],film_img_list[6:12])))
        # 获取电视剧的 名称以及图片地址
        with open('TV.txt','w') as f:
            f.write(TV)
        comic = json.dumps(dict(zip(name[12:18],film_img_list[12:18])))
        with open('comic.txt','w') as f:
            f.write(comic)





if __name__ == '__main__':
    # run = ShenMa('灵能百分百第二季/路人超能100')
    # print(run.film_play_url())
    # print(play_list,title)
    run = Detail()
    run.detail()
    # a = [1,2,3]
    # b = [4,5,6]
    # # c = ['a','b','c']
    # # print(dict(zip(c,[a,b])))
    # print(list(zip(a[0:3],b[0:3])))
