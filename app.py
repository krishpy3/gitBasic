from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

database = [{"mid": 1, "year": 2013, "title": "Rush"},
            {"mid": 2, "year": 2014, "title": "Thor: The Dark World"}]

last_mid = 2


@app.route('/movie')
def list_movie():
    dd = []
    if request.args:
        for m in database:
            if m['year'] == int(request.args.get('year')):
                dd.append(m)
    else:
        dd = database
    return jsonify(dd)


@app.route('/movie/<mid>')
def get_movie(mid):
    for m in database:
        if m['mid'] == int(mid):
            return jsonify(m)
    return jsonify({'error': f'There is no movie with id: {mid}'})


@app.route('/movie', methods=['POST'])
def new_movie():
    global last_mid
    user_data = request.form
    last_mid += 1
    mov = {
        "mid": last_mid,
        "year": int(user_data.get('year', 1950)),
        "title": user_data.get('title', "No Title")
    }
    database.append(mov)
    return jsonify(mov)


@app.route('/movie/<mid>', methods=['PUT'])
def update_movie(mid):
    index = 0
    for m in database:
        if m['mid'] == int(mid):
            year = m['year']
            title = m['title']
            break
        index += 1

    mov = {
        "mid": mid,
        "year": int(request.form.get('year', year)),
        "title": request.form.get('title', title)
    }
    database.pop(index)
    database.insert(index, mov)
    return jsonify(mov)


@app.route('/movie/<mid>', methods=['DELETE'])
def delete_movie(mid):
    index = 0
    for m in database:
        if m['mid'] == int(mid):
            database.pop(index)
            break
        index += 1
    return jsonify({'msg': f'Movie with id {mid} deleted successfully'})


app.run(debug=True)
