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

    query_text = f'SELECT "کدملی(Code)" FROM Sheet۱ WHERE "شرح کد(Value)" LIKE "%{explanation}%"'

    cursorObj.execute(query_text)
    orginal_code = cursorObj.fetchall()

    akbar = set()
    akbar.add(orginal_code[0][0])

    query_text = f'SELECT توضیحات FROM Sheet۱ WHERE "شرح کد(Value)" LIKE "%{explanation}%"'

    cursorObj.execute(query_text)
    description = cursorObj.fetchall()
    description = description[0][0]

    if description:
        reg1 = re.findall(r"(\d{6})", description)  # adad haye tak ra peydamikonad
        reg1 = list(map(int, reg1))
        reg2 = re.findall(r"(\d{6}) تا (\d{6})", description)  # exp : 100010 ta 100020
        reg2 = list(map(int, reg2))
        reg3 = re.findall(r"(\d{6})\s*-\s*(\d{6})", description)  # exp : 100010-100020
        reg3 = list(map(int, reg3))
        reg4 = re.findall(r"(\d{6}) به بعد", description)  # be baad
        reg4 = list(map(int, reg4))

        # print(reg2)
        # print(type(reg2))
        # print(type(reg2[0]))


        if reg1:
            for i in reg1:
                akbar.add(i)

        if reg2:
            for i in range(min(reg2), max(reg2)):
                akbar.add(i)

        if reg3:
            for i in range(min(reg3), max(reg3)):
                akbar.add(i)

        if reg4:
            for i in range(reg4[0], reg4[0] + 10):
                akbar.add(i)

    print(akbar)

    descriptions = list()
    for i in akbar:
        query_text = f'SELECT "شرح کد(Value)" FROM Sheet۱ WHERE "کدملی(Code)" LIKE "%{i}%"'

        cursorObj.execute(query_text)
        descriptions.append(cursorObj.fetchall())

    return JsonResponse(
        {
            'descriptions': descriptions,
        }
    )


def col_12(request):
    explanation = request.GET.get('explanation', None)
    explanation = explanation.split()
    explanation.remove('Select')
    explanation = " ".join(explanation)

    con = sqlite3.connect('db.sqlite3')
    cursorObj = con.cursor()

    query_text = f'SELECT "کدملی(Code)" FROM Sheet۱ WHERE "شرح کد(Value)" LIKE "%{explanation}%"'

    cursorObj.execute(query_text)
    code = cursorObj.fetchall()

    return JsonResponse(
        {
            'code': code,
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
