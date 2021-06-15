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
    term = term.split()

    strings = 'SELECT "شرح کد(Value)" FROM Sheet۱ WHERE "شرح کد(Value)"'

    for word in term:
        strings += f' LIKE "%{word}%"'
        if word != term[-1]:
            strings += ' AND "شرح کد(Value)"'



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

def col_11(request):
    explanation = request.GET.get('explanation', None)
    explanation = explanation.split()
    explanation.remove('Select')
    explanation = " ".join(explanation)

    con = sqlite3.connect('db.sqlite3')
    cursorObj = con.cursor()

    query_text = f'SELECT توضیحات FROM Sheet۱ WHERE "شرح کد(Value)" LIKE "%{explanation}%"'


    cursorObj.execute(query_text)
    descriptions = cursorObj.fetchall()

    # print(descriptions)
    # if descriptions:
    #     descriptions.append(explanation)
    # print(descriptions)

    return JsonResponse(
        {
            'descriptions': descriptions,
        }
    )

# def col_12(request):
#     description = request.GET.get('description', None)
#     description = description.split()
#     description.remove('Select')
#     description = " ".join(description)
#     # print(description)
#     con = sqlite3.connect('db.sqlite3')
#     cursorObj = con.cursor()
#
#     query_text = f'SELECT توضیحات FROM Sheet۱ WHERE "شرح کد(Value)" LIKE "%{description}%"'
#
#
#     cursorObj.execute(query_text)
#     descriptions = cursorObj.fetchall()
#
#     return JsonResponse(
#         {
#             'descriptions': descriptions,
#         }
#     )



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


