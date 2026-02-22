import streamlit as st
import re
import math
import random
import csv
import os
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="AI Tutor Pythagoras", layout="centered")

st.title("📐 E-Book Interaktif Berbasis AI")
st.subheader("Tutor Adaptif Teorema Pythagoras (SMP)")

# ======================
# SESSION STATE
# ======================
if "level" not in st.session_state:
    st.session_state.level = 0
    st.session_state.a = None
    st.session_state.b = None
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.history = []
    st.session_state.difficulty_level = 1
    st.session_state.start_time = None

# ======================
# FUNGSI BANTUAN
# ======================
def extract_numbers(text):
    return list(map(int, re.findall(r"\d+", text)))

def generate_problem():
    level = st.session_state.difficulty_level
    
    if level == 1:
        triples = [(3,4),(5,12),(8,15)]
        st.session_state.a, st.session_state.b = random.choice(triples)
    elif level == 2:
        st.session_state.a = random.randint(3,12)
        st.session_state.b = random.randint(3,12)
    else:
        triples = [(5,13),(9,15),(7,25)]
        pair = random.choice(triples)
        st.session_state.b = pair[1]
        st.session_state.a = pair[0]
    
    st.session_state.level = 1
    st.session_state.start_time = time.time()

def save_to_csv(a,b,answer,correct,confidence):
    file_exists = os.path.isfile("log_data.csv")
    with open("log_data.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["sisi_a","sisi_b","jawaban","benar","confidence"])
        writer.writerow([a,b,answer,correct,confidence])

# ======================
# TOMBOL LATIHAN
# ======================
if st.button("🎲 Mulai Latihan Baru"):
    generate_problem()
    st.info(f"Diketahui segitiga siku-siku dengan sisi {st.session_state.a} dan {st.session_state.b}. Segitiga ini disebut apa?")

# ======================
# INPUT JAWABAN
# ======================
user_input = st.text_input("Jawabanmu:")
confidence = st.slider("Seberapa yakin kamu terhadap jawabanmu? (1-5)",1,5,3)

# ======================
# LOGIKA TAHAP
# ======================
if st.button("Kirim"):

    if st.session_state.level == 1:
        if "siku" in user_input.lower():
            st.success("Benar. Tuliskan rumus Pythagoras.")
            st.session_state.level = 2
        else:
            st.warning("Perhatikan sudut 90°.")
            st.session_state.history.append("Definisi")

    elif st.session_state.level == 2:
        if "kuadrat" in user_input.lower() or "^2" in user_input:
            st.success("Bagus. Hitung kuadrat kedua sisi.")
            st.session_state.level = 3
        else:
            st.warning("Rumus berbentuk kuadrat.")
            st.session_state.history.append("Rumus")

    elif st.session_state.level == 3:
        numbers = extract_numbers(user_input)
        correct_a = st.session_state.a**2
        correct_b = st.session_state.b**2

        if correct_a in numbers and correct_b in numbers:
            st.success("Benar. Sekarang jumlahkan.")
            st.session_state.level = 4
        else:
            st.warning("Kuadrat belum tepat.")
            st.session_state.history.append("Kuadrat")

    elif st.session_state.level == 4:
        try:
            total = int(user_input)
            if total == st.session_state.a**2 + st.session_state.b**2:
                st.success("Benar. Sekarang cari akar kuadratnya.")
                st.session_state.level = 5
            else:
                st.warning("Penjumlahan salah.")
                st.session_state.history.append("Penjumlahan")
        except:
            st.warning("Masukkan angka.")

    elif st.session_state.level == 5:
        try:
            answer = float(user_input)
            correct_value = math.sqrt(st.session_state.a**2 + st.session_state.b**2)
            response_time = round(time.time() - st.session_state.start_time,2)

            st.session_state.total += 1

            if math.isclose(answer, correct_value, rel_tol=1e-2):
                st.success("🎉 Jawaban benar!")
                st.session_state.score += 1
                correct=True

                if confidence >=4:
                    st.info("Diagnostik: Penguasaan kuat.")
                else:
                    st.info("Diagnostik: Benar tetapi keyakinan rendah (pemahaman rapuh).")

            else:
                st.error(f"Jawaban kurang tepat. Nilai benar ≈ {round(correct_value,3)}")
                correct=False

                if confidence >=4:
                    st.warning("Diagnostik: Miskonsepsi kuat (yakin tetapi salah).")
                else:
                    st.warning("Diagnostik: Belum memahami konsep.")

            save_to_csv(st.session_state.a,st.session_state.b,answer,correct,confidence)

            # ADAPTASI KESULITAN
            mastery = st.session_state.score / st.session_state.total
            if mastery >=0.8:
                st.session_state.difficulty_level = min(3, st.session_state.difficulty_level+1)
            elif mastery <0.4:
                st.session_state.difficulty_level = 1

            st.write(f"Waktu respon: {response_time} detik")
            st.session_state.level = 0

        except:
            st.warning("Masukkan angka.")

# ======================
# PROGRESS
# ======================
if st.session_state.total >0:
    mastery = st.session_state.score / st.session_state.total
    st.progress(mastery)
    st.write(f"Skor: {st.session_state.score}/{st.session_state.total}")

    st.subheader("Profil Pemahaman Sementara")
    if mastery>=0.8:
        st.write("Tingkat penguasaan: Tinggi")
    elif mastery>=0.5:
        st.write("Tingkat penguasaan: Sedang")
    else:
        st.write("Tingkat penguasaan: Rendah")

# ======================
# ANALISIS KESALAHAN
# ======================
if st.session_state.history:
    st.subheader("Analisis Kesalahan")
    counter = Counter(st.session_state.history)
    for key,value in counter.items():
        st.write(f"{key}: {value} kali")

# ======================
# GRAFIK PERFORMA
# ======================
if os.path.isfile("log_data.csv"):
    df = pd.read_csv("log_data.csv")
    benar = df["benar"].sum()
    salah = len(df) - benar

    st.subheader("Grafik Performa")
    fig, ax = plt.subplots()
    ax.bar(["Benar","Salah"], [benar,salah])
    ax.set_ylabel("Jumlah")
    st.pyplot(fig)