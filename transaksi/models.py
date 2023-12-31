from django.db import models
from django.contrib.auth.models import User as user_root
from kelas.models import Program, Langganan

class Withdrow(models.Model):
    user        = models.ForeignKey(user_root,blank=True, null=True, on_delete=models.CASCADE, related_name="user_withdrow")
    jumlah      = models.IntegerField(default=0)
    bank        = models.CharField(max_length=30)
    no_bank     = models.CharField(max_length=18)
    penerima    = models.CharField(max_length=50)
    tgl         = models.DateField(auto_now_add=False)
    approve     = models.BooleanField(default=False)
    def __str__(self):
        return "{}.{}".format(self.user, self.jumlah)
    
class Transaksi(models.Model):
    user        = models.ForeignKey(user_root,blank=True, null=True, on_delete=models.CASCADE, related_name="pendapatan_user")
    program     = models.ForeignKey(Program,blank=True, null=True, on_delete=models.CASCADE, related_name="room")
    langganan   = models.ForeignKey(Langganan,blank=True, null=True, on_delete=models.CASCADE, related_name="Langganan")
    tgl         = models.DateField(auto_now_add=False)
    jumlah      = models.IntegerField()
    terbayar    = models.BooleanField(default=False)
    terpakai    = models.BooleanField(default=False)
    trx_id      = models.IntegerField(default=0)
    via         = models.CharField(max_length=50, null=True)
    status      = models.CharField(max_length=50, null=True)
    SessionID   = models.CharField(max_length=50)
    def __str__(self):
        return "{}.{}".format(self.user, self.tgl)
    
class TransaksiGuru(models.Model):
    user        = models.ForeignKey(user_root,blank=True, null=True, on_delete=models.CASCADE, related_name="pendapatan_guru")
    jumlah      = models.IntegerField()
    transaksi   = models.ForeignKey(Transaksi,blank=True, null=True, on_delete=models.CASCADE, related_name="transaksi_guru")
    tgl         = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{}.{}".format(self.user, self.tgl)
    
class TransaksiOwner(models.Model):
    jumlah      = models.IntegerField()
    transaksi   = models.ForeignKey(Transaksi,blank=True, null=True, on_delete=models.CASCADE, related_name="transaksi_owner")
    tgl         = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{}.{}".format(self.jumlah, self.tgl)
    
class TransaksiDeveloper(models.Model):
    jumlah      = models.IntegerField()
    transaksi   = models.ForeignKey(Transaksi,blank=True, null=True, on_delete=models.CASCADE, related_name="transaksi_developer")
    tgl         = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "{}.{}".format(self.jumlah, self.tgl)
    
class Promo(models.Model):
    kode        = models.CharField(max_length=224)
    potongan    = models.IntegerField(default=0)
    by          = models.CharField(max_length=224)
    banner      = models.CharField(max_length=224)
    def __str__(self):
        return "{} by {}".format(self.by, self.kode)

#keranjang untuk semua layanan
class Cart(models.Model):
    user        = models.ForeignKey(user_root, blank=True, null=True,on_delete=models.CASCADE, related_name="user_cart_user")
    kelas       = models.ForeignKey(Program,blank=True, null=True,on_delete=models.CASCADE, related_name="cart_kelas")
    promo       = models.ForeignKey(Promo, blank=True, null=True, on_delete=models.CASCADE, related_name="cart_promo")
    bukti       = models.FileField(upload_to='media/bukti', blank=True)
    approve     = models.BooleanField(default=False)
    favorite    = models.BooleanField(default=False)
    tgl         = models.DateField(auto_now_add=True)
    def __str__(self):
        return "{} take {}".format(self.user, self.kelas)
    



