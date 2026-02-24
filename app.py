import streamlit as st
import random
import time
import math
import pandas as pd
import matplotlib.pyplot as plt
import re

st.set_page_config(page_title="E-Book Interaktif Berbasis AI", layout="wide")

# ===============================
# SESSION STATE
# ===============================
if "score" not in st.session_state:
    st.session_state.score = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "history" not in st.session_state:
    st.session_state.history = []

if "start_time" not in st.session_state:
    st.session_state.start_time = 0

if "tutor_state" not in st.session_state:
    st.session_state.tutor_state = 0

if "tutor_values" not in st.session_state:
    st.session_state.tutor_values = {}

# ===============================
# FUNGSI BANTU
# ===============================

def normalize_input(text):
    text = text.lower()
    text = text.replace("²", "^2")
    text = text.replace("√", "sqrt")
    text = text.replace("akar", "sqrt")
    return text

def extract_numbers(text):
    return re.findall(r"[-+]?\d*\.\d+|\d+", text)

def contains_pythagoras_keyword(text):
    keywords = ["sisi", "miring", "siku", "hipotenusa", "pythagoras", "segitiga"]
    return any(k in text.lower() for k in keywords)

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

    # ===============================
    # MODE PENELITIAN (TETAP)
    # ===============================
    if mode == "Mode Penelitian (Tes)":

        if st.button("🎲 Mulai Latihan Baru"):
            a = random.randint(3, 9)
            b = random.randint(3, 9)
            st.session_state.a = a
            st.session_state.b = b
            st.session_state.jawaban_benar = math.sqrt(a**2 + b**2)
            st.session_state.start_time = time.time()

        if "a" in st.session_state:

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

                if selisih < 0.01:
                    st.success("Benar.")
                    st.session_state.score += 1
                    hasil = "Benar"
                else:
                    st.error(f"Salah. Jawaban yang benar adalah {round(jawaban_benar,2)}")
                    hasil = "Salah"

                st.write(f"Waktu respon: {waktu_respon} detik")
                st.write(f"Skor: {st.session_state.score}/{st.session_state.total}")

                st.session_state.history.append({
                    "Nama": nama,
                    "Mode": mode,
                    "Sisi_a": a,
                    "Sisi_b": b,
                    "Jawaban_Siswa": jawaban,
                    "Jawaban_Benar": round(jawaban_benar,2),
                    "Hasil": hasil,
                    "Confidence": confidence,
                    "Waktu_Respon": waktu_respon
                })

    # ===============================
    # MODE TUTOR AI (BERBASIS PERTANYAAN SISWA)
    # ===============================
    else:

        st.info("Silakan ajukan pertanyaan terkait Teorema Pythagoras.")

        user_input = st.text_input("Tuliskan pertanyaanmu:")
        confidence = st.slider("Seberapa yakin kamu terhadap pemahamanmu? (1-5)", 1, 5, 3)

        if st.button("Kirim"):

            if not nama:
                st.warning("Masukkan nama siswa terlebih dahulu.")
                st.stop()

            if not contains_pythagoras_keyword(user_input):
                st.info("Pertanyaan di luar materi Teorema Pythagoras. Silakan ajukan pertanyaan tentang panjang sisi segitiga siku-siku.")
                st.stop()

            nums = extract_numbers(user_input)

            # Tahap awal: ekstrak angka dari pertanyaan
            if st.session_state.tutor_state == 0:

                if len(nums) >= 2:
                    a = float(nums[0])
                    b = float(nums[1])
                    jawaban_benar = math.sqrt(a**2 + b**2)

                    st.session_state.tutor_values = {
                        "a": a,
                        "b": b,
                        "hasil": jawaban_benar
                    }

                    st.session_state.tutor_state = 1
                    st.success("Baik. Rumus apa yang digunakan untuk mencari sisi miring?")
                else:
                    st.info("Sebutkan dua panjang sisi yang diketahui pada segitiga siku-siku.")
                return

            # Tahap rumus
            if st.session_state.tutor_state == 1:
                norm = normalize_input(user_input)
                if "a^2" in norm and "b^2" in norm:
                    st.session_state.tutor_state = 2
                    st.success("Bagus. Sekarang hitung nilai kuadrat masing-masing sisi.")
                else:
                    st.info("Ingat hubungan antara sisi siku-siku dan sisi miring.")
                return

            # Tahap kuadrat
            if st.session_state.tutor_state == 2:
                nums = extract_numbers(user_input)
                a = st.session_state.tutor_values["a"]
                b = st.session_state.tutor_values["b"]

                if str(int(a**2)) in nums and str(int(b**2)) in nums:
                    st.session_state.tutor_state = 3
                    st.success("Tepat. Sekarang jumlahkan hasil kuadrat tersebut.")
                else:
                    st.info("Periksa kembali hasil kuadrat masing-masing sisi.")
                return

            # Tahap penjumlahan
            if st.session_state.tutor_state == 3:
                nums = extract_numbers(user_input)
                a = st.session_state.tutor_values["a"]
                b = st.session_state.tutor_values["b"]

                if str(int(a**2 + b**2)) in nums:
                    st.session_state.tutor_state = 4
                    st.success("Bagus. Langkah terakhir apa yang harus dilakukan?")
                else:
                    st.info("Jumlahkan hasil kuadrat tadi terlebih dahulu.")
                return

            # Tahap akar
            if st.session_state.tutor_state == 4:
                nums = extract_numbers(user_input)
                hasil = st.session_state.tutor_values["hasil"]

                if nums and abs(float(nums[0]) - hasil) < 0.01:
                    st.success("🎉 Selamat! Kamu berhasil menemukan jawabannya melalui langkah yang benar dan sistematis.")
                    st.session_state.score += 1
                    st.session_state.total += 1
                    st.session_state.tutor_state = 0
                else:
                    st.info("Ambil akar dari hasil penjumlahan tersebut.")
                return

    # ===============================
    # GRAFIK
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

# ===============================
# TAB PENELITIAN
# ===============================
with tab2:
    st.markdown("""
    Aplikasi ini memiliki dua mode pembelajaran:

    1. Mode Penelitian (Tes langsung dengan evaluasi hasil).
    2. Mode Tutor AI berbasis dialog scaffolding yang menuntun siswa tanpa memberikan jawaban langsung.

    Sistem Tutor AI hanya merespons pertanyaan terkait Teorema Pythagoras.
    """)
