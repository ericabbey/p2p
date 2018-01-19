import qrcode
import qrcode.image.svg
from hashlib import sha256
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from dashboard.views import view_notification
from dashboard.models import dashboard, user_info, option
from extra.utils import create_action
from geneology.views import get_auth_upliner, get_upliner
from .forms import WalletForm, ProofData
from. helpers import all_good, good_transaction, amount_to_send, confirm_transaction
from .models import MomoData, Transaction, Missed, Report





@login_required(login_url='/login/')
def stats(request):
    profile = dashboard.objects.get(user=request.user)
    info = user_info.objects.get(user=request.user)
    trans = Transaction.objects.all

    # pending = Transaction.objects.filter(Q(user=request.user)|Q(to=request.user), state="pending", timestamp__gte=profile.reset_date)
    # miss = Missed.objects.filter(was_to=request.user,  timestamp__gte=profile.reset_date)

    miss = Missed.objects.filter(was_to=request.user)
    actions, notif_count = view_notification(request)
    context = {
    'profile': profile,
    'info': info,
    'trans': trans,
    'missed': miss,
    'actions': actions,
    'notification': notif_count
    }
    return render (request, 'profile/stats.html', context )


@login_required(login_url='/login/')
def wallet(request):
    profile = dashboard.objects.get(user=request.user)
    info = user_info.objects.get(user=request.user)
    form = WalletForm(request.POST or None)
    addr_count = MomoData.objects.get(user=request.user).changeCount
    msg = ""
    data = ""
    if request.method == "POST":
        if form.is_valid:
            password = request.POST.get("password")
            number = request.POST.get("number")
            name = request.POST.get("name")
            encoded = request.user.password
            pwd_valid = check_password(password, encoded)
            if pwd_valid:
                user_momo = MomoData.objects.filter(user=request.user)
                # b = btcAddr.objects.filter(user=request.user)
                if addr_count == 0:
                    addr_count = 1
                    user_momo.update(momo_name=name, momo_number=number, changeCount=addr_count)
                    data = "New Mobile Moble added successfully"
                else:
                    addr_count = addr_count + 1
                    user_momo.update(momo_name=name, momo_number=number, changeCount=addr_count)
                    data = "Mobile Money updated successfully"

            else:
                msg = "password invalid"
                form = WalletForm()
    momo = MomoData.objects.filter(user=request.user)
    actions, notif_count = view_notification(request)
    context = {
    'profile': profile,
    'info': info,
    'msg': msg,
    'momo': momo,
    'data': data,
    'actions': actions,
    'notification': notif_count
    }
    return render (request, 'profile/wallet.html', context )

# Will change this some page later on
@login_required(login_url='/login/')
def upgrade(request):
    profile = dashboard.objects.get(user=request.user)
    info = user_info.objects.get(user=request.user)
    op = option.objects.filter(user=request.user)
    upline = get_auth_upliner(profile.level, request)
    addr = MomoData.objects.filter(user=upline)
    proofData = ProofData(request.POST or None, request.FILES or None)
    pending_transaction = Transaction.objects.filter(to=request.user, state='pending', level=profile.level).count()
    print (pending_transaction)
    if proofData.is_valid():
        data = proofData.save(commit=False)
        image_proof = proofData.cleaned_data.get('image_proof')
        text_proof = proofData.cleaned_data.get('text_proof')
        if(image_proof != None or text_proof != None):
            amount = amount_to_send(profile.level)
            Transaction.objects.create(user=request.user, to=upline, text_proof=text_proof, level=profile.level, amount=amount, state="pending")
            create_action(user=upline, target=profile.user, verb="message", extra="pending")
    if addr:
        addr = MomoData.objects.get(user=upline)
    if request.GET.get('report'):
        get_transaction = Transaction.objects.get(user=request.user, to=upline, level=profile.level)
        
        obj, created = Report.objects.get_or_create(by=request.user, against=upline, trans_id=get_transaction)
        msg = 1
        if obj:
            msg = 0
        responseData = {
            'msg': msg
        }
        return JsonResponse(responseData)
    if request.POST.get('confirm'):
        ref = request.POST.get('confirm')
        print(type(ref))
        confirmed_transaction = Transaction.objects.get(id=ref)
        result = confirm_transaction(confirmed_transaction)
        responseData = {
            'msg': result
        }
        return JsonResponse(responseData)

    if request.method == "POST":
        if request.is_ajax():
            val = request.POST.get("value")
            name = request.POST.get("name")
            if name == 'dsd':
                op.update(dsd=val) 
            elif name == 'dsi': 
                op.update(dsi=val)
        # else:
        #     transac = request.POST.get("trid")
        #     amount = request.POST.get("amnt")
        #     transaction.objects.create(user=request.user, to=upline, trans_id=transac, amount=amount,level=profile.level, state="pending")
        #     create_action(user=upline, target=profile.user, verb="message", extra="pending")
        #     if op.allowemail == True:
        #         context = {
        #                     user: profile.user,
        #                     to: upline,
        #                     level: profile.level
        #                   }
        #         sendmail(profile.user, msgContent["pending"], context)
        #     return redirect('profile:index')
    nxt_level = profile.level + 1
    actions, notif_count = view_notification(request)
    profile = dashboard.objects.get(user=request.user)
    payment_made =  Transaction.objects.filter(user=request.user, state='pending', level=profile.level).count()
    print(payment_made)
    context = {
    'profile': profile,
    'info': info,
    'address':addr,
    'payment_made': payment_made,
    'ops':op,
    'nxt_level': nxt_level,
    'upliner': upline,
    'amount': all_good(profile, upline),
    'actions': actions,
    'notification': notif_count,
    'pending_transaction': pending_transaction
    }
    return render (request, 'profile/upgrade.html', context )
