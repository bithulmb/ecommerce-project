"""pawsomepetproducts URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user_home.urls")),  # redirecting to user_home app urls
    path("", include("product.urls")),  # redirecting to product app urls
    path("", include("accounts.urls")),  # redirecting to accounts app urls
    path("", include("customadmin.urls")),  # redirecting to customadmin app urls
    path(
        "accounts/", include("allauth.urls")
    ),  # for including social authentication urls
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # for including media files
