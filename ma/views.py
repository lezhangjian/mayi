from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .shenma import ShenMa
import json
# Create your views here.

class MaYi(View):
    def get(self,request):
        req = request.GET.get('searchword')
        print(req)
        start = ShenMa(req)
        play_list, title, img_url, film_name, actor_name, type, position, year, language, context = start.film_play_url()
        title_url = dict(zip(title,play_list))
        # print('加载完成')
        return render(request, 'search.html',locals())

    def post(self,request):
        req = request.POST.get('searchword')
        print(req)
        start = ShenMa(req)
        play_list, title, img_url, film_name, actor_name, type, position, year, language, context = start.film_play_url()
        title_url = dict(zip(title,play_list))
        # print('加载完成')
        return render(request, 'search.html',locals())

class Test(View):
    def get(self, request):
        with open('/home/lezhangjian/lezhangjian/mayi/ma/recommend1.txt','r') as f:
            recommend1 = json.loads(f.read())
        with open('/home/lezhangjian/lezhangjian/mayi/ma/recommend2.txt','r') as f:
            recommend2 = json.loads(f.read())
        with open('/home/lezhangjian/lezhangjian/mayi/ma/film.txt','r') as f:
            film = json.loads(f.read())
        with open('/home/lezhangjian/lezhangjian/mayi/ma/TV.txt','r') as f:
            TV = json.loads(f.read())
        with open('/home/lezhangjian/lezhangjian/mayi/ma/comic.txt','r') as f:
            comic = json.loads(f.read())
        return render(request, 'index.html',locals())