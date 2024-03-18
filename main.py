import psycopg2

# удаление таблиц
def delete_relationship(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE clients CASCADE;
        DROP TABLE phone_numbers;
        """)

# создание таблиц
def create_relationship(conn):
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
               client_id SERIAL PRIMARY KEY,
               first_name VARCHAR(40) NOT NULL,
               last_name VARCHAR(40) NOT NULL,
               email VARCHAR(80) UNIQUE NOT NULL
        );
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers(
               phone_id SERIAL PRIMARY KEY,
               number CHAR(11) NOT NULL,
               client_id INTEGER NOT NULL,
               CONSTRAINT fk_client FOREIGN KEY(client_id) REFERENCES clients(client_id) ON DELETE CASCADE
        );
        """)
        conn.commit()  # фиксируем в БД

# добавление нового клиента
def entering_client_information(conn, current_first_name, current_last_name, currant_email):
    with conn.cursor() as cur:
        cur.execute("""
           INSERT INTO clients(first_name, last_name, email) 
           VALUES (%s, %s, %s) 
        RETURNING client_id, first_name, last_name, email;
        """, (current_first_name, current_last_name, currant_email))
        print(cur.fetchone())
        
# добавление телефона для существующего клиента
def entering_phone_number(conn, current_number, current_client_id):
    with conn.cursor() as cur:
        cur.execute("""
           INSERT INTO phone_numbers(number, client_id) 
           VALUES (%s, %s) 
        RETURNING phone_id, number, client_id;
        """, (current_number, current_client_id)) 
        print(cur.fetchone())

# изменение данных о клиенте
def change_client_information(conn, client_id, new_first_name=None, new_last_name=None, new_email=None):
    with conn.cursor() as cur:
        cur.execute("""
           UPDATE clients SET first_name=%s, last_name=%s, email=%s 
            WHERE client_id=%s
        RETURNING client_id, first_name, last_name, email;
        """, (new_first_name, new_last_name, new_email, client_id))
        print(cur.fetchone()[0])

# удаление телефона для существующего клиента
def delete_phone_number(conn, client_id, current_number):
    with conn.cursor() as cur:
        cur.execute("""
           DELETE FROM phone_numbers 
            WHERE client_id=%s AND number=%s 
        RETURNING client_id;
        """, (client_id, current_number))
        print('удалён телефон клиента с id:', cur.fetchone())

# удаление существующего клиента
def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
           DELETE FROM clients 
            WHERE client_id=%s 
        RETURNING client_id;
        """, (client_id,))
        print('удалён клиент с id', cur.fetchone())

# поиск клиента по его данным: имени, фамилии, email или телефону
def get_client(conn, current_first_name=None, current_last_name=None, currant_email=None, current_number=None):
    with conn.cursor() as cur:
        cur.execute("""
        SELECT p_n.client_id, first_name, last_name, email, number FROM clients c
          JOIN phone_numbers p_n ON c.client_id = p_n.client_id
         WHERE (first_name=%s AND last_name=%s AND email=%s) OR number=%s;
        """, (current_first_name, current_last_name, currant_email, current_number))
        return cur.fetchall()


with psycopg2.connect(database="clients_db", user="postgres", password="") as conn:
    # delete_relationship(conn)

    create_relationship(conn)

    # entering_client_information(conn, "Галина", "Белова", "gal_bel@gmail.com")
    # entering_client_information(conn, "Тимофей", "Валуев", "tim_val@gmail.com")
    # entering_client_information(conn, "Елена", "Пулак", "el_pul@gmail.com")
    # entering_client_information(conn, "Виктор", "Тен", "v_ten@gmail.com")
    # entering_client_information(conn, "Екатерина", "Шульман", "ek_best@gmail.com")
    # entering_client_information(conn, "Иван", "Ургант", "iv_urg@gmail.com")

    # entering_phone_number(conn, '89054871258', 1)
    # entering_phone_number(conn, '89854687156', 1)
    # entering_phone_number(conn, '89108864973', 2)
    # entering_phone_number(conn, '89053571210', 2)
    # entering_phone_number(conn, '89851274518', 3)
    # entering_phone_number(conn, '89151251417', 4)
    # entering_phone_number(conn, '89057014750', 4)
    # entering_phone_number(conn, '89153405281', 4)
    # entering_phone_number(conn, '89157457859', 5)
    # entering_phone_number(conn, '89857581012', 5)
    # entering_phone_number(conn, '89854861210', 6)

    # change_client_information(conn, 3, 'Елена', 'Валуева', 'el_val@yandex.ru')

    # delete_phone_number(conn, 4, '89151251417')
    # delete_phone_number(conn, 5, '89857581012')

    # delete_client(conn, 3)

    # required_client_1 = get_client(conn, "Галина", "Белова", "gal_bel@gmail.com")
    # print(required_client_1)

    # required_client_2 = get_client(conn, current_number='89108864973')
    # print(required_client_2)

    # required_client_3 = get_client(conn, current_number='89108864975')
    # print(required_client_3)

conn.close()