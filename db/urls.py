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
router = DefaultRouter(trailing_slash=False)
from django.urls import include


from db.views import TotalUnit, InsertData,FetchAllData,DataGraphPlotter,DataFilterGraphPlotter,Last24HoursData

router.register(r"total-unit", TotalUnit, basename="totalunit")
router.register(r"daily-unit", Last24HoursData, basename="dailyunit")
router.register(r"insert-data", InsertData, basename="insertdata")
router.register(r"fetch-all", FetchAllData, basename="fetchall")
router.register(r"plot-graph", DataGraphPlotter, basename="plotgraph")
router.register(r"plot-filter-graph", DataFilterGraphPlotter, basename="plotfiltergraph")

urlpatterns = [
    path(r"", include(router.urls)),
]
