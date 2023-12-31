from django.contrib import admin
from transaksi.models import Withdrow, Transaksi, TransaksiGuru, TransaksiOwner, TransaksiDeveloper, Promo, Cart

admin.site.register(Withdrow)
admin.site.register(Transaksi)
admin.site.register(TransaksiGuru)
admin.site.register(TransaksiOwner)
admin.site.register(TransaksiDeveloper)
admin.site.register(Promo)
admin.site.register(Cart)