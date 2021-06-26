import re
from urllib import parse
from pprint import pprint
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

    # print(akbar)

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


def col_13(request):
    data = request.GET.get('arr', None)
    data = list(set(re.findall(r"(\d{6})", data)))

    con = sqlite3.connect('db.sqlite3')
    cursorObj = con.cursor()

    my_dict = dict()

    for elem in data:
        my_dict[elem] = dict()

        query_text = f'SELECT توضیحات FROM Sheet۱ WHERE "کدملی(Code)" LIKE "%{elem}%"'
        cursorObj.execute(query_text)
        des = cursorObj.fetchall()
        my_dict[elem]['des'] = des[0][0]

        query_text = f'SELECT "شرح کد(Value)" FROM Sheet۱ WHERE "کدملی(Code)" LIKE "%{elem}%"'
        cursorObj.execute(query_text)
        expl = cursorObj.fetchall()
        my_dict[elem]['expl'] = expl[0][0]

    # pprint(my_dict)
    del data

    my_list = list()
    for k, v in my_dict.items():

        expl = v['expl']
        des = v['des']

        if des == None:
            des = ""

        if ("(عمل مستقل)" in expl) or ("کد ديگري" in des):
            if len(my_dict.keys()) > 1:
                report = f"کد {k} همراه با کد دیگری قابل قبول نیست."

                my_list.append(report)

        if "به جز کد" in des:
            pattern3 = r"\(به جز کد (\d{6})\)"
            num = re.findall(pattern3, des)
            if num not in my_dict.keys():
                report = f"کد {k} همراه با کد انتخابی قابل قبول نیست."
                my_list.append(report)

        if des:

            ###########################
            pattern1 = r"(\(این کد.*\d{6}.*نمی‌باشد\))"
            # print(des)
            new_des = re.findall(pattern1, des)
            # print(new_des)
            if new_des:
                new_des = new_des[0]
            else:
                new_des = ""

            nums = re.findall(r"(\d{6})", new_des)

            if any(i in my_dict.keys() for i in nums):
                report = f"کد {k} با کد یا کدهای {nums} تداخل دارد."

                my_list.append(report)

            ###########################
            pattern2 = r"گزارش نگردد"
            if re.findall(pattern2, des):

                nums = re.findall(r"(\d{6})", new_des)

                if any(i in my_dict.keys() for i in nums):
                    report = f"کد {k} با کد یا کدهای {nums} تداخل دارد."

                    my_list.append(report)

            ###########################

    del my_dict

    if not my_list:
        my_list = 200

    return JsonResponse(
        {
            'status_code': my_list,
        }
    )


from .models import Icd10


def col_14(request):
    first_name = request.GET.get('first_name', None)
    # print(type(first_name))
    last_name = request.GET.get('last_name', None)
    # print(last_name)
    doctor_name = request.GET.get('doctor_name', None)
    # print(doctor_name)
    national_code = request.GET.get('national_code', None)
    # print(national_code)
    codes = request.GET.get('codes', None)
    print(codes)
    print(type(codes))

    if not all([first_name, last_name, doctor_name, national_code, codes]):
        return JsonResponse(
            {
                'status_code': 400,
            }
        )
    asghar = Icd10.objects.create()
    asghar.first_name = first_name
    asghar.last_name = last_name
    asghar.doctorname = doctor_name
    asghar.nationalcode = national_code
    asghar.codes = codes
    asghar.save()

    return JsonResponse(
        {
            'status_code': 200,
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
