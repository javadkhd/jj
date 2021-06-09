from django.shortcuts import render, redirect, get_object_or_404

from django.db import connection
import sqlite3


def col_1():
    con = sqlite3.connect('nozad.db')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT دستگاه FROM Sheet۱ ')

    col1 = set(cursorObj.fetchall())

    return col1


def col_2(value2):

    con = sqlite3.connect('nozad.db')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT "سرفصل خدمتی" FROM Sheet۱ where دستگاه = "%s"'%(value2))


    col2 = set(cursorObj.fetchall())

    return col2


def col_3(value2, value3):
    con = sqlite3.connect('nozad.db')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT "گروه خدمتی" FROM Sheet۱ where دستگاه = "%s" and "سرفصل خدمتی" = "%s" ' % (value2, value3))

    col3 = set(cursorObj.fetchall())

    return col3

def col_4():
    pass


def nozad(request):
    """
    This view will send data to page
    """

    db_col_1 = col_1()
    db_col_2 = col_2("پوست")
    db_col_3 = col_3("پوست", "پستان")

    return render(
        request=request,
        context={
            'db_col_1': db_col_1,
            'db_col_2': db_col_2,
            'db_col_3': db_col_3,
        },
        template_name='icd10/index.html'
    )
