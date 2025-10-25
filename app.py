import os
from flask import (
    Flask, request, render_template, redirect, url_for, session, flash,
    send_file, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import io, json

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')
FLAG = os.getenv('FLAG', 'TCC{FAKE_FLAG_FOR_TEST}')

# In-memory "database" of 10 mahasiswa
users = {
    "1": {
        "username": "agus",
        "email": "agus.santoso@pens.ac.id",
        "password": generate_password_hash("agus123"),
        "nrp": "242000001",
        "jurusan": "Teknologi Rekayasa Internet",
        "joined": datetime(2022, 1, 10),
        "bio": "Mahasiswa aktif di program studi Teknologi Rekayasa Internet.",
        "location": "Kota Jakarta",
        "profile_image": "1.png",
        "alamat": "Jl. Merdeka No. 1, Jakarta",
        "telepon": "081234567890",
        "ip_terakhir": "192.168.0.1"
    },
    "2": {
        "username": "Budi Pratama",
        "email": "budi.pratama@pens.ac.id",
        "password": generate_password_hash("pass2"),
        "nrp": "242000002",
        "jurusan": "Teknik Informatika",
        "joined": datetime(2021, 9, 15),
        "bio": "Mahasiswa aktif di program studi Teknik Informatika.",
        "location": "Kota Bandung",
        "profile_image": "2.png",
        "alamat": "Jl. Diponegoro No. 12, Bandung",
        "telepon": "082134567891",
        "ip_terakhir": "192.168.0.2"
    },
    "3": {
        "username": "Citra Dewi",
        "email": "citra.dewi@pens.ac.id",
        "password": generate_password_hash("pass3"),
        "nrp": "242000003",
        "jurusan": "Teknologi Game",
        "joined": datetime(2023, 2, 20),
        "bio": "Mahasiswa aktif di program studi Teknologi Game.",
        "location": "Kota Surabaya",
        "profile_image": "3.png",
        "alamat": "Jl. Pahlawan No. 34, Surabaya",
        "telepon": "083234567892",
        "ip_terakhir": "192.168.0.3"
    },
    "4": {
        "username": "Dewi Lestari",
        "email": "dewi.lestari@pens.ac.id",
        "password": generate_password_hash("pass4"),
        "nrp": "242000004",
        "jurusan": "Teknik Telekomunikasi",
        "joined": datetime(2020, 7, 12),
        "bio": "Mahasiswa aktif di program studi Teknik Telekomunikasi.",
        "location": "Kota Yogyakarta",
        "profile_image": "4.png",
        "alamat": "Jl. Malioboro No. 56, Yogyakarta",
        "telepon": "084234567893",
        "ip_terakhir": "192.168.0.4"
    },
    "5": {
        "username": "Eko Saputra",
        "email": "eka.saputra@pens.ac.id",
        "password": generate_password_hash("pass5"),
        "nrp": "242000005",
        "jurusan": "Teknologi Rekayasa Internet",
        "joined": datetime(2022, 4, 8),
        "bio": "Mahasiswa aktif di program studi Teknologi Rekayasa Internet.",
        "location": "Kota Tulungagung",
        "profile_image": "5.png",
        "alamat": "Jl. Setiabudi No. 78, Tulungagung",
        "telepon": "085234567894",
        "ip_terakhir": "192.168.0.5",
        "flag": FLAG
    },
    "6": {
        "username": "Fajar Nugroho",
        "email": "fajar.nugroho@pens.ac.id",
        "password": generate_password_hash("pass6"),
        "nrp": "242000006",
        "jurusan": "Teknik Informatika",
        "joined": datetime(2023, 10, 5),
        "bio": "Mahasiswa aktif di program studi Teknik Informatika.",
        "location": "Kota Jakarta",
        "profile_image": "6.png",
        "alamat": "Jl. Sudirman No. 99, Jakarta",
        "telepon": "086234567895",
        "ip_terakhir": "192.168.0.6",
        "note": "Dikit lagi bang"
    },
    "7": {
        "username": "Gita Ramadhan",
        "email": "gita.ramadhan@pens.ac.id",
        "password": generate_password_hash("pass7"),
        "nrp": "242000007",
        "jurusan": "Teknologi Game",
        "joined": datetime(2021, 11, 18),
        "bio": "Mahasiswa aktif di program studi Teknologi Game.",
        "location": "Kota Surabaya",
        "profile_image": "7.png",
        "alamat": "Jl. Kayoon No. 100, Surabaya",
        "telepon": "087234567896",
        "ip_terakhir": "192.168.0.7"
    },
    "8": {
        "username": "Hadi Wijaya",
        "email": "hadi.wijaya@pens.ac.id",
        "password": generate_password_hash("pass8"),
        "nrp": "242000008",
        "jurusan": "Teknik Telekomunikasi",
        "joined": datetime(2022, 6, 30),
        "bio": "Mahasiswa aktif di program studi Teknik Telekomunikasi.",
        "location": "Kota Yogyakarta",
        "profile_image": "8.png",
        "alamat": "Jl. Kaliurang No. 123, Yogyakarta",
        "telepon": "088234567897",
        "ip_terakhir": "192.168.0.8"
    },
    "9": {
        "username": "Intan Permata",
        "email": "intan.permata@pens.ac.id",
        "password": generate_password_hash("pass9"),
        "nrp": "242000009",
        "jurusan": "Teknik Informatika",
        "joined": datetime(2020, 8, 15),
        "bio": "Mahasiswa aktif di program studi Teknik Informatika.",
        "location": "Kota Bandung",
        "profile_image": "9.png",
        "alamat": "Jl. Pasteur No. 45, Bandung",
        "telepon": "089234567898",
        "ip_terakhir": "192.168.0.9"
    },
    "10": {
        "username": "Woko Jidodo",
        "email": "woko.jidodo@pens.ac.id",
        "password": generate_password_hash("pass10"),
        "nrp": "242000010",
        "jurusan": "Teknologi Rekayasa Internet",
        "joined": datetime(2021, 12, 22),
        "bio": "Mahasiswa aktif di program studi Teknologi Rekayasa Internet.",
        "location": "Kota Jakarta",
        "profile_image": "10.png",
        "alamat": "Jl. Gatot Subroto No. 67, Jakarta",
        "telepon": "080234567899",
        "ip_terakhir": "192.168.0.10",
        "note": "Hmm sepertinya user dibawah 7 punya rahasia"
    },
    "11": {
        "username": "Dian Susena",
        "email": "dian.susena@pens.ac.id",
        "password": generate_password_hash("pass10"),
        "nrp": "242000010",
        "jurusan": "Teknologi Rekayasa Internet",
        "joined": datetime(2021, 12, 22),
        "bio": "Mahasiswa aktif di program studi Teknologi Rekayasa Internet.",
        "location": "Kota Jakarta",
        "profile_image": "10.png",
        "alamat": "Jl. Gatot Subroto No. 67, Jakarta",
        "telepon": "080234567899",
        "ip_terakhir": "192.168.0.10",
        "note": "Hmm sepertinya user dibawah 7 punya rahasia"
    },
    "12": {
        "username": "Ilham Hilmawan",
        "email": "ilham837748@pens.ac.id",
        "password": generate_password_hash("pass10"),
        "nrp": "242000010",
        "jurusan": "Teknologi Rekayasa Internet",
        "joined": datetime(2021, 12, 22),
        "bio": "Mahasiswa aktif di program studi Teknologi Rekayasa Internet.",
        "location": "Kota Jakarta",
        "profile_image": "10.png",
        "alamat": "Jl. Gatot Subroto No. 67, Jakarta",
        "telepon": "080234567899",
        "ip_terakhir": "192.168.0.10",
        "note": "Hmm sepertinya user dibawah 7 punya rahasia"
    },
    "13": {
        "username": "Dian Sastrowijowo",
        "email": "wijowow8372@pens.ac.id",
        "password": generate_password_hash("pass10"),
        "nrp": "242000010",
        "jurusan": "Teknologi Rekayasa Internet",
        "joined": datetime(2021, 12, 22),
        "bio": "Mahasiswa aktif di program studi Teknologi Rekayasa Internet.",
        "location": "Kota Jakarta",
        "profile_image": "10.png",
        "alamat": "Jl. Gatot Subroto No. 67, Jakarta",
        "telepon": "080234567899",
        "ip_terakhir": "192.168.0.10",
        "note": "Hmm sepertinya user dibawah 7 punya rahasia"
    }
}

def get_user_by_username(username):
    for uid, data in users.items():
        if data['username'] == username:
            return uid, data
    return None, None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('profile', user_id=session['user_id']))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    uid, user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        session['user_id'] = uid
        return redirect(url_for('profile', user_id=uid))
    flash('Invalid credentials', 'danger')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/profile/<user_id>')
def profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = users.get(user_id)
    if not user:
        return "Mahasiswa tidak ditemukan", 404
    return render_template('profile.html', **user, id=user_id)

# New: Download transcript (dummy PDF)
@app.route('/profile/<user_id>/transcript')
def transcript(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    # IDOR applies here as well
    # Generate dummy PDF in-memory
    pdf = io.BytesIO()
    pdf.write(b"%PDF-1.4\n%Dummy transcript for user " + user_id.encode())
    pdf.seek(0)
    return send_file(
        pdf,
        as_attachment=True,
        download_name=f"transcript_{user_id}.pdf",
        mimetype='application/pdf'
    )

# New: Export personal data as JSON
@app.route('/profile/<user_id>/export')
def export_data(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    user = users.get(user_id)
    if not user:
        return "Mahasiswa tidak ditemukan", 404
    # Exclude password
    export = {k: v for k, v in user.items() if k != 'password'}
    return jsonify(export)

# New: Send message to admin (dummy)
@app.route('/profile/<user_id>/message', methods=['POST'])
def send_message(user_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    msg = request.form.get('message')
    # In real app, store or email; here just flash
    flash(f"Pesan terkirim ke BAAK: {msg}", 'success')
    return redirect(url_for('profile', user_id=user_id))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)