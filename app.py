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
st.title("📐 E-Book Interaktif Berbasis AI")
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

        st.info(f"Diketahui segitiga siku-siku dengan sisi {a} dan {b}. Berapa panjang sisi miringnya?")

        jawaban = st.text_input("Jawabanmu:")

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
            # MODE PENELITIAN
            # ===============================
            if mode == "Mode Penelitian (Tes)":

                if selisih < 0.01:
                    st.success("Benar.")
                    st.session_state.score += 1
                    hasil = "Benar"
                else:
                    st.error(f"Salah. Jawaban yang benar adalah {round(jawaban_benar,2)}")
                    hasil = "Salah"

            # ===============================
            # MODE TUTOR AI
            # ===============================
            else:

                if selisih < 0.01:
                    st.success("Bagus! Jawabanmu benar. Sekarang coba jelaskan langkahnya.")
                    st.session_state.score += 1
                    hasil = "Benar"
                else:
                    hasil = "Salah"

                    if selisih > 5:
                        st.info("Petunjuk 1: Sisi miring selalu berhadapan dengan sudut 90°.")
                    elif selisih > 1:
                        st.info("Petunjuk 2: Gunakan rumus Pythagoras → a² + b² = c²")
                    else:
                        st.info("Petunjuk 3: Hitung √(a² + b²). Periksa kembali perhitungan akarmu.")

            st.write(f"Waktu respon: {waktu_respon} detik")
            st.write(f"Skor: {st.session_state.score}/{st.session_state.total}")

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

        # Export CSV
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
    st.markdown("## 📊 Tentang Penelitian")

    st.markdown("""
    Aplikasi ini dirancang untuk menguji efektivitas dua pendekatan pembelajaran:

    1. Mode Penelitian (Tes langsung dengan evaluasi hasil)
    2. Mode Tutor AI (Scaffolding bertahap berbasis petunjuk)

    Data yang dikumpulkan:
    - Nama siswa
    - Mode pembelajaran
    - Jawaban siswa
    - Confidence level
    - Waktu respon
    - Hasil benar/salah

    Data dapat diekspor dalam format CSV untuk analisis statistik.
    """)
