"""Provide REST API.

Root URL: http://[hostname/]/tracktools/v1.0/

Methods:
GET http://[hostname/]/tracktools/v1.0/users/[user_id]/workouts
    List workout for a user
GET http://[hostname/]/tracktools/v1.0/users/[user_id]/workouts/[workout_timestamp]
    Get a workout
GET http://[hostname/]/tracktools/v1.0/users/[user_id]/workouts/[workout_timestamp]/stats
    Get only workout stats
POST http://[hostname/]/tracktools/v1.0/users/[user_id]/workouts
    Store a new workout
"""

from flask import Flask, abort, jsonify, request, flash
import workout
import storage_helper
import file_helper

ROOT_URL = "/tracktools/v1.0/users/1/"

app = Flask(__name__, static_url_path='/static')

@app.route(ROOT_URL + 'workouts/<int:workout_timestamp>', methods=['GET'])
def get_workout(workout_timestamp):
    print("I'm get_workout")
    try:
        print("Connecting to DB")
        my_storage_helper = storage_helper.StorageHelper('eu-central-1', "https://dynamodb.eu-central-1.amazonaws.com",
                                                     "WorkoutsTest")
        print("Loading workout from DB")
        my_workout_dict = my_storage_helper.load_workout_json(user_id=1, timestamp=workout_timestamp)
    except:
        print("Cannot load workout from DB.")
        abort(500)
    else:
        return jsonify(my_workout_dict)

@app.route(ROOT_URL + 'workouts', methods=['POST'])
def post_workout():
    """Load workout from tcx/gpx and store it to database

    Request format:
    raw tcx/gpx file
    """
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    f = request.files['file']
    print("Type of f is", type(f))
    # if user does not select file, browser also
    # submits an empty part without filename
    if f.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if f is not None:
        read_data = f.read()

    try:
        my_file_helper = file_helper.FileHelper()
        my_workout = my_file_helper.load(read_data)
        print("my_workout type is: ", type(my_workout))
        print(my_workout)
    except:
        print("Cannot parse uploaded file")
        abort(500)

    try:
        my_storage_helper = storage_helper.StorageHelper('eu-central-1',
                                                         "https://dynamodb.eu-central-1.amazonaws.com", "WorkoutsTest")
        my_storage_helper.save_workout(my_workout)
    except:
        print("Cannot save to DB")
        abort(500)

    response = {
        'timestamp': my_workout.timestamp,
        'status': 'saved'
    }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, port=8080)