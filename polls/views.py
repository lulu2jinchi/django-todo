from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from datetime import datetime, timezone
from .models import *


def getJSONResp(resp, ok=True, message=''):
    return HttpResponse(json.dumps(
        {
            'success': ok,
            'message': message,
            'data': resp
        }
    ), content_type='application/json')


def toDateTime(mills):
    return datetime.fromtimestamp(mills / 1000, timezone.utc)


@login_required
def index(request):
    # text = requests.get('http://127.0.0.1:8080').text
    # return HttpResponse(text, content_type='text/html')
    return render(request, 'index.html')

# 查询当前用户的所有事项
# /api/item_list


@login_required
def item_list(request):
    items = TodoItem.objects.filter(userid=request.user.id)
    resp = []
    for item in items:
        resp.append(
            item.toJSON()
        )
    return getJSONResp(resp)


@login_required
@csrf_exempt
def item(request, id=-1):
    # 查询
    if request.method == 'GET':
        if id < 0:
            return getJSONResp(None, False, '请提供id')
        try:
            print('传入id为', id)
            result = TodoItem.objects.get(id=id)
            if not result:
                return getJSONResp(None, False, '项目不存在！')
            if result.userid != request.user.id:
                return getJSONResp(None, False, '非法访问！')
            return getJSONResp(
                result.toJSON(), True, '成功'
            )
        except:
            return getJSONResp(None, False, '查询失败')

    # 新建
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            new_item = TodoItem(
                userid=request.user.id,
                title=payload['title'],
                create_date=toDateTime(payload['create_date']),
                due_date=toDateTime(payload['due_date']),
                status='normal'
            )
            new_item.save()
            return getJSONResp(new_item.toJSON(), True, '创建成功')
        except:
            return getJSONResp(None, False, '创建失败')
    # 修改
    if request.method == 'PUT':
        try:
            payload = json.loads(request.body)
            result = TodoItem.objects.get(id=payload['id'])
            if not result:
                return getJSONResp(None, False, '项目不存在！')
            if result.userid != request.user.id:
                return getJSONResp(None, False, '非法访问！')
            if 'title' in payload:
                result.title = payload['title']
            if 'due_date' in payload:
                result.due_date = toDateTime(payload['due_date'])
            if 'status' in payload:
                result.status = payload['status']
            result.save()
            return getJSONResp(result.toJSON(), True, '修改成功')
        except:
            return getJSONResp(None, False, '修改失败')

    # 删除
    if request.method == 'DELETE':
        if id < 0:
            return getJSONResp(None, False, '请提供id')
        try:
            print('传入id为', id)
            result = TodoItem.objects.get(id=id)
            if not result:
                return getJSONResp(None, False, '项目不存在！')
            if result.userid != request.user.id:
                return getJSONResp(None, False, '非法访问！')
            result.delete()
            return getJSONResp(
                None, True, '删除成功'
            )
        except:
            return getJSONResp(None, False, '删除失败')
