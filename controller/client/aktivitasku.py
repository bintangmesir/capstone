from . import *


@app.route('/aktivitasku')
@login_required
def aktivitasku():
    aktivitas = db["aktivitas"]
    aktivitasku = db["aktivitasku"]
    aktivitas_data = aktivitas.find()
    aktivitasku_data = aktivitasku.find()
    return render_template('view/client/aktivitasku.html', aktivitas=aktivitas_data, aktivitasku=aktivitasku_data)
