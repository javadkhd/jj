import re

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
import sqlite3
from collections import defaultdict


def col_1():
    con = sqlite3.connect('db.sqlite3')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT دستگاه FROM Sheet۱ ')

    col1 = set(cursorObj.fetchall())
    col11 = list()
    for item in col1:
        col11.append(item[0].strip())
    # print(col11)

    return col11


def col_10(request):

    term = request.GET.get('term', None)
    strings = f'SELECT "شرح کد(Value)" FROM Sheet۱ WHERE "شرح کد(Value)" LIKE "%{term}%"'

    con = sqlite3.connect('db.sqlite3')
    cursorObj = con.cursor()
    cursorObj.execute(strings)
    explanations = cursorObj.fetchall()
    # print(explanations)

    return JsonResponse(
        {
            'explanations': explanations,
        }
    )




def nozad(request):
    """
    This view will send data to page
    """

    db_col_1 = col_1()

    return render(
        request=request,
        context={
            'db_col_1': db_col_1,
        },
        template_name='icd10/index.html'
    )
