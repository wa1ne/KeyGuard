import sqlite3

def open_connection():
    connection = sqlite3.connect('passbase.db')
    query = '''
CREATE TABLE IF NOT EXISTS Passwords (
id INTEGER,
service TEXT NOT NULL,
password TEXT NOT NULL,
tag blob
);
    '''
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
       print(f"The error '{e}' occurred")
    connection.close()

def add_password(user_id, service, password, tag):
    connection = sqlite3.connect('passbase.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Passwords (id, service, password, tag) VALUES (?, ?, ?, ?)', (user_id, service.lower(), password, tag))
    connection.commit()
    connection.close()

def get_password(user_id, service):
    connection = sqlite3.connect('passbase.db')
    cursor = connection.cursor()
    cursor.execute('SELECT password, tag FROM Passwords WHERE id = ? and service = ?', (user_id, service.lower()))
    pass_result = cursor.fetchall()
    connection.close()
    return pass_result

def remove_service(user_id, service):
    connection = sqlite3.connect('passbase.db')
    cursor = connection.cursor()
    print(user_id, service)
    cursor.execute('DELETE FROM Passwords WHERE id = ? and service = ?', (user_id, service))
    connection.commit()
    connection.close()

def list_of_services(user_id):
    connection = sqlite3.connect('passbase.db')
    cursor = connection.cursor()
    cursor.execute('SELECT service FROM Passwords WHERE id = ?', (user_id,))
    pass_result = cursor.fetchall()
    return pass_result

def get_list_of_services(user_id):
    list = list_of_services(user_id)
    pass_string = ''
    for service in list:
        service_string = service[0]
        pass_string = pass_string + service_string + '\n'
    return pass_string