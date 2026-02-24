import streamlit as st
import random
import time
import math
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Book Interaktif Berbasis AI", layout="wide")

# ===============================
# SESSION STATE
# ===============================
if "started" not in st.session_state:
    st.session_state.started = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

# ===============================
# HEADER
# ===============================
st.title("📐 E-Book Interaktif Berbasis Rule-Based ITS")
st.subheader("Tutor Adaptif Teorema Pythagoras (SMP)")

tab1, tab2 = st.tabs(["📘 Latihan", "📊 Tentang Penelitian"])

# ===============================
# TAB LATIHAN
# ===============================
with tab1:

    nama = st.text_input("Masukkan Nama Lengkap Siswa")

    mode = st.radio(
        "Pilih Mode Pembelajaran:",
        ["Mode Penelitian (Tes)", "Mode Tutor AI (Scaffolding)"]
    )

    if st.button("🎲 Mulai Latihan Baru"):
        a = random.randint(3, 9)
        b = random.randint(3, 9)
        st.session_state.a = a
        st.session_state.b = b
        st.session_state.jawaban_benar = math.sqrt(a**2 + b**2)
        st.session_state.started = True
        st.session_state.start_time = time.time()

    if st.session_state.started:

        a = st.session_state.a
        b = st.session_state.b
        jawaban_benar = st.session_state.jawaban_benar

        st.info(f"Diketahui segitiga siku-siku dengan sisi {a} cm dan {b} cm. Berapa panjang sisi miringnya?")

        jawaban = st.text_input("Jawabanmu (dalam cm):")
        confidence = st.slider("Seberapa yakin kamu terhadap jawabanmu? (1-5)", 1, 5, 3)

        if st.button("Kirim"):

            if not nama:
                st.warning("Masukkan nama siswa terlebih dahulu.")
                st.stop()

            try:
                jawaban_float = float(jawaban)
            except:
                st.warning("Masukkan angka yang valid.")
                st.stop()

            waktu_respon = round(time.time() - st.session_state.start_time, 2)
            selisih = abs(jawaban_float - jawaban_benar)

            st.session_state.total += 1

            # ===============================
            # MODE PENELITIAN (TES LANGSUNG)
            # ===============================
            if mode == "Mode Penelitian (Tes)":

                if selisih < 0.01:
                    st.success("✔ Benar. Jawabanmu tepat.")
                    st.session_state.score += 1
                    hasil = "Benar"
                else:
                    st.error(f"✘ Salah. Jawaban yang benar adalah {round(jawaban_benar,2)} cm.")
                    hasil = "Salah"

            # ===============================
            # MODE TUTOR AI (SCAFFOLDING TERSTRUKTUR)
            # ===============================
            else:

                if selisih < 0.01:
                    st.success("🎉 Selamat! Jawabanmu benar.")
                    st.info("Coba jelaskan kembali langkah-langkah yang kamu gunakan untuk menemukan hasil tersebut.")
                    st.session_state.score += 1
                    hasil = "Benar"

                else:
                    hasil = "Salah"

                    # Kategori Kesalahan Konseptual (jauh sekali)
                    if selisih > jawaban_benar * 0.5:
                        st.info("Petunjuk Konsep: Sisi miring adalah sisi yang berhadapan dengan sudut 90° pada segitiga siku-siku.")
                        st.info("Pastikan kamu menggunakan hubungan antara sisi siku-siku dan sisi miring.")

                    # Kesalahan Prosedural (sedang)
                    elif selisih > 1:
                        st.info("Petunjuk Prosedur: Gunakan rumus Teorema Pythagoras → a² + b² = c².")
                        st.info("Hitung kuadrat masing-masing sisi terlebih dahulu, lalu jumlahkan.")

                    # Kesalahan Teknis (kecil)
                    else:
                        st.info("Petunjuk Perhitungan: Setelah menjumlahkan a² + b², jangan lupa mengambil akar kuadratnya.")
                        st.info("Periksa kembali langkah akarmu dengan teliti.")

            st.write(f"Waktu respon: {waktu_respon} detik")
            st.write(f"Skor sementara: {st.session_state.score}/{st.session_state.total}")

            # Simpan ke history
            st.session_state.history.append({
                "Nama": nama,
                "Mode": mode,
                "Sisi_a": a,
                "Sisi_b": b,
                "Jawaban_Siswa": jawaban_float,
                "Jawaban_Benar": round(jawaban_benar,2),
                "Hasil": hasil,
                "Confidence": confidence,
                "Waktu_Respon": waktu_respon
            })

    # ===============================
    # GRAFIK PERFORMA
    # ===============================
    if st.session_state.history:

        st.markdown("## 📈 Grafik Performa")

        df = pd.DataFrame(st.session_state.history)

        benar_count = len(df[df["Hasil"] == "Benar"])
        salah_count = len(df[df["Hasil"] == "Salah"])

        fig, ax = plt.subplots()
        ax.bar(["Benar", "Salah"], [benar_count, salah_count])
        ax.set_ylabel("Jumlah")
        ax.set_title("Performa Jawaban")

        st.pyplot(fig)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export Data CSV",
            csv,
            "data_penelitian_pythagoras.csv",
            "text/csv"
        )

# ===============================
# TAB PENELITIAN
# ===============================
with tab2:
    st.markdown("""
    Aplikasi ini dikembangkan sebagai bagian dari penelitian pengembangan (R&D) 
    untuk menghasilkan e-book interaktif berbasis Rule-Based Intelligent Tutoring System.

    Fitur utama:
    1. Mode Penelitian (Tes langsung dengan evaluasi hasil).
    2. Mode Tutor AI (Scaffolding terstruktur berbasis tingkat kesalahan siswa).

    Sistem Tutor AI mengklasifikasikan kesalahan siswa menjadi:
    - Kesalahan Konseptual
    - Kesalahan Prosedural
    - Kesalahan Teknis

    Data yang dikumpulkan:
    - Nama siswa
    - Mode pembelajaran
    - Jawaban siswa
    - Confidence level
    - Waktu respon
    - Hasil benar/salah

    Data dapat diekspor dalam format CSV untuk analisis lebih lanjut.
    """)
