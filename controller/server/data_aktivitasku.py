from . import *
aktivitas = db["aktivitas"]
aktivitasku = db["aktivitasku"]


@app.route('/data_aktivitasku', methods=["GET"])
@login_required
@roles_required('admin')
def data_aktivitasku():
    aktivitasku_data = aktivitasku.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/server/data-aktivitasku/index.html', aktivitasku=aktivitasku_data)


@app.route('/data_aktivitasku/<id>/edit', methods=["GET"])
@login_required
@roles_required('admin')
def data_aktivitasku_edit(id):
    aktivitasku_data = aktivitasku.find_one({"_id": ObjectId(id)})
    return render_template('view/server/data-aktivitasku/edit.html', aktivitasku=aktivitasku_data)


@app.route('/data_aktivitasku', methods=["POST"])
@login_required
@roles_required('guest', 'donatur', 'admin')
def data_aktivitasku_store():
    id = request.args.get('id')
    aktivitas_data = aktivitas.find_one({"_id": ObjectId(id)})
    deskripsi = request.form['deskripsi']
    deskripsi2 = request.form['deskripsi2']
    pekerjaan = request.form['pekerjaan']

    required_fields = ['deskripsi', 'deskripsi2', 'pekerjaan']
    error_messages = {
        'deskripsi': 'Data deskripsi tidak boleh kosong',
        'deskripsi2': 'Data deskripsi tidak boleh kosong',
        'pekerjaan': 'Data pekerjaan tidak boleh kosong',
    }

    for field in required_fields:
        if not locals()[field]:
            flash(error_messages[field], 'error')
            return redirect(url_for('aktivitas_detail', id=id))

    aktivitasku.insert_one({"username": current_user.username,
                            "deskripsi": deskripsi,
                            "deskripsi2": deskripsi2,
                            "pekerjaan": pekerjaan,
                            "aktivitasData": aktivitas_data,
                            "status": "pending",
                            "createdAt": current_time,
                            "updateAt": current_time})
    flash('Permohonan bergabung pada aktivitas berhasil di kirim!', 'success')
    return redirect(url_for('aktivitasku'))


@app.route('/data_aktivitasku/<id>', methods=["POST"])
@login_required
@roles_required('admin')
def data_aktivitasku_update(id):
    deskripsi = request.form['deskripsi']
    deskripsi2 = request.form['deskripsi2']
    pekerjaan = request.form['pekerjaan']
    status = request.form['status']

    required_fields = ['deskripsi',
                       'deskripsi2', 'pekerjaan', 'status']
    error_messages = {
        'deskripsi': 'Data deskripsi tidak boleh kosong',
        'deskripsi2': 'Data deskripsi tidak boleh kosong',
        'pekerjaan': 'Data pekerjaan tidak boleh kosong',
        'status': 'Data status tidak boleh kosong',
    }

    aktivitasku.update_one({"_id": ObjectId(id)},
                           {"$set": {
                               "deskripsi": deskripsi,
                               "deskripsi2": deskripsi2,
                               "pekerjaan": pekerjaan,
                               "status": status,
                               "updateAt": current_time}
                            })
    flash('Data aktivitasku berhasil di edit!', 'success')
    return redirect(url_for('data_aktivitasku'))


@app.route('/data_aktivitasku/delete/<id>', methods=["POST"])
@login_required
@roles_required('guest', 'donatur', 'admin')
def data_aktivitasku_delete(id):
    aktivitasku.delete_one({"_id": ObjectId(id)})
    flash('Data aktivitasku berhasil di hapus!', 'success')
    return redirect(url_for('data_aktivitasku'))
