from . import *

target = os.path.join(
    APP_ROOT, app.config['IMG_DONATUR'])
target2 = os.path.join(
    APP_ROOT, app.config['IMG_QR'])
donatur = db["donatur"]


@app.route('/data_donatur', methods=["GET"])
def data_donatur():
    donatur_data = donatur.find().sort("createdAt", pymongo.DESCENDING)
    return render_template('view/server/data-donatur/index.html', donatur=donatur_data)


@app.route('/data_donatur/create', methods=["GET"])
def data_donatur_create():
    return render_template('view/server/data-donatur/create.html')


@app.route('/data_donatur/<id>/edit', methods=["GET"])
def data_donatur_edit(id):
    donatur_data = donatur.find_one({"_id": ObjectId(id)})
    return render_template('view/server/data-donatur/edit.html', donatur=donatur_data)


@app.route('/data_donatur', methods=["POST"])
def data_donatur_store():
    if not os.path.isdir(target):
        os.mkdir(target)
    judul = request.form['judul']
    deskripsi = request.form['deskripsi']
    image = request.files["image"]
    imageQr = request.files["imageQr"]

    required_fields = ['judul', 'deskripsi', 'image', 'imageQr']
    error_messages = {
        'judul': 'Data judul tidak boleh kosong',
        'deskripsi': 'Data deskripsi tidak boleh kosong',
        'image': 'Data image tidak boleh kosong',
        'imageQr': 'Data image QR tidak boleh kosong',
    }

    for field in required_fields:
        if not locals()[field]:
            flash(error_messages[field], 'error')
            return redirect(url_for('data_donatur_create'))

    current_time = datetime.utcnow()
    filename = secure_filename(image.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
    destination = os.path.join(target, unique_filename)
    image.save(destination)

    filename2 = secure_filename(imageQr.filename)
    unique_filename2 = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename2}"
    destination2 = os.path.join(target2, unique_filename2)
    imageQr.save(destination2)
    donatur.insert_one({'judul': judul,
                        'deskripsi': deskripsi,
                        "image": unique_filename,
                        "imageQr": unique_filename2,
                        "createdAt": current_time,
                        "updateAt": current_time})
    flash('Data donatur berhasil di tambah!', 'success')
    return redirect(url_for('data_donatur'))


@app.route('/data_donatur/<id>', methods=["POST"])
def data_donatur_update(id):
    judul = request.form['judul']
    deskripsi = request.form['deskripsi']
    new_image = request.files["image"]
    new_imageQr = request.files["imageQr"]

    required_fields = ['judul', 'deskripsi', 'new_image', 'new_imageQr']

    error_messages = {
        'judul': 'Data judul tidak boleh kosong',
        'deskripsi': 'Data deskripsi tidak boleh kosong',
        'new_image': 'Data image tidak boleh kosong',
        'new_imageQr': 'Data image QR tidak boleh kosong',
    }

    for field in required_fields:
        if not locals()[field]:
            flash(error_messages[field], 'error')
            return redirect(url_for('data_donatur_edit', id=id))

    if not os.path.isdir(target):
        os.mkdir(target)

    existing_data = donatur.find_one({"_id": ObjectId(id)})
    existing_image = existing_data.get("image")

    if existing_image:
        existing_image_path = os.path.join(target, existing_image)
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)

    filename = secure_filename(new_image.filename)
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename}"
    destination = os.path.join(target, unique_filename)
    new_image.save(destination)

    if not os.path.isdir(target2):
        os.mkdir(target2)
    existing_image2 = existing_data.get("imageQr")

    if existing_image2:
        existing_image_path2 = os.path.join(target2, existing_image2)
        if os.path.exists(existing_image_path2):
            os.remove(existing_image_path2)

    filename2 = secure_filename(new_imageQr.filename)
    unique_filename2 = f"{datetime.now().strftime('%Y%m%d%H%M%S')}-{filename2}"
    destination2 = os.path.join(target2, unique_filename2)
    new_imageQr.save(destination2)

    donatur.update_one({"_id": ObjectId(id)},
                       {"$set": {
                           "judul": judul,
                           "deskripsi": deskripsi,
                           "image": unique_filename,
                           "imageQr": unique_filename2,
                           "updateAt": current_time}
                        })
    flash('Data donatur berhasil di edit!', 'success')
    return redirect(url_for('data_donatur'))


@app.route('/data_donatur/delete/<id>', methods=["POST"])
def data_donatur_delete(id):
    if not os.path.isdir(target):
        os.mkdir(target)

    existing_data = donatur.find_one({"_id": ObjectId(id)})
    existing_image = existing_data.get("image")

    if existing_image:
        existing_image_path = os.path.join(target, existing_image)
        if os.path.exists(existing_image_path):
            os.remove(existing_image_path)

    if not os.path.isdir(target2):
        os.mkdir(target2)
    existing_image2 = existing_data.get("imageQr")

    if existing_image2:
        existing_image_path2 = os.path.join(target2, existing_image2)
        if os.path.exists(existing_image_path2):
            os.remove(existing_image_path2)
    donatur.delete_one({"_id": ObjectId(id)})
    flash('Data donatur berhasil di hapus!', 'success')
    return redirect(url_for('data_donatur'))
