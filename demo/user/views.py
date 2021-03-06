from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from . import models
from . import forms


def login(request):
    if request.session.get('is_login', None): #不允許重複登錄
        status = 'login'
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '請檢查填寫的內容!'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            if username == 'admin':
                if password == 'yzucs21':
                    return HttpResponseRedirect('/admin')
            try:
                user = models.User.objects.get(name=username)
            except:
                message = '用戶不存在!'
                return render(request, 'login.html', locals())
            if user.password == password:
                #在session字典裡寫入用戶狀態和數據
                request.session['is_login'] = True
                request.session['user_name'] = user.name
                status = 'login'
                return HttpResponseRedirect('/')
            else:
                message = '密碼不正確'
                return render(request, 'login.html', locals())
        else:
            return render(request, 'login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "請檢查填寫的內容!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            common_store = register_form.cleaned_data.get('common_store')

            if password1[0].isalpha() == False:
                message = "密碼開頭必須為英文字母!"
                return render(request, 'register.html', locals())

            if password1 != password2:
                message = "兩次輸入的密碼不同!"
                return render (request , 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = "用戶名已存在!"
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)

                if same_email_user:
                    message = "該信箱已被註冊!"
                    return render(request, 'register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.common_store = common_store
                new_user.save()

                return redirect('/user/login')
        else:
            return render(request, 'register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'register.html')


def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/')

def reset_pw(request):
    if request.method == 'POST':
        reset_pw_form = forms.ResetForm(request.POST)
        message = "請檢查填寫的內容!"
        if reset_pw_form.is_valid():
            password1 = reset_pw_form.cleaned_data.get('password1')
            password2 = reset_pw_form.cleaned_data.get('password2')
            password3 = reset_pw_form.cleaned_data.get('password3')
            try:
                user = models.User.objects.get(name=request.session.get('user_name'))
            except:
                return HttpResponseRedirect('/')

            if user.password != password1:
                message = "輸入錯誤的原始密碼!"
                return render (request , 'reset_pw.html', locals())
            else:
                if password2[0].isalpha() == False:
                    message = "密碼開頭必須為英文字母!"
                    return render(request, 'reset_pw.html', locals())
                else:
                    if password2 != password3:
                        message = "兩次輸入的密碼不同!"
                        return render(request, 'reset_pw.html', locals())
                    user.password = password2
                    user.save()
                    return HttpResponseRedirect('/')
        else:
            return render(request, 'reset_pw.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'reset_pw.html')