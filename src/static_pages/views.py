import datetime
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import (
    authenticate,
    login,
    logout,
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from extra.utils import create_action
from dashboard.models import dashboard, user_info, option
from geneology.models import tree, Descendant
from static_pages.forms import registerForm, dashForm, loginForm

def index(request, ref=None):
    request.session['ref_id'] = ref
    return render(request, 'flatpages/index.html')

def contact(request):
    return render(request, 'registration/support.html', {})


def validate_username(request):
    if request.is_ajax():
        username = request.GET.get('username', None)
        exist = User.objects.filter(username__iexact=username).exists()
        # print(username)
        if exist:
            return JsonResponse({'error_message': 'A user with this username already exists.'})
        else:
            exist = User.objects.filter(email__iexact=username).exists()
            if exist:
                return JsonResponse({'error_message': 'user exists'})
            else:
                return JsonResponse({'error_message': 'exists'})


def validate_password(request):
    if request.is_ajax():
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        exist = User.objects.filter(username__iexact=username).exists()
        if exist:
            user = User.objects.get(username=username)
        else:
            user = User.objects.get(email=username)
        encoded = user.password
        valid = check_password(password, encoded)
        if not valid:
            return JsonResponse({'error_message': 'The password is invalid'})
        else:
            return JsonResponse({'error_message': 'valid'})


def validate_email(request):
    if request.is_ajax():
        email = request.GET.get('email', None)
        exist = User.objects.filter(email__iexact=email).exists()
        if exist:
            return JsonResponse({'error_message': 'The email already exists'})
        else:
            return JsonResponse({'error_message': 'exists'})


def login_view(request):
    form = loginForm(request.POST or None)
    nxt = request.GET.get('next', '/profile/')
    key = request.session['ref'] = "eric"
    print(key)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            usr = User.objects.get(username__iexact=username)
            user = authenticate(username=usr.username, password=password)

        if not user:
            usr = User.objects.get(email__iexact=username)
            user = authenticate(username=usr.username, password=password)
        login(request, user)
        last_login = datetime.datetime.today()
        dashboard.objects.filter(user=request.user).update(last_login=last_login)
        print(request.user)
        if nxt:
            return redirect(nxt)
        print(form.errors)
    context = {
        'form': form
    }
    return render(request, 'registration/login.html', context)


def generate_ref():
    ref = '%010x' % random.randrange(10**80)
    ref = ref[:10]
    db_ref = dashboard.objects.filter(ref_id__exact=ref).exists()
    while db_ref:
        ref = '%010x' % random.randrange(10**80)
        ref = ref[:10]
    return ref

def have_reach_max( referer):
    instance = dashboard.objects.get(ref_id=referer)
    downliner = tree.objects.filter(p1=instance.user)
    ref_count = downliner.count()
    ref = referer
    if ref_count >= instance.total_ref() :
        print("you have more passing to child")
        for c in downliner:
            c_instance = dashboard.objects.get(user=c.doner)
            c_downliner = tree.objects.filter(p1=c.doner)
            ref_count = c_downliner.count()
            print('child')
            if ref_count >= c_instance.total_ref():
                print("child have more passing to l1_child")
                for g in c_downliner:
                    g_instance = dashboard.objects.get(user=g.doner)
                    g_downliner = tree.objects.filter(p1=g.doner)
                    ref_count = g_downliner.count()
                    if ref_count >= g_instance.total_ref():
                        print("l1_child have more passing to l2_child")
                        for gg in g_downliner:
                            gg_instance = dashboard.objects.get(user=gg.doner)
                            gg_downliner = tree.objects.filter(p1=gg.doner)
                            ref_count = gg_downliner.count()
                            if ref_count >= gg_instance.total_ref():
                                for ggg in gg_downliner:
                                    ggg_instance = dashboard.objects.get(user=ggg.doner)
                                    ggg_downliner = tree.objects.filter(p1=ggg.doner)
                                    ref_count = ggg_downliner.count()
                                    if ref_count >= ggg_instance.total_ref():
                                        ref = "1ae8f991ce"
                                    else:
                                        ref = ggg_instance.ref_id
                                        break
                            else:
                                ref = gg_instance.ref_id
                                break
                    else:
                        ref = g_instance.ref_id
                        break
            else:
                ref = c_instance.ref_id
                break
    return ref


def register(request, ref=None):
    form = registerForm(request.POST or None)
    form_dash = dashForm(request.POST or None)
    referer = ""
    if 'ref_id' in request.session:
        referer = request.session['ref_id']
    if not referer:
        request.session['ref_id'] = ref
        referer = request.session['ref_id']
        if not referer:
            referer = "1ae8f991ce"
    print(referer)
    referer = have_reach_max(referer)
    instance = dashboard.objects.get(ref_id=referer)
    ref_username = instance.user.username
    if not instance:
        ref_username = 'btcAdmin'
    nxt = request.GET.get('next', '/profile/')
    my_id = generate_ref()
    if form.is_valid() and form_dash.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        ref = ref_username
        ip = request.META['REMOTE_ADDR']
        # ques = form_dash.cleaned_data.get('sec_q')
        # ans = form_dash.cleaned_data.get('sec_a')
        country = form_dash.cleaned_data.get('country')
        phone = form_dash.cleaned_data.get('phone_num')
        name = form.cleaned_data.get('first_name') + ' ' + form.cleaned_data.get('last_name')
        referer = User.objects.get(username=ref)
        expire = datetime.date.today()
        expire = expire + datetime.timedelta(6 * 30)
        last_login = datetime.datetime.today()
        new_dashboard, created = dashboard.objects.get_or_create(
            user=request.user,
            name=name,
            sponsor=referer,
            ip_addr=ip,
            country=country,
            phoneNum=phone,
            ref_id=my_id,
            expire=expire,
            last_login=last_login,
        )
        new_user_info, created = user_info.objects.get_or_create(
            user=request.user,
        )
        new_option, created = option.objects.get_or_create(
            user=request.user,
        )
        new_dashboard.reset_date = new_dashboard.date_joined
        new_dashboard.save()
        # geneos
        p1 = new_dashboard.sponsor
        p2 = dashboard.objects.get(user=p1)
        p3 = dashboard.objects.get(user=p2.sponsor)
        p4 = dashboard.objects.get(user=p3.sponsor)
        new_tree, created = tree.objects.get_or_create(
            doner=request.user,
            p1=p1,
            p2=p2.sponsor,
            p3=p3.sponsor,
            p4=p4.sponsor,
            ref_id=new_dashboard.ref_id
        )
        Descendant.objects.create(upliner=p1, downliner=request.user)
        Descendant.objects.create(upliner=p2.sponsor, downliner=request.user)
        Descendant.objects.create(upliner=p3.sponsor, downliner=request.user)
        Descendant.objects.create(upliner=p4.sponsor, downliner=request.user)

        btcAddr.objects.create(user=request.user)

        create_action(user=request.user, verb='refered', target=p1, extra=str(request.user.username))

        create_action(user=p2.sponsor, verb='refered', target=p3.sponsor, extra=str(request.user.username))
        create_action(user=p2.sponsor, verb='refered', target=p4.sponsor, extra=str(request.user.username))

        create_action(user=p3.sponsor, verb='refered', target=p4.sponsor, extra=str(request.user.username))

        del request.session['ref_id']
        if nxt:
            return redirect(nxt)

    context = {
        'form': form,
        'form2': form_dash,
        'ref': ref_username
    }
    return render(request, 'registration/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')
