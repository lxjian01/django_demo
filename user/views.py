import re
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django_demo import logger
from user import tasks
from user.models import UserInfo
from user.tasks import send_register_email
from utils.email_handler import django_send_email
from utils.response_helper import MyResponse, ResState
from utils.token_handler import TokenHandler

# 跳转到登录页面
def to_login(request):
    return render(request, 'login.html')

# 跳转到注册页面
def to_register(request):
    return render(request, 'register.html')

# 注册
@require_http_methods(["POST"])
def register(request):
    myRes = MyResponse()
    username = request.POST.get("username")
    email = request.POST.get("email")
    pwd = request.POST.get("pwd")
    pwd_ok = request.POST.get("pwd_ok")
    try:
        if len(username) < 6 or len(username) > 64:
            return myRes.to_json_msg("用户名长度应在6-64之间")
        if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
            # 返回错误信息
            return myRes.to_json_msg("邮箱格式不正确")
        elif pwd != pwd_ok:
            return myRes.to_json_msg("密码不一致，请重新输入")
        user = UserInfo.objects.filter(username=username).first()
        if user:
            return myRes.to_json_msg("用户名已存在")
        user = UserInfo.objects.filter(email=email).first()
        if user:
            return myRes.to_json_msg("邮箱已存在")
        pwd = make_password(pwd, None, 'pbkdf2_sha256')
        user = UserInfo(username=username, pwd=pwd,email=email)
        user.save()
        myRes.status = ResState.HTTP_SUCCESS
        # 将注册激活token发送给用户激活
        token = TokenHandler().encrypt(str(user.id))
        user_id = TokenHandler().decrypt(token)
        logger.info("user_id is {0}".format(user_id))
        # send_register_email(username,token,email)
        tasks.send_register_email.delay(username,token,email)
    except Exception as ex:
        logger.error("Register error by {0}".format(ex))
        myRes.msg = str(ex)

    return myRes.to_json()

# 登录
@require_http_methods(["POST"])
def login(request):
    myRes = MyResponse()
    username = request.POST.get("username")
    pwd = request.POST.get("pwd")
    try:
        if username is None or username == "":
            return myRes.to_json_msg("用户名不能为空")
        if pwd is None or pwd == "":
            return myRes.to_json_msg("密码不能为空")
        user = UserInfo.objects.filter(username=username).first()
        if user is None:
            return myRes.to_json_msg("用户不存在")
        if user.is_active == 1:
            return myRes.to_json_msg("请先激活账号")
        if user.is_enabled == 1:
            return myRes.to_json_msg("账号已被禁用，请与管理员连携")
        pwd_bool = check_password(pwd, user.pwd)
        if not pwd_bool:
            return myRes.to_json_msg("密码错误")
        response = myRes.to_json()
        token = TokenHandler().encrypt(str(user.id))
        response.set_cookie("token", token)
        request.session["token"] = token
        myRes.status = ResState.HTTP_SUCCESS
        myRes.msg = "登录成功"
        return myRes.to_json()
    except Exception as ex:
        logger.error("Login error by {0}".format(ex))
        myRes.msg = str(ex)
        return myRes.to_json()

# 激活
@require_http_methods(["GET"])
def active(request,token):
    logger.info(token)
    try:
        user_id = TokenHandler().decrypt(token)
        if user_id is None or user_id == "" or user_id == "None":
            raise Exception("无效的认证")
        user = UserInfo.objects.filter(id=int(user_id)).first()
        if user is None:
            raise Exception("用户不存在")
        if user.is_active == 1:
            user.is_active = 0
            user.save()
        return redirect('/user/to_login')
    except Exception as ex:
        logger.error("Login error by {0}".format(ex))
        return render(request, "error.html", {"msg": str(ex)});