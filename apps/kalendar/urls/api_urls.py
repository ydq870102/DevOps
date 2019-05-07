# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
from django.urls import path
from .. import api as KalendarAPI
urlpatterns = [
    # Resource kalendar api
    path(r'v1/days/', KalendarAPI.KalendarDaysAPI.as_view()),
    path(r'v1/<str:year>/<str:month>/<str:day>/list/', KalendarAPI.KalendarListAPI.as_view()),
    path(r'v1/create/', KalendarAPI.KalendarCreateAPI.as_view()),
    path(r'v1/<uuid:pk>/update/', KalendarAPI.KalendarUpdateAPI.as_view()),
    path(r'v1/<uuid:pk>/delete/', KalendarAPI.KalendarDeleteAPI.as_view()),
]
