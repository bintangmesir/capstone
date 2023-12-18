from . import *
target = os.path.join(
    APP_ROOT, app.config['IMG_AKTIVITAS'])
aktivitas = db["aktivitas"]


@app.route('/data_aktivitas', methods=["GET"])
@login_required
@roles_required('admin')
def data_aktivitas():
    aktivitas_data = aktivitas.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/server/data-aktivitas/index.html', aktivitas=aktivitas_data)


@app.route('/data_aktivitas/create', methods=["GET"])
@login_required
@roles_required('admin')
def data_aktivitas_create():
    return render_template('view/server/data-aktivitas/create.html')


@app.route('/data_aktivitas/<id>/edit', methods=["GET"])
@login_required
@roles_required('admin')
def data_aktivitas_edit(id):
    aktivitas_data = aktivitas.find_one({"_id": ObjectId(id)})
    return render_template('view/server/data-aktivitas/edit.html', aktivitas=aktivitas_data)


@app.route('/data_aktivitas', methods=["POST"])
@login_required
@roles_required('admin')
def data_aktivitas_store():
    if not os.path.isdir(target):
        os.mkdir(target)
    judul = request.form['judul']
    deskripsi = request.form['deskripsi']
    image = request.files["image"]

    required_fields = ['judul', 'deskripsi', 'image']
    error_messages = {
        'judul': 'Data judul tidak boleh kosong',
        'deskripsi': 'Data deskripsi tidak boleh kosong',
        'image': 'Data image tidak boleh kosong',
    }

    for field in required_fields:
        if not locals()[field]:
            flash(error_messages[field], 'error')
            return redirect(url_for('data_aktivitas_create'))

    filename = secure_filename(image.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
    destination = os.path.join(target, unique_filename)
    image.save(destination)

    aktivitas.insert_one({'judul': judul,
                          'deskripsi': deskripsi,
                          "image": unique_filename,
                          "createdAt": current_time,
                          "updateAt": current_time})
    flash('Data aktivitas berhasil di tambah!', 'success')
    return redirect(url_for('data_aktivitas'))


@app.route('/data_aktivitas/<id>', methods=["POST"])
@login_required
@roles_required('admin')
def data_aktivitas_update(id):
    judul = request.form['judul']
    deskripsi = request.form['deskripsi']
    new_image = request.files["image"]

    required_fields = ['judul', 'deskripsi', 'new_image']
    error_messages = {
        'judul': 'Data judul tidak boleh kosong',
        'deskripsi': 'Data deskripsi tidak boleh kosong',
        'new_image': 'Data image tidak boleh kosong',
    }

    for field in required_fields:
        if not locals()[field]:
            flash(error_messages[field], 'error')
            return redirect(url_for('data_aktivitas_edit', id=id))

    if not os.path.isdir(target):
        os.mkdir(target)

    existing_data = aktivitas.find_one({"_id": ObjectId(id)})
    existing_image = existing_data.get("image")

    if existing_image:
        existing_image_path = os.path.join(target, existing_image)
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)

    filename = secure_filename(new_image.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
    destination = os.path.join(target, unique_filename)
    new_image.save(destination)

    aktivitas.update_one({"_id": ObjectId(id)},
                         {"$set": {
                             "judul": judul,
                             "deskripsi": deskripsi,
                             "image": unique_filename,
                             "updateAt": current_time}
                          })
    flash('Data aktivitas berhasil di edit!', 'success')
    return redirect(url_for('data_aktivitas'))


@app.route('/data_aktivitas/delete/<id>', methods=["POST"])
@login_required
@roles_required('admin')
def data_aktivitas_delete(id):
    if not os.path.isdir(target):
        os.mkdir(target)

    existing_data = aktivitas.find_one({"_id": ObjectId(id)})
    existing_image = existing_data.get("image")

    if existing_image:
        existing_image_path = os.path.join(target, existing_image)
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)
    aktivitas.delete_one({"_id": ObjectId(id)})
    flash('Data aktivitas berhasil di hapus!', 'success')
    return redirect(url_for('data_aktivitas'))
