# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render, get_object_or_404, Http404
from django.core.exceptions import PermissionDenied
from django.views.generic import View
from ..models import *
from ..forms import *


class TopicView(View):

    def get(self, request, **kwargs):
        return HttpResponse('OK')
