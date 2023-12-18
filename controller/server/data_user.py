from . import *

users = db["users"]


@app.route('/data_users', methods=["GET"])
def data_users():
    users_data = users.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/server/data-user/index.html', users=users_data)


@app.route('/data_users/<id>/edit', methods=["GET"])
def data_users_edit(id):
    users_data = users.find_one({"_id": ObjectId(id)})
    return render_template('view/server/data-user/edit.html', users=users_data)


@app.route('/data_users/<id>', methods=["POST"])
def data_users_update(id):
    username = request.form['username']
    email = request.form['email']
    role = request.form['role']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    required_fields = ['username', 'email',
                       'role', 'password', 'confirm_password']
    error_messages = {
        'username': 'Data username tidak boleh kosong',
        'email': 'Data email tidak boleh kosong',
        'role': 'Data role tidak boleh kosong',
        'password': 'Data password tidak boleh kosong',
        'confirm_password': 'Data confirm_password tidak boleh kosong',
    }

    for field in required_fields:
        if not locals()[field]:
            flash(error_messages[field], 'error')
            return redirect(url_for('data_users_edit', id=id))

    if password != confirm_password:
        flash('Password dan Confirm password tidak sama', 'error')
        return redirect(url_for('data_users_edit', id=id))

    user = users.find_one({"username": request.form['username']})
    if user and bcrypt.check_password_hash(user['password'], request.form['password']):
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        users.update_one({"_id": ObjectId(id)},
                         {"$set": {
                             'username': username,
                             'email': email,
                             'password': hashed_password,
                             'role': role,
                             'updateAt': current_time}
                          })
        flash('Data user berhasil di edit!', 'success')
        return redirect(url_for('data_users'))
    else:
        return redirect(url_for('data_users_edit', id=id))


@app.route('/data_users/delete/<id>', methods=["POST"])
@login_required
@roles_required('admin')
def data_users_delete(id):
    delete_user = users.find_one({'_id': ObjectId(id)})
    users.delete_one(delete_user)
    flash('Data user berhasil di hapus!', 'success')
    return redirect(url_for('data_users'))
