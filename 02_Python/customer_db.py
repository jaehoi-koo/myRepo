##################
## SQL실행문 함수화
###############3##
import pymysql
import datetime from date

def select_customer_by_id(cust_id:int)->tuple|None:
    """
    고객 id로 고객정보를 DB에서 조회해서 반환
    Args:
    Returns:
    Raises:
    """
    sql = "SELECT * FROM customer WHERE id = %s" 
    with pymysql.connect(host="127.0.0.1", port=3306, user='playdata', password='1111', db='mydb') as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql,[cust_id])
            print("조회행수:", result)
            return cursor.fetchone()

def select_all_customer():
    """
    전체 고객 정보를 조회하는 함수
    SELECT * FROM customer
    """
    sql = "SELECT * FROM customer" 
    with pymysql.connect(host="127.0.0.1", port=3306, user='playdata', password='1111', db='mydb') as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql)
            print("조회행수:", result)
            return cursor.fetchall()

def update_customer(cust_id, name, email, tall, birthday):

    sql = (
        "UPDATE customer "
        "SET name=%s, email=%s, tall=%s, birthday=%s "
        "WHERE id=%s"
    )
    with pymysql.connect(host="127.0.0.1", port=3306, user='playdata', password='1111', db='mydb') as conn:
        with conn.cursor() as cursor:
            result = cursor.execute(sql,(name, email, tall, birthday, cust_id))
            conn.commit()
            return result

