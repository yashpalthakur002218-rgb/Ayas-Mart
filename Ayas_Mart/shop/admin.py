from django.contrib import admin
from .models import Product

admin.site.register(Product)

# कंट्रोल रूम का नाम बदलने के लिए
admin.site.site_header = "Ayas Mart Admin"
admin.site.site_title = "Ayas Mart Control Room"
admin.site.index_title = "Welcome to Ayas Mart Shop Management"