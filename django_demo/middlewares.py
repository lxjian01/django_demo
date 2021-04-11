from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect

from django_demo import logger

try:

    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class LoginMiddleware(MiddlewareMixin):
    """
    登录拦截器
    """
    def process_request(self, request):
        path = request.path
        logger.info(path)
        no_intercept_urls = ["/user/to_login","/user/to_login/","/user/login","/user/login/","/user/to_register","/user/to_register/","/user/register","/user/register/"]
        if path not in no_intercept_urls:
            if request.session.get('token',None):
                pass
            else:
                return HttpResponseRedirect('/user/to_login/')