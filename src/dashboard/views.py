import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password, make_password


from extra.models import Action, Notif_Count
from extra.utils import create_action, sendmail
from financial.models import Transaction
from geneology.models import tree
from .forms import imageForm, SupportForm
from .models import (dashboard,
                     option,
                     user_info,
                     Testiment,
                     )
from .utils import get_code_from_country

def reset_account(instance):
    instance.reset_date = instance.expire
    instance.reset_count = instance.reset_count + 1
    today = datetime.date.today()
    instance.expire = today  + datetime.timedelta(6 * 30)
    instance.level = 0
    admin = User.objects.get(username='superAdmin')
    create_action(user=admin, verb="message", target=instance.user, extra="reset")

def time_left(instance, today):
    left = instance.expire - today
    if left == 30:
        create_action(user=admin, verb="expire", target=instance.user, extra="1 month")
    elif left == 15:
        create_action(user=admin, verb="expire", target=instance.user, extra="15 days")
    elif left == 5:
        create_action(user=admin, verb="expire", target=instance.user, extra="2 days")


def check_expire():
    queryset = dashboard.objects.all()
    for q in queryset:
        today = datetime.date.today()
        if q.acc_type == 'n':
            if q.expire == today:
                reset_count(q)
            else:
                time_left(q)
        if q.acc_type == 'p':
            year_time = p.expire + datetime.timedelta(6 * 30)
            if year_time == today:
                reset_count(q, today)
            else:
                time_left(q)


# def progress(request, lev):
#     trees = tree.objects.all()
#     if lev == 0:
#         tr = trees.filter(p1=request.user, timestamp__gte=request.user.dashboard.reset_date)
#     elif lev == 1:
#         tr = trees.filter(p2=request.user, timestamp__gte=request.user.dashboard.reset_date)
#     elif lev == 2:
#         tr = trees.filter(p3=request.user, timestamp__gte=request.user.dashboard.reset_date)
#     elif lev == 3:
#         tr = trees.filter(p4=request.user, timestamp__gte=request.user.dashboard.reset_date)
#     count = tr.count
#     return count

def progress(request, lev):
    trees = tree.objects.all()
    if lev == 0:
        tr = trees.filter(p1=request.user)
    elif lev == 1:
        tr = trees.filter(p2=request.user)
    elif lev == 2:
        tr = trees.filter(p3=request.user)
    elif lev == 3:
        tr = trees.filter(p4=request.user)
    count = tr.count
    return count


def received_amount(request, lev):
    amt_rec = 0.00
    # rec = transaction.objects.filter(to=request.user, level=lev, timestamp__gte=request.user.dashboard.reset_date)
    rec = Transaction.objects.filter(to=request.user, level=lev)
    for r in rec:
        amt_rec = amt_rec + float(r.amount)
    return amt_rec

def sent_amount(request, lev):
    amt_snt = 0.00
    # snt = transaction.objects.filter(user=request.user, level=lev, timestamp__gte=request.user.dashboard.reset_date)
    snt = Transaction.objects.filter(user=request.user, level=lev)
    for s in snt:
        amt_snt = amt_snt + float(s.amount)
    return amt_snt

def total_amount(tp):
    print(tp)
    if tp == 'n':
        val = 3
    elif tp == 'p':
        val = 10
    elif tp == 'd':
        val = 100
    elif tp == 's':
        val = 10000
    max = val * ((1*0.002)+(3*0.003)+(9*0.02)+(27*0.45))
    return max


def view_notification(r):
    a = Action.objects.exclude(user=r.user)
    a = a[:5]
    b = ""
    state = r.GET.get("viewed")
    print(state)
    if Notif_Count.objects.filter(target=r.user).exists():
        b = Notif_Count.objects.get(target=r.user)
        if state:
            b.count = 0
            b.save()
    return a, b



@login_required(login_url='/login/')
def profile_index(request):
    profile = dashboard.objects.get(user=request.user)
    info = user_info.objects.get(user=request.user)
    sponsor = user_info.objects.get(user=profile.sponsor)
    sponsor_op = option.objects.get(user=profile.sponsor)
    joined = request.user.date_joined
    sent = Transaction.objects.filter(user=request.user)
    data = {}
    data['subject'] = 'welcome to fx to pay'
    data['message'] = 'hello ma friend this to f2kssfjh'
    mail = sendmail(profile, data)
    print('mail is '+str(mail))
    amt_sent = 0.00
    for s in sent:
        amt_sent = amt_sent + float(s.amount)
    received = Transaction.objects.filter(to=request.user)
    amt_rec = 0.00
    for r in received:
        amt_rec = amt_rec + float(r.amount)
    tr = tree.objects.all()
    actions, notif_count = view_notification(request)
    i, j = 0, 1
    amt = {
        'lev1': received_amount(request, 0),
        'lev2': received_amount(request, 1),
        'lev3': received_amount(request, 2),
        'lev4': received_amount(request, 4)
    }
    sent = {
        'lev1': sent_amount(request, 0),
        'lev2': sent_amount(request, 1),
        'lev3': sent_amount(request, 2),
        'lev4': sent_amount(request, 4)
    }

    lev = {
        'lev1': progress(request, 0 ),
        'lev2': progress(request, 1 ),
        'lev3': progress(request, 2 ),
        'lev4': progress(request, 3 )
    }
    # rate = get_btc_rate(request.user)
    context = {
        # 'rate': rate,
        's_option': sponsor_op,
        'profile': profile,
        'joined': joined,
        'info': info,
        'sponsor': sponsor,
        'sent':  amt_sent,
        'received': amt_rec,
        'l': lev,
        'a': amt,
        's': sent,
        'total': total_amount(profile.acc_type),
        'actions': actions,
        'notification': notif_count
    } 
    return render(request, 'profile/index.html', context)


