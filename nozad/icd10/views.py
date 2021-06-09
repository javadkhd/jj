from django.shortcuts import render, redirect, get_object_or_404

from django.db import connection
import sqlite3


def sql_fetch(con):
    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM Sheet۱')

    rows = cursorObj.fetchall()

    for row in rows[:10]:
        print(row)
    return rows[:10]


def nozad(request):
    """
    This view will send data to page
    """

    con = sqlite3.connect('nozad.db')

    rows = sql_fetch(con)

    col = "111111111111"

    db_col_1 = rows[:10]
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
