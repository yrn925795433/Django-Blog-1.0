from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest
import simplejson
from .models import User
from django.conf import settings
import bcrypt
import jwt
import datetime
from django.db.models import Q

AUTH_EXPIRE = 8 * 60 * 60
def gen_token(user_id):
    key = settings.SECRET_KEY
    j = jwt.encode({'user': user_id,
                    'exp':int(datetime.datetime.now().timestamp())+AUTH_EXPIRE}
                   , key, 'HS256')
    return j.decode()


def reg(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)

        email = payload['email']
        query = User.objects.filter(email=email)

        if query.first():
            return HttpResponseBadRequest('用户名已存在')

        name = payload['name']
        password = payload['password']

        user = User()
        user.email = email
        user.name = name
        user.password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            user.save()
            token = gen_token(user.id)
            res = JsonResponse({
                'user': {'user_id': user.id, 'user_name': user.name, 'user_email': user.email},
                'token': token
            })
            res.set_cookie('jwt', token)
            return res
        except Exception as e:
            return JsonResponse({'reason': 'not found error'}, status=400)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest(b'error argument', status=400)


def login(request: HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        # name = payload['name']
        email = payload['email']
        password = payload['password']
        user = User.objects.filter(email=email).get()
        if user:
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                token = gen_token(user.id)

                res = JsonResponse({
                    'user': {'user_id': user.id, 'user_name': user.name, 'user_email': user.email},
                    'token': token
                })
                res.set_cookie('jwt',token)
                return res
            else:
                return HttpResponseBadRequest(b'failed connection')
        else:
            return HttpResponseBadRequest(b'failed connection')

    except Exception as e:
        print(e)
        return HttpResponseBadRequest(b'failed connection')


def auth(view_func):
    def wrapper(request:HttpRequest):
        token = request.META.get('HTTP_JWT',None)
        if not token:
            print('================')
            return HttpResponseBadRequest('no token',status=400)
        key = settings.SECRET_KEY
        try:
            payload = jwt.decode(token,key,algorithms=['HS256'])
            user = User.objects.filter(pk=payload['user']).first()
            if user:

                request.user = user
                ret = view_func(request)
                return ret
            else:
                return HttpResponseBadRequest('password user error1')
        except jwt.ExpiredSignatureError as e:
            return HttpResponseBadRequest('Expired')
        except Exception as e:
            print(e)
            return HttpResponseBadRequest('password user error2')

    return wrapper

# @auth
def show(request: HttpRequest):
    print(11111111,request.GET)
    print(2222222,request.POST)
    res = JsonResponse({'status': 'ok'})
    res['Access-Control-Allow-Origin'] = '*'
    return res

