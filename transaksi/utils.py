from transaksi.models import Transaksi, TransaksiDeveloper, TransaksiOwner
from akun.models import Users
from config.models import Setting
import midtransclient
import requests
import base64
from datetime import datetime

setting = Setting.objects.all().first()

server_key = "SB-Mid-server-dY0SSXtJamUYuoMTM2Uy3fr7"
snap = midtransclient.Snap( is_production=False,server_key=server_key)

def purchase(user, program=None, premium=None, tgl=datetime.now()):
    try:
        jumlah = program.discount if program else premium.diskon
        transaksi = Transaksi.objects.create(user=user, program=program, jumlah=program.discount, tgl=tgl) if program else Transaksi.objects.create(user=user, langganan=premium, jumlah=premium.diskon, tgl=tgl)
        TransaksiOwner.objects.create(jumlah=jumlah * setting.komisi_owner / 100, transaksi=transaksi)
        TransaksiDeveloper.objects.create(jumlah=jumlah * setting.komisi_developer / 100, transaksi=transaksi)
        return transaksi
    except Exception as e:
        print(e)
        return False

def midtrans(request, gross_amount, order_id):
    param = {
        "transaction_details": {"order_id": order_id,"gross_amount": gross_amount},
        "credit_card":{"secure" : True},
        "customer_details":{"first_name": request.user.first_name,"last_name": request.user.last_name,"email": request.user.email,"phone": Users.objects.get(user=request.user).phone}
    }
    transaction = snap.create_transaction(param)
    return transaction['redirect_url'], transaction['token']

def status(order_id):
    auth_string = base64.b64encode(f"{server_key}:".encode()).decode()
    url = f'https://api.sandbox.midtrans.com/v2/{order_id}/status'
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_string}"
    }
    return requests.get(url, headers=headers).json()
