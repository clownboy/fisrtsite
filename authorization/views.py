from django.http import JsonResponse,HttpResponse
from django.shortcuts import render
from django.conf import settings
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from firstapp.models import Userinfo


class UserView:
    def get(self,request):
        pass
    def post(self,request):
        pass

# def session1(request):
#     request.session['message'] = 'test ok'
#     response=['data']
#     return JsonResponse(response,safe=False)
#
# def session2(request):
#     print('session',request.session.items())
#     response=['data']
#     return JsonResponse(response,safe=False)
def c2s(appid,code):
    API = 'https://api.weixin.qq.com/sns/jscode2session'
    params = 'appid=%s&secret=%s&js_code=%s&grant_type=authorization_code'%(appid,settings.WX_APP_SECRET,code)
    url = API+'?'+params
    response = requests.get(url=url)
    data = json.loads(response.text)
    print(data)
    return data

@csrf_exempt
def authorize(request):
    post_data = request.body.decode('utf-8')
    post_data = json.loads(post_data)
    print (post_data)
    code = post_data.get('code').strip()
    app_id = post_data.get('appID').strip()
    nickname = post_data.get('nickname').strip()
    # if not code or not app_id:
    #     response['message'] = 'not ok'
    #     return response
    data = c2s(app_id,code)
    openid = data.get('openid')
    # print (openid)
    # response = openid
    request.session['open_id'] = openid
    request.session['is_autherized'] = True
    #
    if not User.objects.filter(open_id=openid):
        new_user = User(open_id=openid,nickname=nickname)
        new_user.save()

    return JsonResponse(data=openid,safe=False)
