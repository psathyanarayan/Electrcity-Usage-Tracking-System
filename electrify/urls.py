"""
URL configuration for electrify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.urls import include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.views.generic import TemplateView
# from django.contrib.auth.decorators import login_required
# from rest_framework.permissions import AllowAny
# from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path("api/db/", include("db.urls")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# if settings.ENABLE_DOCS:
#     urlpatterns += [path(
#         "api/openapi",
#         get_schema_view(
#             title="API",
#             description="Internal endpoints to support our  products",
#             version="0.0.0",
#             permission_classes=[AllowAny],
#         ),
#         name="openapi-schema",
#     ),
#     path('api/docs/', login_required(TemplateView.as_view(
#         template_name='swagger-ui.html',
#         extra_context={'schema_url': 'openapi-schema'}
#     ), login_url="api/admin"), name='swagger-ui'),
# ]
