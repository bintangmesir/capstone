from . import *


@app.route('/tentang')
def tentang():
    return render_template('view/client/tentang.html')
