from flask import Flask, render_template, request, jsonify
from config import connection_string
import pyodbc

app = Flask(__name__)


def sqlQueri(queri: str, tupQueriInfo=None):
    try:
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()

        cursor.execute(queri, tupQueriInfo or ())

        if queri.strip().lower().startswith('select'):
            return cursor.fetchall()
        else:
            cnxn.commit()
    except pyodbc.Error as ex:
        print('Error', ex)
    finally:
        cursor.close()
        cnxn.close()


@app.route('/selectExercises', methods=['GET', 'POST'])
def selectExercises():

    query = """SELECT * FROM Exercises"""
    rezult = sqlQueri(query)

    exercises = []
    for row in rezult:
        exercise = {
            'id': row.id,
            'name': row.name,
            'type': row.type,
            'discrete': bool(row.discrete),
            'calories': row.calories,
            'muscle_ids': row.muscle_ids.split(',') if row.muscle_ids else [],
            'personalWeight': bool(row.personalWeight)
        }
        exercises.append(exercise)

    return jsonify(exercises)


'''
@app.route('/search_exercise', methods=['GET', 'POST'])
def search_exercise():
    # Отримання назви вправи з параметрів запиту
    if request.method == 'POST':
        exercise_name = request.form.get('name', '')
    else:
        exercise_name = request.args.get('name', '')

    if not exercise_name:
        return jsonify({'error': 'Назва вправи не була надана.'}), 400

    # Виконання пошуку в базі даних
    query = "SELECT * FROM Exercises WHERE name LIKE ?;"
    search_pattern = f"%{exercise_name}%"
    results = sqlQueri(query, (search_pattern,))

    if results is None:
        return jsonify({'error': 'Помилка при виконанні запиту до бази даних.'}), 500

    # Перетворення результатів у список словників
    exercises = []
    for row in results:
        exercise = {
            'id': row.id,
            'name': row.name,
            'type': row.type,
            'discrete': bool(row.discrete),
            'calories': row.calories,
            'muscle_ids': row.muscle_ids.split(',') if row.muscle_ids else [],
            'personalWeight': bool(row.personalWeight)
        }
        exercises.append(exercise)

    # Відправка результатів до зовнішнього сервісу
    external_service_url = 'http://localhost:5000/api/receive'  # Замініть на фактичну URL вашого сервісу
    try:
        response = requests.post(external_service_url, json={'exercises': exercises})
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print('Помилка при відправці даних до зовнішнього сервісу:', e)
        return jsonify({'error': 'Помилка при відправці даних до зовнішнього сервісу.'}), 500

    return jsonify(
        {'message': 'Пошук виконано успішно та дані відправлено до зовнішнього сервісу.', 'exercises': exercises}), 200
'''


if __name__ == '__main__':
    app.run(debug=True)