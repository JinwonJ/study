from django.shortcuts import render, get_object_or_404
from django.db import connection
from .models import Book

# Create your views here.
def BookListView(request):
    # books = Book.objects.all()
    try:
        cursor = connection.cursor()

        strSql = "SELECT code, name, author FROM bookstore_book"
        result = cursor.execute(strSql)
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        books = []
        for data in datas:
            row = {'code': data[0],
                   'name': data[1],
                   'author': data[2]}

            books.append(row)

    except:
        connection.rollback()
        print("Failed selecting in BookListView")


    return render(request, 'book_list.html', {'books': books})



def BookDetailView(request, code):
    # book1 = get_object_or_404(Book, code=code)
    # book2 = Book.objects.get(code=code)

    try:
        cursor = connection.cursor()

        strSql = "SELECT code, name, author, price, url FROM bookstore_book WHERE code = (%s)"
        result = cursor.execute(strSql, (code,))
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        book = {'code': datas[0][0],
                'name': datas[0][1],
                'author': datas[0][2],
                'price': datas[0][3],
                'url': datas[0][4]}

    except:
        connection.rollback()
        print("Failed selecting in BookListView")


    return render(request, 'book_detail.html', {'book': book})