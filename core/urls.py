from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name ="index"),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    # path('setting_view/', views.setting_view, name='setting_view'),
    path('home/', views.home, name="home"),
    path('deposit/', views.deposit, name='deposit'),
    path('plans/', views.planview, name='planview'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('profile/', views.profile, name = 'profile'),
    path('contact/', views.contact_form, name = 'contact_form'),
    path('home_faq/', views.home_faq, name='home_faq'),
    path('faq/', views.faq, name='faq'),
    path('invest/', views.invest, name='invest'),
    # path('earning/', views.earning, name='earning'),

]


