from extra.utils import create_action
from geneology.views import get_upliner
from .models import Transaction


def confirm_transaction(t):
    t.state = "confirmed"
    t.save()
    check_missed(t)
    make_upgrade(t.amount, t.user.dashboard, t.to) 
    return True
    # if t.user.option.allowemail == True:
    #     context = {
    #                 user: t.user,
    #                 to: t.to,
    #                 level: t.user.dashboard.level
    #               }
    #     sendmail(t.user, msgContent["confirmed"], context)



def check_missed(transaction):
    true_parent = get_upliner(transaction.level, transaction.user)
    if not true_parent == transaction.to:
        missed.objects.create(
                user=transaction.user,
                was_to=true_parent,
                missed_to=transaction.to,
                trans_id=transaction.trans_id,
                amount=transaction.amount
                )

def get_total_amount(i, r):
    same_transaction = Transaction.objects.filter(user=i.user, to=r)
    if same_transaction:
        total_amount = 0.00
        for sm in same_transaction:
            total_amount = total_amount + float(sm.amount)
        return total_amount
    return False

def good_transaction(i, r):
    valid_amount = amount_to_send(i.level)
    total_amount = get_total_amount(i, r)
    # print('total made is '+ str(total_amount) +' line 42')
    if total_amount:
        if total_amount == valid_amount:
            return 'equal'
        elif total_amount < valid_amount:
            return 'less'
        else:
            return 'more'
    return False


def make_upgrade(amount, instance, receiver):
    good = good_transaction(instance, receiver)
    if good == 'equal' or good == 'more' :
        instance.level = instance.level + 1
        instance.save()
        create_action(user=receiver, target=instance.user, verb="message", extra="done_upgrade")
    # elif good == 'less':
    #     print("upgrade failing confirmed redo upgrade")
    #     create_action(user=receiver, target=instance.user, verb="message", extra="redo_upgrade")
    #     print('action created')
    #     valid_amount = amount_to_send(instance.level)
    #     total_amount = get_total_amount(instance, receiver)
    #     redo_amount(valid_amount, total_amount, instance.level)


def all_good(instance, receiver):
    good = good_transaction(instance, receiver)
    # print ('transaction is ' + str(good)+' line 70')
    a = get_total_amount(instance, receiver)
    l = instance.level
    v = amount_to_send(l)
    if good == 'less':
        amount = float(v)- float(a)
        return amount
    else:
        return v

def redo_amount(v, a, l):
    amount = float(v)- float(a)
    am = amount_to_send(l, amount)
    return am

def amount_to_send(level, amt=None):
    if amt:
        amount = amt
    else:
        amount = ""
        if level == 0:
            amount = 10.00
        elif level == 1:
            amount = 15.00
        elif level == 2:
            amount = 50.00
        elif level == 3:
            amount = 100.00
    return amount
