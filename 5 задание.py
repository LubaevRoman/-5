import psycopg2


from pprint import pprint


def create_db(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        name VARCHAR(40),
        lastname VARCHAR(40),
        email VARCHAR(40)
        );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phonenumbers(
        number VARCHAR(11) PRIMARY KEY,
        client_id INTEGER REFERENCES clients(id)
        );
    """)
    return


def delete_db(cur):
    cur.execute("""
        DROP TABLE clients, phonenumbers CASCADE;
        """)


def insert_tel(cur, client_id, tel):
    cur.execute("""
        INSERT INTO phonenumbers(number, client_id)
        VALUES (%s, %s)
        """, (tel, client_id))
    return client_id


def insert_client(cur, name=None, surname=None, email=None, tel=None):
    cur.execute("""
        INSERT INTO clients(name, lastname, email)
        VALUES (%s, %s, %s)
        """, (name, surname, email))
    cur.execute("""
        SELECT id from clients
        ORDER BY id DESC
        LIMIT 1
        """)
    id = cur.fetchone()[0]
    if tel is None:
        return id
    else:
        insert_tel(cur, id, tel)
        return id


def update_client(cur, id, name=None, surname=None, email=None):
    cur.execute("""
        SELECT * from clients
        WHERE id = %s
        """, (id, ))
    info = cur.fetchone()
    if name is None:
        name = info[1]
    if surname is None:
        surname = info[2]
    if email is None:
        email = info[3]
    cur.execute("""
        UPDATE clients
        SET name = %s, lastname = %s, email =%s 
        where id = %s
        """, (name, surname, email, id))
    return id


def delete_phone(cur, number):
    cur.execute("""
        DELETE FROM phonenumbers 
        WHERE number = %s
        """, (number, ))
    return number


def delete_client(cur, id):
    cur.execute("""
        DELETE FROM phonenumbers
        WHERE client_id = %s
        """, (id, ))
    cur.execute("""
        DELETE FROM clients 
        WHERE id = %s
       """, (id,))
    return id


def find_client(cur, name=None, surname=None, email=None, tel=None):
    if name is None:
        name = '%'
    else:
        name = '%' + name + '%'
    if surname is None:
        surname = '%'
    else:
        surname = '%' + surname + '%'
    if email is None:
        email = '%'
    else:
        email = '%' + email + '%'
    if tel is None:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
            LEFT JOIN phonenumbers p ON c.id = p.client_id
            WHERE c.name LIKE %s AND c.lastname LIKE %s
            AND c.email LIKE %s AND p.number like %s
            """, (name, surname, email, tel))
    return cur.fetchall()


if __name__ == '__main__':
    with psycopg2.connect(database="homewok5", user="LR",
                          password="1") as conn:
        with conn.cursor() as curs:            
            delete_db(curs)            
            create_db(curs)
            print("БД создана")    
            print("Добавлен клиент: ",
                  insert_client(curs, "0", "0000", "0000@gmail.com")) #БН
            print("Добавлен клиент: ",
                  insert_client(curs, "1", "0001",
                                "0001@gmail.com", 0001))
            print("Добавлен клиент: ",
                  insert_client(curs, "2", "0002",
                                "0002@gmail.com", 0002))
            print("Добавлен клиент: ",
                  insert_client(curs, "3", "0003",
                                "0003@gmail.com", 0003))
            print("Добавлена клиент: ",
                  insert_client(curs, "4", "0004", "0004@gmail.com"))#БН
            print("Данные в таблицах")
            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            pprint(curs.fetchall())             
            print("Телефон добавлен клиенту: ",
                  insert_tel(curs, 2, 0007)) 
            print("Телефон добавлен клиенту: ",
                  insert_tel(curs, 1, 0009))
            
            print("Данные в таблицах")
            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            pprint(curs.fetchall())
            print("Изменены данные клиента №*: ",
                  update_client(curs, 4, "0004", None, '0004@outlook.com'))            
            print("Телефон удалён c номером: ",
                  delete_phone(curs, '0009'))
            print("Данные в таблицах")
            curs.execute("""
                SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                LEFT JOIN phonenumbers p ON c.id = p.client_id
                ORDER by c.id
                """)
            pprint(curs.fetchall())
            print("Клиент №* удалён: ",
                  delete_client(curs, 2))
            curs.execute("""
                            SELECT c.id, c.name, c.lastname, c.email, p.number FROM clients c
                            LEFT JOIN phonenumbers p ON c.id = p.client_id
                            ORDER by c.id
                            """)
            pprint(curs.fetchall())
         
            print('Найденный клиент по имени, фамилии, телефону и email:') 
            pprint(find_client(curs, '3', '0003',
                               '0003@gmail.com', '0003'))

            print('Найденный клиент по имени, фамилии, телефону:')
            pprint(find_client(curs, None, None, None, '0001'))