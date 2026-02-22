import streamlit as st
import random
import time
import pandas as pd
import os
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
if "mistakes" not in st.session_state:
    st.session_state.mistakes = {"Definisi": 0, "Rumus": 0, "Kuadrat": 0, "Akar": 0}
if "responses" not in st.session_state:
    st.session_state.responses = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None

# ===============================
# HEADER
# ===============================
st.title("📐 E-Book Interaktif Berbasis AI")
st.subheader("Tutor Adaptif Teorema Pythagoras (SMP)")

tabs = st.tabs(["📘 Latihan", "📊 Tentang Penelitian"])

# ===============================
# TAB LATIHAN
# ===============================
with tabs[0]:

    student_name = st.text_input("Masukkan Nama Lengkap Siswa")

    if st.button("🎲 Mulai Latihan Baru"):
        if student_name.strip() == "":
            st.warning("Nama siswa wajib diisi.")
        else:
            st.session_state.started = True
            st.session_state.start_time = time.time()

    if st.session_state.started:

        a = random.randint(3, 9)
        b = random.randint(3, 9)
        c_squared = a*a + b*b

        st.info(f"Diketahui segitiga siku-siku dengan sisi {a} dan {b}. Berapa panjang sisi miringnya?")

        answer = st.text_input("Jawabanmu:")
        confidence = st.slider("Seberapa yakin kamu terhadap jawabanmu? (1-5)", 1, 5, 3)

        if st.button("Kirim"):
            response_time = round(time.time() - st.session_state.start_time, 2)
            st.session_state.total += 1

            try:
                correct = round(c_squared**0.5, 2)
                user_answer = round(float(answer), 2)

                if user_answer == correct:
                    st.success("Benar! 🎉")
                    st.session_state.score += 1
                    result = "Benar"
                else:
                    st.warning(f"Salah. Jawaban yang benar adalah {correct}")
                    result = "Salah"
                    st.session_state.mistakes["Kuadrat"] += 1

            except:
                st.warning("Masukkan angka yang valid.")
                result = "Error"

            # Simpan data
            data_row = {
                "Nama": student_name,
                "Sisi_A": a,
                "Sisi_B": b,
                "Jawaban_Siswa": answer,
                "Jawaban_Benar": correct,
                "Hasil": result,
                "Confidence": confidence,
                "Waktu_Respon_Detik": response_time
            }

            st.session_state.responses.append(data_row)

            # Simpan ke CSV
            df = pd.DataFrame(st.session_state.responses)
            df.to_csv("data_penelitian.csv", index=False)

            st.write(f"Waktu respon: {response_time} detik")
            st.progress(st.session_state.score / st.session_state.total)

        st.write(f"Skor: {st.session_state.score}/{st.session_state.total}")

        # ===============================
        # GRAFIK PERFORMA
        # ===============================
        if st.session_state.total > 0:
            st.subheader("Grafik Performa")

            benar = st.session_state.score
            salah = st.session_state.total - st.session_state.score

            fig, ax = plt.subplots()
            ax.bar(["Benar", "Salah"], [benar, salah])
            st.pyplot(fig)

        # ===============================
        # DOWNLOAD CSV
        # ===============================
        if os.path.exists("data_penelitian.csv"):
            with open("data_penelitian.csv", "rb") as f:
                st.download_button(
                    label="Download Data Penelitian (CSV)",
                    data=f,
                    file_name="data_penelitian.csv",
                    mime="text/csv"
                )

# ===============================
# TAB TENTANG PENELITIAN
# ===============================
with tabs[1]:

    st.header("Tentang Penelitian")

    st.write("""
    Aplikasi ini dikembangkan sebagai media pembelajaran berbasis AI 
    untuk mengukur pemahaman konsep Teorema Pythagoras pada siswa SMP.

    Sistem ini mengukur:
    - Ketepatan jawaban
    - Tingkat kepercayaan diri (confidence)
    - Waktu respon siswa

    Data yang dikumpulkan digunakan untuk analisis peningkatan 
    pemahaman konsep matematika melalui pendekatan adaptif.
    """)

    st.write("Penelitian ini menggunakan desain pretest-posttest untuk mengukur efektivitas media.")
