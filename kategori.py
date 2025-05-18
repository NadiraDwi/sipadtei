import hashlib
from flask import Blueprint, request, render_template, redirect, url_for, flash
from koneksi import get_db_connection

kategori_bp = Blueprint('kategori', __name__)

@kategori_bp.route("/kategori", endpoint='kategori')
def kategori():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kategori")
    kategori = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('kategori/index.html', kategori=kategori)

@kategori_bp.route("/kategori/tambah", methods=['GET', 'POST'], endpoint='tambah_kategori')
def tambah_kategori():
    if request.method == 'POST':
        nama_kategori = request.form.get('nama_kategori')

        if not nama_kategori:
            flash('Nama kategori tidak boleh kosong!', 'danger')
            return redirect(url_for('kategori.tambah_kategori'))

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Ambil ID terakhir dari kategori
        cursor.execute("SELECT id_kategori FROM kategori ORDER BY id_kategori DESC LIMIT 1")
        last = cursor.fetchone()
        
        if last:
            last_id = last['id_kategori']  # Contoh: 'K002'
            number = int(last_id[1:]) + 1  # Ambil angka dan tambah 1
        else:
            number = 1  # Jika belum ada data

        new_id = f'K{number:03d}'  # Format ke 'K001', 'K002', dst

        # Simpan ke database
        cursor.execute("INSERT INTO kategori (id_kategori, nama_kategori) VALUES (%s, %s)", (new_id, nama_kategori))
        conn.commit()
        cursor.close()
        conn.close()

        flash('Kategori berhasil ditambahkan!', 'success')
        return redirect(url_for('kategori.kategori'))

    return render_template('kategori/add.html')

@kategori_bp.route("/kategori/edit/<id>", methods=["GET", "POST"])
def edit_kategori(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        nama_kategori = request.form["nama_kategori"]
        cursor.execute("UPDATE kategori SET nama_kategori = %s WHERE id_kategori = %s", (nama_kategori, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Kategori berhasil diperbarui.", "success")
        return redirect(url_for("kategori.kategori"))

    cursor.execute("SELECT * FROM kategori WHERE id_kategori = %s", (id,))
    kategori = cursor.fetchone()
    cursor.close()
    conn.close()

    if kategori is None:
        flash("Data kategori tidak ditemukan!", "danger")
        return redirect(url_for("kategori.kategori"))

    return render_template("kategori/edit.html", kategori=kategori)

@kategori_bp.route("/kategori/hapus/<id>", methods=["GET", "POST"])
def hapus_kategori(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM kategori WHERE id_kategori = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash("Kategori berhasil dihapus.", "success")
    return redirect(url_for("kategori.kategori"))

