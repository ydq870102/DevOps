# -*- coding:utf-8 -*-
# !/usr/bin/env python
# Time 18-7-3
# Author Yo
# Email YoLoveLife@outlook.com
import redis
import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import Response, status
from rest_framework.views import APIView
from django_redis import get_redis_connection
from deveops.api import WebTokenAuthentication
from django.conf import settings
from manager.models import Group

__all__ = [
    "DashboardCountAPI", "DashboardGroupAPI", "DashboardWorkAPI",
]


class DashboardCountAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        conn = get_redis_connection('dashboard')
        TEMP = conn.hgetall('COUNT',)
        COUNT = {}
        for key in TEMP:
            COUNT[str(key, encoding='utf-8')] = TEMP[key]
        return Response(
            COUNT or {}, status.HTTP_200_OK
        )


class DashboardWorkAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        conn = get_redis_connection('dashboard')
        week_list = [b'Won', b'Tue', b'Wed', b'Thur', b'Fri', b'Sat', b'Sun',]
        TEMP = conn.hgetall('WORK',)
        WORK = []
        for key in week_list:
            WORK.append({
                'time': str(key, encoding='utf-8'),
                '执行次数': TEMP[key]
            })
        return Response(
            {'title': '一周内工单执行', 'dataset': WORK} or {}, status.HTTP_200_OK
        )


class DashboardGroupAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        conn = get_redis_connection('dashboard')
        TEMP = conn.hgetall('GROUP',)
        GROUP = [
            ['主机数目','count'],
        ]
        for key in TEMP:
            GROUP.append([str(key, encoding='utf-8'), int(TEMP[key])])
        return Response(
            {'title': '主机统计', 'dataset': GROUP} or {}, status.HTTP_200_OK
        )


class DashboardGroupRandomLoadAPI(WebTokenAuthentication, APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        conn = get_redis_connection('dashboard')
        group = Group.objects.order_by('?')[:1].get()
        results = conn.get('GROUP'+str(group.uuid))
        if results is not None:
            return Response(
                {
                    'data': json.loads(str(results, encoding='utf-8')),
                    'group': group.name
                } or {},
                status.HTTP_200_OK
            )
        else:
            return Response({
                'data': '',
                'group': '',
            }, status.HTTP_404_NOT_FOUND)


class DashboardWorkOrderAPI(WebTokenAuthentication, APIView):
    permission_classes = [AllowAny, ]

    def get(self, request, *args, **kwargs):
        conn = get_redis_connection('dashboard')
        get_dict = dict()

        if conn.exists('WORKORDER_COUNT') and conn.exists('REPOSITORY_COUNT') \
            and conn.exists('WORKORDER_LAST') and conn.exists('MONTHS_COUNT') and 0:

            WORKORDER_COUNT = conn.get('WORKORDER_COUNT')
            get_dict['count'] = json.loads(WORKORDER_COUNT)

            REPOSITORY_COUNT = conn.get('REPOSITORY_COUNT')
            get_dict['repository'] = json.loads(REPOSITORY_COUNT)

            WORKORDER_LAST = conn.get('WORKORDER_LAST')
            get_dict['workorder'] = json.loads(WORKORDER_LAST)

            MONTHS_COUNT = conn.get('MONTHS_COUNT')
            get_dict['months'] = json.loads(MONTHS_COUNT)

            TIMELINES = '[]'#conn.get('TIMELINES')
            get_dict['timelines'] = json.loads(TIMELINES)
        else:
            get_dict = {
                'timelines': [],
                'count': {},
                'repository': [],
                'workorder': [],
                'months': [],
            }

        return Response(
            get_dict or {}, status.HTTP_200_OK
        )
