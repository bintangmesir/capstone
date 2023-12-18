from . import *


@app.route('/dashboard')
@login_required
@roles_required('admin')
def dashboard():
    users = db["users"].count_documents({})
    donatur = db["donatur"].count_documents({})
    artikel = db["artikel"].count_documents({})
    aktivitas = db["aktivitas"].count_documents({})
    aktivitasku = db["aktivitasku"].count_documents({})
    return render_template('view/server/dashboard.html', users=users, donatur=donatur, artikel=artikel, aktivitas=aktivitas, aktivitasku=aktivitasku)
