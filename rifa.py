import psycopg2
import random
import flask
import json


database = 'rifa'
user ='valentinaguerrero'
password ='Perro12345678?'

app = flask.Flask(__name__)


@app.route('/nueva_boleta/<name>/<string_one>/<string_two>')
def update_boleta(name, string_one, string_two):
    connection = connect_database()
    cursor = connection.cursor()
    query=  '''UPDATE boletas SET name = %s, available = 'Nop' WHERE numberOne = %s AND numberTwo = %s; '''
    cursor.execute(query, (name, string_one, string_two))
    connection.commit()
    count = cursor.rowcount
    message = {
    'message' : 'Record updated successfully',
    'primer_numero': string_one,
    'segundo_numero': string_two,
    'nombre': name,
    'number': count
    }
    return json.dumps(message)




def connect_database():
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        return connection
    except Exception as e:
        print(e)
        exit()



def add_boleta(string_one, string_two, string_three, string_four):
   
    search_string_one = string_one
    search_string_two = string_two
    search_string_three = string_three
    search_string_four = string_four
    

    query=  '''INSERT INTO boletas (numberOne, numberTwo, name, available) VALUES (%s, %s, %s, %s); '''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        record_to_insert = (string_one, string_two, string_three, string_four)
        cursor.execute(query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        response = {
         'message' : 'Record inserted successfully into mobile table',
         'count': count

        }
        return json.dumps(response)
                    
    except (Exception, psycopg2.Error) as error :
        if(connection):
            response = {
             'message' : 'Error, please check your entry',
             'count': count

            }
            return json.dumps(response)

@app.route('/nueva_boleta_azar/<name>')
def nueva_boleta_azar(name):
    search_string_one = ''
    search_string_two = ''
    query = '''SELECT * FROM boletas WHERE available = 'No'; '''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            search_string_one = row[0]
            search_string_two = row[1]
    
        cursor = connection.cursor()
        query=  '''UPDATE boletas SET name = %s, available = 'Nop' WHERE numberOne = %s AND numberTwo = %s; '''
        cursor.execute(query, (name, string_one, string_two))
        connection.commit()
        count = cursor.rowcount
        message = {
        'message' : 'Record updated successfully',
        'primer_numero': string_one,
        'segundo_numero': string_two,
        'nombre': name,
        'number': count
        }
        return json.dumps(message)

    except Exception as e:
        response = {
         'message' : 'Error, please check your entry'

        }
        return json.dumps(response)

def create_rifa():
    first_list = []
    second_list = []
    final_list = []
    for i in range(1, 51):
        if i not in first_list:
            first_list.append(i)
    

    for i in range(51, 101):
        if i not in second_list:
            second_list.append(i)
   

    for number in first_list:
        length = len(second_list) - 1 
        if number < 50:
            index = random.randint(1, length)
            final_list.append([number, second_list[index]])
            second_list.pop(index)

        else:
            last_element = second_list.pop()
            final_list.append([number, last_element])

    return final_list


@app.route('/eliminar_boleta/<name>/<string_one>/<string_two>')
def reset_boleta(string_one, string_two, name):
    connection = connect_database()
    cursor = connection.cursor()

    query=  '''UPDATE boletas SET name = 'Nadie', available = 'Yes' WHERE name = %s AND numberOne = %s AND numberTwo = %s; '''
    try:
        cursor.execute(query, (name, string_one, string_two))
        connection.commit()
        count = cursor.rowcount
        response = {
         'message' : 'Record inserted successfully into mobile table',
         'count': count
        }
        return json.dumps(response)
    except Exception as e:
        response = {
         'message' : 'Error, please check your entry',
         'count': count

        }
        return json.dumps(response)


@app.route('/crear_rifa')
def populate_rifa():
    final_list = create_rifa()

    for row in final_list:
        numberOne = row[0]
        numberTwo = row[1]
        name = "Nadie"
        disponible = "Si"
        add_boleta(numberOne, numberTwo, name, disponible)



@app.route('/todas')
def todas():
    response = []
    query = '''SELECT * FROM boletas'''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            dictionary = {
            'primer_numero' : row[0],
            'segundo_numero' : row[1],
            'nombre' : row[2],
            'disponible' : row[3],
            }
            
            response.append(dictionary)
        return json.dumps(response)

                
    except Exception as e:
        print(e)
        exit()

@app.route('/disponibles')
def disponibles():
    response = []
    query = '''SELECT * FROM boletas WHERE available != 'No';'''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            dictionary = {
            'primer_numero' : row[0],
            'segundo_numero' : row[1],
            'nombre' : row[2],
            'disponible' : row[3],
            }
            
            response.append(dictionary)
        return json.dumps(response)

                
    except Exception as e:
        print(e)
        exit()

    

@app.route('/compradas')
def compradas():
    response = []
    query = '''SELECT * FROM boletas WHERE available = 'No';'''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            dictionary = {
            'primer_numero' : row[0],
            'segundo_numero' : row[1],
            'nombre' : row[2],
            'disponible' : row[3],
            }
            
            response.append(dictionary)
        return json.dumps(response)

                
    except Exception as e:
        print(e)
        exit()


def create_boleta_azar(name, string_one, string_two):
    connection = connect_database()
    cursor = connection.cursor()
    query=  '''UPDATE boletas SET name = %s, available = 'Nop' WHERE numberOne = %s AND numberTwo = %s; '''
    cursor.execute(query, (name, string_one, string_two))
    connection.commit()
    count = cursor.rowcount
    message = {
    'message' : 'Record updated successfully',
    'primer_numero': string_one,
    'segundo_numero': string_two,
    'nombre': name,
    'number': count
    }
    return json.dumps(message)



if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
    




