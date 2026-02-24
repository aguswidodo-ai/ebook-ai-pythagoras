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

if "tutor_state" not in st.session_state:
    st.session_state.tutor_state = 0

# ===============================
# FUNGSI BANTU
# ===============================

def normalize_input(text):
    text = text.lower()
    text = text.replace("²", "^2")
    text = text.replace("√", "sqrt")
    text = text.replace("akar", "sqrt")
    text = text.replace(" ", "")
    return text

def extract_numbers(text):
    return re.findall(r"[-+]?\d*\.\d+|\d+", text)

def contains_pythagoras_keyword(text):
    keywords = ["sisi", "miring", "siku", "hipotenusa", "pythagoras", "akar", "kuadrat"]
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

    if st.button("🎲 Mulai Latihan Baru"):
        a = random.randint(3, 9)
        b = random.randint(3, 9)
        st.session_state.a = a
        st.session_state.b = b
        st.session_state.jawaban_benar = math.sqrt(a**2 + b**2)
        st.session_state.started = True
        st.session_state.start_time = time.time()
        st.session_state.tutor_state = 0

    if st.session_state.started:

        a = st.session_state.a
        b = st.session_state.b
        jawaban_benar = st.session_state.jawaban_benar

        st.info(f"Diketahui segitiga siku-siku dengan sisi {a} dan {b}. Berapa panjang sisi miringnya?")

        jawaban = st.text_input("Masukkan jawaban atau pertanyaanmu:")
        confidence = st.slider("Seberapa yakin kamu terhadap jawabanmu? (1-5)", 1, 5, 3)

        if st.button("Kirim"):

            if not nama:
                st.warning("Masukkan nama siswa terlebih dahulu.")
                st.stop()

            waktu_respon = round(time.time() - st.session_state.start_time, 2)
            st.session_state.total += 1

            # ===============================
            # MODE PENELITIAN (TETAP)
            # ===============================
            if mode == "Mode Penelitian (Tes)":

                try:
                    jawaban_float = float(jawaban)
                except:
                    st.warning("Masukkan angka yang valid.")
                    st.stop()

                selisih = abs(jawaban_float - jawaban_benar)

                if selisih < 0.01:
                    st.success("Benar.")
                    st.session_state.score += 1
                    hasil = "Benar"
                else:
                    st.error(f"Salah. Jawaban yang benar adalah {round(jawaban_benar,2)}")
                    hasil = "Salah"

            # ===============================
            # MODE TUTOR AI (SCaffolding Baru)
            # ===============================
            else:

                user_input = normalize_input(jawaban)

                if not contains_pythagoras_keyword(jawaban):
                    st.info("Pertanyaan tersebut di luar materi Teorema Pythagoras. Mari kembali fokus pada panjang sisi segitiga siku-siku.")
                    hasil = "Proses"

                else:

                    # Tahap 0: Tanya rumus
                    if st.session_state.tutor_state == 0:
                        if "a^2" in user_input and "b^2" in user_input and "+" in user_input:
                            st.success("Bagus. Sekarang hitung nilai a² dan b² terlebih dahulu.")
                            st.session_state.tutor_state = 1
                        else:
                            st.info("Untuk menghitung sisi miring, rumus apa yang digunakan?")
                        hasil = "Proses"

                    # Tahap 1: Kuadrat
                    elif st.session_state.tutor_state == 1:
                        nums = extract_numbers(user_input)
                        if str(a**2) in nums and str(b**2) in nums:
                            st.success("Tepat sekali. Sekarang jumlahkan hasil kuadrat tersebut.")
                            st.session_state.tutor_state = 2
                        else:
                            st.info("Coba hitung nilai a² dan b² dengan benar.")
                        hasil = "Proses"

                    # Tahap 2: Penjumlahan
                    elif st.session_state.tutor_state == 2:
                        nums = extract_numbers(user_input)
                        if str(a**2 + b**2) in nums:
                            st.success("Bagus. Langkah terakhir apa yang harus dilakukan?")
                            st.session_state.tutor_state = 3
                        else:
                            st.info("Jumlahkan hasil kuadrat a² dan b² terlebih dahulu.")
                        hasil = "Proses"

                    # Tahap 3: Akar
                    elif st.session_state.tutor_state == 3:
                        nums = extract_numbers(user_input)
                        try:
                            if nums and abs(float(nums[0]) - jawaban_benar) < 0.01:
                                st.success("🎉 Selamat! Kamu berhasil menemukan jawaban dengan langkah yang sistematis dan benar. Terus pertahankan cara berpikirmu!")
                                st.session_state.score += 1
                                hasil = "Benar"
                                st.session_state.tutor_state = 0
                            else:
                                st.info("Ambil akar dari hasil penjumlahan tadi.")
                                hasil = "Proses"
                        except:
                            st.info("Periksa kembali langkah terakhirmu.")
                            hasil = "Proses"

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
    st.markdown("## 📊 Tentang Penelitian")
    st.markdown("""
    Aplikasi ini memiliki dua mode pembelajaran:

    1. Mode Penelitian (Tes langsung dengan evaluasi hasil).
    2. Mode Tutor AI (Scaffolding interaktif bertahap tanpa memberikan jawaban langsung).

    Data yang dikumpulkan:
    - Nama siswa
    - Mode pembelajaran
    - Jawaban siswa
    - Confidence level
    - Waktu respon
    - Hasil benar/salah

    Data dapat diekspor dalam format CSV untuk analisis statistik.
    """)
