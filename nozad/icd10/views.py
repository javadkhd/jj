from django.shortcuts import render, redirect, get_object_or_404

from django.db import connection
import sqlite3


def sql_fetch():
    con = sqlite3.connect('nozad.db')
    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM Sheet۱ where ')

    db = cursorObj.fetchall()

    return db


def col_1():

    db = sql_fetch()

    col_1 = set()
    for row in db:
        col_1.add(row[1])

    return col_1

def col_2(str):

    db = sql_fetch()
    col1 = col_1()

    if str in col1:

        col_2 = set()
        for row in db:
            col_1.add(row[2])

        return col_1



def nozad(request):
    """
    This view will send data to page
    """



    col1 = col_1()
    print(col1)

    col = "111111111111"

    db_col_1 = col1
    # db_col_2 =
    # db_col_3 =
    return render(
        request=request,
        context={
            'db_col_1': db_col_1,
            # 'db_col_2': db_col_2,
            # 'db_col_3': db_col_3,
        },
        template_name='icd10/index.html'
    )
