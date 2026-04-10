import streamlit as st

# ==============================
# CONFIG
# ==============================
st.set_page_config(page_title="Sistem Pakar Laptop", layout="wide")

st.title("💻 Sistem Pakar Diagnosa Laptop")
st.write("Pilih gejala yang dialami laptop Anda:")

# ==============================
# GEJALA
# ==============================
gejala = {
    "G1": ("Laptop mulai terasa lambat", "awal"),
    "G2": ("Baterai mulai cepat habis", "awal"),
    "G3": ("Laptop mulai hang ringan", "awal"),
    "G4": ("Kipas mulai sering aktif", "awal"),
    "G5": ("Layar kadang redup/tidak stabil", "awal"),

    "G6": ("Laptop sering freeze", "menengah"),
    "G7": ("Laptop restart sendiri", "menengah"),
    "G8": ("Baterai drop drastis", "menengah"),
    "G9": ("Laptop panas berlebih", "menengah"),
    "G10": ("Kipas sangat berisik", "menengah"),
    "G11": ("Aplikasi sering crash", "menengah"),

    "G12": ("Blue screen (BSOD)", "parah"),
    "G13": ("Laptop mati saat charger dilepas", "parah"),
    "G14": ("Laptop mati mendadak saat panas", "parah"),
    "G15": ("Tidak bisa booting", "parah"),
    "G16": ("Laptop tidak menyala sama sekali (mati total)", "parah"),
    "G17": ("Tidak ada indikator lampu/charging", "parah")
}

# ==============================
# BOBOT LEVEL
# ==============================
level_weight = {
    "awal": 0.5,
    "menengah": 1.0,
    "parah": 1.5
}

# ==============================
# RULE BASE
# ==============================
rules = {
    "RAM": ["G1", "G3", "G6", "G7", "G11", "G12", "G15"],
    "BATTERY": ["G2", "G8", "G13"],
    "OVERHEATING": ["G4", "G9", "G10", "G14"],
    "MATI_TOTAL": ["G5", "G7", "G13", "G16", "G17"]
}

# ==============================
# INIT SESSION STATE
# ==============================
if "checked" not in st.session_state:
    st.session_state.checked = {kode: False for kode in gejala}

# ==============================
# FUNGSI RESET
# ==============================
def reset():
    for k in st.session_state.checked:
        st.session_state.checked[k] = False
    st.rerun()

# ==============================
# UI PEMILIHAN GEJALA
# ==============================
selected = []

st.subheader("Gejala Awal")
cols = st.columns(2)
i = 0
for kode, (desc, level) in gejala.items():
    if level == "awal":
        checked = cols[i % 2].checkbox(
            f"{kode} - {desc}",
            value=st.session_state.checked[kode],
            key=kode
        )
        st.session_state.checked[kode] = checked
        if checked:
            selected.append(kode)
        i += 1

st.subheader("Gejala Menengah")
cols = st.columns(2)
i = 0
for kode, (desc, level) in gejala.items():
    if level == "menengah":
        checked = cols[i % 2].checkbox(
            f"{kode} - {desc}",
            value=st.session_state.checked[kode],
            key=kode
        )
        st.session_state.checked[kode] = checked
        if checked:
            selected.append(kode)
        i += 1

st.subheader("Gejala Parah")
cols = st.columns(2)
i = 0
for kode, (desc, level) in gejala.items():
    if level == "parah":
        checked = cols[i % 2].checkbox(
            f"{kode} - {desc}",
            value=st.session_state.checked[kode],
            key=kode
        )
        st.session_state.checked[kode] = checked
        if checked:
            selected.append(kode)
        i += 1

# ==============================
# TOMBOL AKSI
# ==============================
col1, col2 = st.columns(2)

diagnosa_clicked = col1.button("🔍 Diagnosa")
reset_clicked = col2.button("🔄 Reset")

# ==============================
# PROSES DIAGNOSA
# ==============================
if diagnosa_clicked:

    if not selected:
        st.warning("Pilih minimal satu gejala!")
    else:
        scores = {d: 0 for d in rules}
        max_scores = {d: 0 for d in rules}

        for diagnosis, gej_list in rules.items():
            for g in gej_list:
                level = gejala[g][1]
                max_scores[diagnosis] += level_weight[level]

        for diagnosis, gej_list in rules.items():
            for g in selected:
                if g in gej_list:
                    level = gejala[g][1]
                    scores[diagnosis] += level_weight[level]

        percentages = {
            d: (scores[d] / max_scores[d]) * 100 for d in scores
        }

        st.subheader("📊 Hasil Diagnosa")

        for d, p in percentages.items():
            st.progress(int(p))
            st.write(f"{d}: {p:.2f}%")

        hasil = max(percentages, key=percentages.get)

        if percentages[hasil] < 40:
            kondisi = "Ringan"
        elif percentages[hasil] < 70:
            kondisi = "Sedang"
        else:
            kondisi = "Parah"

        st.success(f"Diagnosa Utama: {hasil}")
        st.info(f"Tingkat Kerusakan: {kondisi}")

        st.subheader("🛠️ Saran")

        if hasil == "RAM":
            st.write("- Bersihkan RAM\n- Upgrade jika perlu")

        elif hasil == "BATTERY":
            st.write("- Ganti baterai\n- Gunakan charger original")

        elif hasil == "OVERHEATING":
            st.write("- Bersihkan kipas\n- Ganti thermal paste")

        elif hasil == "MATI_TOTAL":
            st.write("- Cek adaptor\n- Periksa motherboard")

# ==============================
# RESET ACTION
# ==============================
if reset_clicked:
    reset()