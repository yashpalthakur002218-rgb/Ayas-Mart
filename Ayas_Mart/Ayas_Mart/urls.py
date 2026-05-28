from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),  # दुकान के सारे रास्ते यहाँ जुड़ गए
]

# यह जादुई लाइन ब्राउज़र में सामान की फोटो दिखाएगी
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    