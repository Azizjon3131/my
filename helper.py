from django.shortcuts import render
import requests
import psycopg2
import psycopg2.extras
from catalog.models import Orders,Orders_product

class DbHelper:

    def category(self,id):
        response=requests.get(f'http://127.0.0.1:8000/category/?id={id}')
        return response.json()

    def product2(self,id):
        response=requests.get(f'http://127.0.0.1:8000/product/?id={id}')
        return response.json()


    def category_parent(self):
        response=requests.get('http://127.0.0.1:8000/category-list1/')
        return response.json()

    def category_child(self,id):
        response=requests.get(f'http://127.0.0.1:8000/category-list2/?id={id}')
        if response.json()!=[]:
            return response.json()


    def product_type(self,id):
        button=[]
        response=requests.get(f'http://127.0.0.1:8000/category-product/?id={id}')
        data=response.json()
        for i in data:
            response=requests.get(f"http://127.0.0.1:8000/category-type/?id={i['product_type']}")
            type=response.json()
            button.append(type[0])
        return button

    def product(self,category_id,type_id):
        response = requests.get(f'http://127.0.0.1:8000/category-product/?id={category_id}')
        data=response.json()
        for i in data:
            if i['product_type']==type_id:
                return i

    def product_image(self,id):
        x={}
        response = requests.get(f'http://127.0.0.1:8000/category-image/?id={id}')
        data=response.json()
        for i in data:
            if i['is_main']==True:
                x=i
                break
        return x



class DbHelper2:

    def __init__(self):
        self.conn=psycopg2.connect(
            host="127.0.0.1",
            database="loyiha",
            user="postgres",
            password="root"
        )

        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def insert_data(self,price,prise,product_name,user_id):
        self.cur.execute(f"""
        INSERT INTO orders(price,prise,product_name,user_id)
        VALUES({price},{prise},'{product_name}',{user_id})
        """)
        self.conn.commit()

    def read_product(self,id):
        self.cur.execute(f"""
        SELECT * FROM orders WHERE user_id={id}
        """)
        rows=self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute(f"""
        DELETE FROM orders WHERE user_id={id}
        """)
        self.conn.commit()

    def remove_product(self, id):
        self.cur.execute(f"""
        DELETE FROM orders WHERE id={id}
        """)
        self.conn.commit()

    def catalog_contact_insert(self,location,contact):
        self.cur.execute(f"""
         INSERT INTO catalog_orders(location, phone_number)
            VALUES({location},{contact})
        """)
        self.conn.commit()

    def catalog_conta_insert(self,price_all,contact):
        self.cur.execute(f"""
        UPDATE catalog_orders SET price_all={price_all}  WHERE phone_number='{contact}';
        """)
        self.conn.commit()



    def insert_data2(self,price,prise,product_name,user,id):
        self.cur.execute(f"""
        INSERT INTO catalog_orders_product(price,prise,product_name,user_id,orders_id)
        VALUES({price},{prise},'{product_name}',{user}, {id})
        """)
        self.conn.commit()

    def read_orders_product(self,id):
        self.cur.execute(f"""
        SELECT * FROM orders WHERE user_id={id}
        """)
        rows=self.cur.fetchall()
        return rows

    def read_product_contact(self,id):
        self.cur.execute(f"""
        SELECT * FROM catalog_orders WHERE phone_number='{id}'
        """)
        row=self.cur.fetchone()
        return row
