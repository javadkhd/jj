from django.shortcuts import render, redirect, get_object_or_404

from django.db import connection


def nozad(request):
    """
    This view will send data to page
    """
    cursor = connection['nozad.db'].cursor()

    col = cursor.execute("SELECT index FROM Sheet۱").fetchall()


    # cursor = connections['db.sqlite3'].cursor()

    # db = connection.
    db_col_1 = col
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
