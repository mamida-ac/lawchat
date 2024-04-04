"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from mcq_generator.views import mcq_generator
from legal_ilp_app.views import upload_file
from legal_ilp_app.views import home
from myapp.views import rasahome,send_message
urlpatterns = [
    path('admin/', admin.site.urls),
    path("chat", rasahome, name="rasahome"),
    path("send_message/", send_message, name="send_message"),
    path('',home,name='home'),
    path('mcq', mcq_generator, name='mcq_generator'),
    path('case',upload_file,name='upload_file')
    
]
