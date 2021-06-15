"""nozad URL Configuration

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
from django.urls import path, include

from icd10.views import nozad, col_10, col_11

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', nozad), #, name='nozad'
    path('col10/', col_10), #, name='nozad'
    path('col11/', col_11), #, name='nozad'
    # path('col12/', col_12), #, name='nozad'
    # path('icd10/', include('icd10.urls'))


    # path(r'^ajax_calls/search/', autocomplete),

    # path('blog/', include('blog.urls')),
    # path('users/', include('users.urls')),
    # path('', show_all_posts, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
