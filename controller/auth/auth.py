from . import *


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        user = users.find_one({"username": request.form['username']})
        if not user:
            flash('Username tidak ditemukan!', 'error')
            return render_template('view/auth/login.html')

        if not bcrypt.check_password_hash(user['password'], request.form['password']):
            flash('Password tidak sesuai!', 'error')
            return render_template('view/auth/login.html')

        user_obj = User(username=user['username'],
                        role=user['role'], id=user['_id'])
        login_user(user_obj)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
            return redirect(next_page)
        return redirect(request.args.get("next") or url_for("dashboard"))
    return render_template('view/auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        current_time = datetime.utcnow()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        required_fields = ['username', 'email', 'password']

        error_messages = {
            'username': 'Username tidak boleh kosong!',
            'email': 'Email tidak boleh kosong!',
            'password': 'Password tidak boleh kosong!',
        }

        for field in required_fields:
            if not locals()[field]:
                flash(error_messages[field], 'error')
                return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password,
            'role': 'guest',
            'createdAt': current_time,
            'updateAt': current_time
        })
        flash('Registrasi berhasil dilakukan!', 'success')
        return redirect(url_for('login'))
    return render_template('view/auth/register.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))
