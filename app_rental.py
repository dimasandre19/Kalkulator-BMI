import streamlit as st
import mysql.connector
import pandas as pd

# Konfigurasi Halaman Web
st.set_page_config(page_title="Rentalinaja", layout="wide")

# Fungsi Koneksi ke Database MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Sesuaikan jika XAMPP kamu ada password-nya
        database="db_rental_mobil"
    )

st.title("Rentalinaja")

# Menu Navigasi di Sidebar Kiri
menu = st.sidebar.selectbox("Pilih Menu", ["Kelola Penyewa", "Kelola Mobil", "Transaksi Rental"])

# ==========================================
# 1. MENU KELOLA PENYEWA
# ==========================================
if menu == "Kelola Penyewa":
    st.header("Data Penyewa")
    
    with st.expander("Tambah Penyewa Baru"):
        nama = st.text_input("Nama Lengkap")
        no_hp = st.text_input("Nomor HP / WhatsApp")
        alamat = st.text_area("Alamat Lengkap")
        
        if st.button("Simpan Penyewa"):
            if nama and no_hp:
                conn = get_connection()
                cursor = conn.cursor()
                query = "INSERT INTO penyewa (merek, plat_nomor, harga_sewa) VALUES (%s, %s, %s)"
                cursor.execute(query, (merek, plat_nomor, harga_sewa))
                conn.commit()
                conn.close()
                st.success(f"Berhasil menambahkan penyewa: {nama}")
                st.rerun()
            else:
                st.warning("Nama dan Nomor HP wajib diisi!")

    # Tampilkan Tabel Penyewa
    conn = get_connection()
    try:
        df_penyewa = pd.read_sql("SELECT * FROM penyewa", conn)
        st.subheader("Daftar Penyewa Terdaftar")
        st.dataframe(df_penyewa, use_container_width=True)
    except Exception as e:
        st.info("Belum ada data penyewa.")
    finally:
        conn.close()

# ==========================================
# 2. MENU KELOLA MOBIL
# ==========================================
elif menu == "Kelola Mobil":
    st.header("Data Mobil")
    
    with st.expander("Tambah Mobil Baru"):
        nama_mobil = st.text_input("Nama / Merk Mobil (misal: Avanza, Innova)")
        nopol = st.text_input("Nomor Polisi (Plat Nomor)")
        harga_sewa = st.number_input("Harga Sewa per Hari (Rp)", min_value=0, step=50000)
        
        if st.button("Simpan Mobil"):
            if nama_mobil and nopol:
                conn = get_connection()
                cursor = conn.cursor()
                # UBAH QUERY INSERT AGAR SESUAI DATABASE:
query = "INSERT INTO mobil (merk, plat_nomor, harga_sewa) VALUES (%s, %s, %s)"
cursor.execute(query, (nama_mobil, nopol, harga_sewa))
                conn.commit()
                conn.close()
                st.success(f"Berhasil menambahkan mobil: {nama_mobil}")
                st.rerun()
            else:
                st.warning("Nama Mobil dan Plat Nomor wajib diisi!")

    # Tampilkan Tabel Mobil
    conn = get_connection()
    try:
        df_mobil = pd.read_sql("SELECT * FROM mobil", conn)
        st.subheader("Daftar Armada Mobil")
        st.dataframe(df_mobil, use_container_width=True)
    except Exception as e:
        st.info("Belum ada data mobil.")
    finally:
        conn.close()

# ==========================================
# 3. MENU TRANSAKSI RENTAL
# ==========================================
elif menu == "Transaksi Rental":
    st.header("Transaksi Peminjaman Mobil")
    
    conn = get_connection()
    df_penyewa = pd.read_sql("SELECT id_penyewa, nama FROM penyewa", conn)
    df_mobil = pd.read_sql("SELECT id_mobil, nama_mobil, nopol, harga_sewa FROM mobil", conn)
    conn.close()
    
    if df_penyewa.empty or df_mobil.empty:
        st.warning("Data Penyewa atau Data Mobil masih kosong! Harap isi dulu di menu Kelola Penyewa / Kelola Mobil.")
    else:
        with st.form("form_transaksi"):
            # Dropdown pilih dari data yang sudah ada di DB
            list_penyewa = {row['id_penyewa']: f"{row['nama']} (ID: {row['id_penyewa']})" for _, row in df_penyewa.iterrows()}
            id_penyewa_terpilih = st.selectbox("Pilih Penyewa", options=list(list_penyewa.keys()), format_func=lambda x: list_penyewa[x])
            
            list_mobil = {row['id_mobil']: f"{row['nama_mobil']} - {row['nopol']} (Rp {row['harga_sewa']:,}/hari)" for _, row in df_mobil.iterrows()}
            id_mobil_terpilih = st.selectbox("Pilih Mobil", options=list(list_mobil.keys()), format_func=lambda x: list_mobil[x])
            
            tgl_sewa = st.date_input("Tanggal Sewa")
            lama_sewa = st.number_input("Lama Sewa (Hari)", min_value=1, value=1)
            
            submit_transaksi = st.form_submit_button("🚗 Proses Transaksi")
            
            if submit_transaksi:
                conn = get_connection()
                cursor = conn.cursor()
                query = "INSERT INTO transaksi (id_penyewa, id_mobil, tgl_sewa, lama_sewa) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (id_penyewa_terpilih, id_mobil_terpilih, tgl_sewa, lama_sewa))
                conn.commit()
                conn.close()
                st.success("Transaksi peminjaman berhasil disimpan!")
                st.rerun()

    st.divider()
    st.subheader("Riwayat Transaksi Rental")
    conn = get_connection()
    query_join = """
    SELECT 
        t.id_transaksi AS 'ID Transaksi',
        p.nama AS 'Nama Penyewa',
        m.nama_mobil AS 'Mobil',
        m.nopol AS 'Plat Nomor',
        t.tgl_sewa AS 'Tanggal Sewa',
        t.lama_sewa AS 'Lama (Hari)',
        (t.lama_sewa * m.harga_sewa) AS 'Total Biaya (Rp)'
    FROM transaksi t
    JOIN penyewa p ON t.id_penyewa = p.id_penyewa
    JOIN mobil m ON t.id_mobil = m.id_mobil
    """
    try:
        df_transaksi = pd.read_sql(query_join, conn)
        st.dataframe(df_transaksi, use_container_width=True)
    except Exception as e:
        st.info("Belum ada data transaksi tersimpan.")
    finally:
        conn.close()