# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import HttpResponse, render, get_object_or_404, Http404
from django.core.exceptions import PermissionDenied


def solution(request, solution_id):

    return HttpResponse('OK')