@login_required(login_url='/login/')
def profile_settings(request):
    info = user_info.objects.get(user=request.user)
    imgForm = imageForm(request.POST or None, request.FILES or None, instance=info)
    msg = ""
    if imgForm.is_valid():
        img = imgForm.save(commit=False)
        print(imgForm.cleaned_data.get("user_image"))
        img.save()
    if not request.FILES:
        if request.POST or request.is_ajax:
            val = request.POST.get("value")
            name = request.POST.get("name")
            op = option.objects.filter(user=request.user)
            if name == 'show_soc':
                op.update(show_soc=val)
            elif name == 'autos':
                op.update(autosave=val)
            elif name == 'allowemail':
                op.update(allowemail=val)
            elif name == 'showpp':
                op.update(show_pp=val)
            elif name == 'shownum':
                op.update(show_num=val)
            faceb = request.POST.get('fb')
            twitt = request.POST.get('tw')
            gplus = request.POST.get('gp')
            linkn = request.POST.get('in')
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            country = request.POST.get('country')
            old_password = request.POST.get('old_password')
            password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')
            if old_password  and password and cpassword:
                if old_password:
                    if password:
                        if cpassword:
                            print("all entered")
                            u = User.objects.get(username=request.user.username)
                            valid = u.check_password(old_password)
                            if valid:
                                if password == cpassword:
                                    u.set_password(password)
                                    u.save()
                                    change = authenticate(username=request.user.username, password=password)
                                    login(request, change)
                                else:
                                    msg = "password confirmation did not match"
                                    print(msg)
                            else:
                                msg = " The current password you entered is wrong "
                                print(msg)
                        else:
                            msg = "You did not confirm your password"
                    else:
                         msg = "You did not enter any password"
                else:
                    msg = "Please enter your current password"
            # else:
            #     msg = "Fill the fields before submiting"
            if faceb:
                user_info.objects.filter(user=request.user).update(fb_link=faceb)
            if twitt:
                user_info.objects.filter(user=request.user).update(twi_link=twitt)
            if gplus:
                user_info.objects.filter(user=request.user).update(gm_link=gplus)
            if linkn:
                user_info.objects.filter(user=request.user).update(lin_link=linkn)
            if name:
                dashboard.objects.filter(user=request.user).update(name=name)
            if email:
                dashboard.objects.filter(user=request.user).update(email=email)
            if phone:
                dashboard.objects.filter(user=request.user).update(phone=phone)
            if country:
                dashboard.objects.filter(user=request.user).update(country=country)

    profile = dashboard.objects.get(user=request.user)
    op = option.objects.get(user=request.user)
    info_nw = user_info.objects.get(user=request.user)
    usr_sponsor = profile.sponsor
    joined = request.user.date_joined
    actions, notif_count = view_notification(request)
    context = {
        'profile': profile,
        'info': info_nw,
        'joined': joined,
        'option': op,
        'sponsor': usr_sponsor,
        'msg': msg,
        'actions': actions,
        'notification': notif_count

    }
    return render(request, 'profile/profile.html', context)


@login_required(login_url='/login/')
def ext_profile(request, name=None):
    profile = dashboard.objects.get(user=request.user)
    info = user_info.objects.get(user=request.user)
    extUser = User.objects.get(username=name)
    extUserProfile = get_object_or_404(dashboard, user=extUser)
    actions, notif_count = view_notification(request)
    context = {
        'profile': profile,
        'info': info,
        'ext': extUserProfile,
        'actions': actions,
        'notification': notif_count
    }
    return render(request, 'profile/ext-profile.html', context)

@login_required(login_url='/login/')
def testiment(request):
    testimony = Testiment.objects.all()
    profile = dashboard.objects.get(user=request.user)
    info = user_info.objects.get(user=request.user)
    actions, notif_count = view_notification(request)
    context = {
        'testimony': testimony,
        'profile': profile,
        'info': info,
        'actions': actions,
        'notification': notif_count
    }
    return render(request, 'profile/testimonial.html', context)


@login_required(login_url='/login/')
def new_test(request):
    profile = dashboard.objects.get(user=request.user)
    info = user_info.objects.get(user=request.user)
    if request.method == "POST":
        msg = request.POST.get("msg")
        if msg:
            Testiment.objects.create(user=request.user, msg=msg)
            return redirect("profile:testiment")
    actions, notif_count = view_notification(request)
    context = {
        'profile': profile,
        'info': info,
        'actions': actions,
        'notification': notif_count
    }
    return render(request, 'profile/add-test.html', context )


@login_required
def support(request):
    profile = dashboard.objects.get(user=request.user)
    info = user_info.objects.get(user=request.user)
    form = SupportForm(request.POST or None)
    print(form)
    if form.is_valid:
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
    else:
        form = SupportForm()
    actions, notif_count = view_notification(request)
    context = {
    'profile': profile,
    'info': info,
    'form': form,
    'actions': actions,
    'notification': notif_count
    }
    return render(request, 'profile/support.html', context )

@login_required
def news(request):
    actions, notif_count = view_notification(request)
    return render(request, 'profile/news.html', {})
