from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest, HttpRequest, HttpResponseNotFound
from .models import Post, Content
from user.models import User
from user.views import auth
import simplejson
import datetime
import math


@auth
def pub(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        title = payload['title']
        print(title)

        post = Post()
        post.title = title
        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.author = request.user
        post.save()

        content = Content()
        content.post = post
        content.content = payload['content']
        content.save()

        return JsonResponse({"post_id": post.id})

    except Exception as e:
        print(e)
        return HttpResponseBadRequest(b'error')


def get(request: HttpRequest, id):
    try:
        post = Post.objects.get(pk=eval(id))
        return JsonResponse({
            'post': {
                'post_id': post.id,
                'post_title': post.title,
                'postdate': int(post.postdate.timestamp()),
                'author_name': post.author.name,
                'author_id': post.author_id,
                'content': post.content.content
            }})
    except Exception as e:
        return HttpResponseNotFound()


def validate(d: dict, name: str, convert_func, default, validate_func):
    try:
        x = convert_func(d.get(name))
        ret = validate_func(x, default)
    except:
        ret = default
    return ret


def getall(request: HttpRequest):
    page = validate(request.GET, 'page', int, 1,lambda x,y:x if x>0 else y)

    size = validate(request.GET, 'size', int, 20,lambda x,y:x if x>0 and x<30 else y)

    start = (page - 1) * size
    posts = Post.objects.order_by('-pk')
    count = posts.count()
    pages = math.ceil(count / size)
    posts = posts[start:start + size]
    if posts:
        return JsonResponse({
            'posts': [{
                'post_id': post.id,
                'post_title': post.title
            } for post in posts],
            'pagination': {
                'page': page,
                'size': size,
                'count': count,
                'pages': pages,
            }})
    else:
        return HttpResponseNotFound()
