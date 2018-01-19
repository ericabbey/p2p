from urllib.request import urlopen
from financial.helpers import make_transaction
from financial.models import transaction as Transaction

from .model import Transaction


def check_confirmation():
    pending_transaction = Transaction.objects.filter(state="pending")
    pending_transaction = pending_transaction[:10]
    for pending in pending_transaction:
        block = urlopen(' https://blockchain.info/tx/'+trans_id+'?show_adv=false&format=json')
        block_height = block['block_height']
        block_count = urlopen('http://blockchain.info/q/getblockcount')
        num_of_confirms = block_count - block_height + 1
        if num_of_confirms == 3:
            make_transaction(pending)


def find_and_make_upgrade():
    
