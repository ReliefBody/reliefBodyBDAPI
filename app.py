from flask import Flask, request, jsonify
from config import connection_string
import pyodbc

app = Flask(__name__)

def sqlQueri(queri: str, tupQueriInfo=None):
    try:
        cnxn = pyodbc.connect(connection_string)
        cursor = cnxn.cursor()
        cursor.execute(queri, tupQueriInfo or ())
        columns = [column[0] for column in cursor.description]
        # Перетворення результатів у список словників
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except pyodbc.Error as ex:
        print('Error executing query:', ex)
        return None
    finally:
        cursor.close()
        cnxn.close()


@app.route('/searchExercisesByID', methods=['GET', 'POST'])
def selectExercisesByID():
    if request.method == 'POST':
        exerciseId = request.form.get('id', '')
    else:
        exerciseId = request.args.get('id', '')

    if not exerciseId:
        return jsonify({'error': 'ID вправи не було надано.'}), 400

    query = """
    SELECT 
        e.id,
        e.name,
        et.name AS type,
        e.discrete,
        e.calories,
        STRING_AGG(m.name, ', ') AS muscles,
        e.personalWeight
    FROM 
        Exercises e
    INNER JOIN 
        ExerciseTypes et ON e.type_id = et.id
    CROSS APPLY 
        STRING_SPLIT(REPLACE(e.muscle_ids, ' ', ''), ',') AS s
    INNER JOIN 
        Muscles m ON CAST(s.value AS INT) = m.id
    WHERE 
        e.id = ?
    GROUP BY 
        e.id, e.name, et.name, e.discrete, e.calories, e.personalWeight;
    """
    rezults = sqlQueri(query, (exerciseId,))

    if rezults is None:
        return jsonify({'error': 'Помилка виконання запиту.'}), 500

    exercises = []
    for row in rezults:
        exercise = {
            'id': row.get('id'),
            'name': row.get('name'),
            'type': row.get('type', 'Не знайдено тип.'),
            'discrete': bool(row.get('discrete')),
            'calories': row.get('calories'),
            'muscle_names': [muscle.strip() for muscle in row.get('muscles', '').split(',')],
            'personalWeight': bool(row.get('personalWeight'))
        }
        exercises.append(exercise)
    return jsonify(exercises)

@app.route('/searchExercisesByName', methods=['GET', 'POST'])
def selectExercisesByName():
    if request.method == 'POST':
        exerciseName = request.form.get('name', '')
    else:
        exerciseName = request.args.get('name', '')

    if not exerciseName:
        return jsonify({'error': 'Назва вправи не була надана.'}), 400

    query = """
    SELECT 
        e.id,
        e.name,
        et.name AS type,
        e.discrete,
        e.calories,
        STRING_AGG(m.name, ', ') AS muscles,
        e.personalWeight
    FROM 
        Exercises e
    INNER JOIN 
        ExerciseTypes et ON e.type_id = et.id
    CROSS APPLY 
        STRING_SPLIT(REPLACE(e.muscle_ids, ' ', ''), ',') AS s
    INNER JOIN 
        Muscles m ON CAST(s.value AS INT) = m.id
    WHERE 
        e.name LIKE ?
    GROUP BY 
        e.id, e.name, et.name, e.discrete, e.calories, e.personalWeight;
    """
    prams = f"%{exerciseName}%"
    rezults = sqlQueri(query, (prams,))

    if rezults is None:
        return jsonify({'error': 'Помилка виконання запиту.'}), 500

    exercises = []
    for row in rezults:
        exercise = {
            'id': row.get('id'),
            'name': row.get('name'),
            'type': row.get('type', 'Не знайдено тип.'),
            'discrete': bool(row.get('discrete')),
            'calories': row.get('calories'),
            'muscle_names': [muscle.strip() for muscle in row.get('muscles', '').split(',')],
            'personalWeight': bool(row.get('personalWeight'))
        }
        exercises.append(exercise)
    return jsonify(exercises)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
