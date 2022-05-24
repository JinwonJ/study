from django.shortcuts import render
from django.db import connection

# Create your views here.
def MainView(request):
    try:
        cursor = connection.cursor()

        strSql = "SELECT DISTINCT(c_code), c_name"
        strSql += " FROM category"
        result = cursor.execute(strSql)
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        categories = []
        for data in datas:
            row = {'c_code': data[0],
                   'c_name': data[1],}

            categories.append(row)

    except:
        connection.rollback()
        print("Failed selecting in MainView")


    render_page = "main.html"
    return render(request, render_page, {"categories": categories,})



def ProductListView(request, c_code):
    try:
        cursor = connection.cursor()

        strSql = "SELECT c_name"
        strSql += " FROM category"
        strSql += " WHERE c_code = (%s)"
        result = cursor.execute(strSql, (c_code,))
        datas = cursor.fetchall()
        c_name = datas[0][0]


        strSql = "SELECT p.p_id, p.p_name, p.img_src, p.price"
        strSql += " FROM product p"
        strSql += " JOIN category c ON c.c_id = p.c_id"
        strSql += " WHERE c.c_code = (%s)"
        result = cursor.execute(strSql, (c_code,))
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        products = []
        for data in datas:
            row = {'p_id': data[0],
                   'p_name': data[1],
                   'img_src': data[2],
                   'price': data[3],}

            products.append(row)

    except:
        connection.rollback()
        print("Failed selecting in ProductListView")


    render_page = "product_list.html"
    return render(request, render_page, {'c_name': c_name, 'products': products,})



def ProductDetailView(request, p_id):
    try:
        cursor = connection.cursor()

        strSql = "SELECT c.c_name, c.i_name, p.p_id, p.p_name, p.img_src, p.price, p.link"
        strSql += " FROM product p"
        strSql += " JOIN category c ON c.c_id = p.c_id"
        strSql += " WHERE p.p_id = (%s)"
        result = cursor.execute(strSql, (p_id,))
        datas = cursor.fetchall()

        connection.commit()
        connection.close()

        product = {'c_name': datas[0][0],
                   'i_name': datas[0][1],
                   'p_id': datas[0][2],
                   'p_name': datas[0][3],
                   'img_src': datas[0][4],
                   'price': datas[0][5],
                   'link': datas[0][6],}


    except:
        connection.rollback()
        print("Failed selecting in ProductListView")


    render_page = "product_detail.html"
    return render(request, render_page, {'product': product})