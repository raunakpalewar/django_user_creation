from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('welcome/',views.welcome_page,name='welcome'),
    path('login/',views.login_page,name='login'),
    path('register/',views.register_page,name='register'),
    path('otpverify/',views.verifyotp,name='otpverify'),
    path('profilepage/',views.profile_page,name='profile'),
    path('logout/',views.logout_view,name='logout')
] +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 