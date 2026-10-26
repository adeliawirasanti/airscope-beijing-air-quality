
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from html import escape

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AirScope | Beijing Air Quality",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. PREMIUM DARK THEME
# =====================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #081321, #0D1D30);
    color: #EFF7FF;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #102236;
    border-right: 1px solid #294256;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #F4FAFF !important;
}

[data-testid="stMetric"] {
    background: #152B40;
    border: 1px solid #294559;
    border-radius: 16px;
    padding: 18px;
}

[data-testid="stMetricValue"] {
    color: #67E6C7;
}

[data-testid="stMetricLabel"] {
    color: #B9CEE0;
}

[data-testid="stTabs"] button {
    font-weight: 600;
}

.hero {
    background: linear-gradient(
        110deg, #123B4A, #123049, #192747
    );
    border: 1px solid #285168;
    border-radius: 22px;
    padding: 36px 32px;
    margin-bottom: 22px;
}

.eyebrow {
    color: #62E4C7;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero-title {
    font-size: clamp(32px, 4vw, 52px);
    line-height: 1.15;
    font-weight: 800;
    color: #FFFFFF;
    margin: 14px 0;
    letter-spacing: -1px;
}

.accent {
    color: #62E4C7;
}

.hero-desc {
    font-size: 15px;
    line-height: 1.8;
    color: #C3D5E5;
    max-width: 820px;
}

.kpi-card {
    background: #152B40;
    border: 1px solid #2B485D;
    border-radius: 17px;
    padding: 20px;
    min-height: 142px;
}

.kpi-label {
    color: #B9CEE0;
    font-size: 11px;
    letter-spacing: 1px;
    font-weight: 700;
    text-transform: uppercase;
}

.kpi-value {
    color: #F5FBFF;
    font-size: clamp(22px, 2.5vw, 34px);
    font-weight: 800;
    margin: 14px 0 6px;
    overflow-wrap: anywhere;
}

.kpi-note {
    color: #68E0C5;
    font-size: 12px;
}

.insight-card {
    background: #142D40;
    border-left: 4px solid #62E4C7;
    border-radius: 13px;
    padding: 20px;
    margin: 14px 0;
    color: #D6E5F0;
    line-height: 1.7;
}

.section-caption {
    color: #A8BED0;
    font-size: 13px;
    margin-bottom: 18px;
}

.footer {
    color: #9CB3C8;
    font-size: 12px;
    text-align: center;
    padding-top: 26px;
    line-height: 1.8;
}

div[data-testid="stAlert"] {
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 3. LOAD DATA
# =====================================================

DATA_PATH = Path(__file__).resolve().parent / "main_data.csv"

@st.cache_data(show_spinner="Memuat dataset Air Quality...")
def load_data():
    data = pd.read_csv(DATA_PATH)

    required = [
        "station", "year", "month", "day", "hour", "PM2.5"
    ]

    missing_columns = [
        col for col in required if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Kolom tidak ditemukan: {missing_columns}"
        )

    data["datetime"] = pd.to_datetime(
        data[["year", "month", "day", "hour"]],
        errors="coerce"
    )

    return data

try:
    df = load_data()
except (FileNotFoundError, ValueError) as error:
    st.error(f"Gagal memuat data: {error}")
    st.stop()

df = df.dropna(subset=["datetime"]).copy()

if df.empty:
    st.error("Dataset tidak memiliki tanggal yang valid.")
    st.stop()

# =====================================================
# 4. SIDEBAR FILTERS
# =====================================================

with st.sidebar:
    st.title("🌍 AirScope.")
    st.caption("BEIJING AIR QUALITY INTELLIGENCE")

    st.divider()

    st.subheader("Explore Your Data")

    station_options = ["Semua Stasiun"] + sorted(
        df["station"].dropna().unique().tolist()
    )

    selected_station = st.selectbox(
        "📍 Pilih Stasiun",
        options=station_options
    )

    min_date = df["datetime"].min().date()
    max_date = df["datetime"].max().date()

    # FILTER TANGGAL BARU
    # Menggunakan dua input tanggal terpisah

    start_date = st.date_input(
        "📅 Tanggal Mulai",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        format="DD/MM/YYYY",
        key="start_date"
    )

    end_date = st.date_input(
        "📅 Tanggal Akhir",
        value=max_date,
        min_value=start_date,
        max_value=max_date,
        format="DD/MM/YYYY",
        key="end_date"
    )

    st.divider()

    st.caption("DATASET INFORMATION")
    st.write("📍 Beijing, China")
    st.write("🏢 12 monitoring stations")
    st.write("🕒 Hourly observations")

    st.divider()

    st.info(
        "Dashboard proyek analisis data Dicoding. "
        "Data bersifat historis, bukan real-time."
    )

# =====================================================
# 5. APPLY FILTERS
# =====================================================

filtered_df = df.copy()

# Filter berdasarkan stasiun
if selected_station != "Semua Stasiun":
    filtered_df = filtered_df[
        filtered_df["station"] == selected_station
    ]

# FILTER TANGGAL BARU
# Memastikan tanggal mulai tidak melebihi tanggal akhir
if start_date > end_date:
    st.error(
        "Tanggal mulai tidak boleh melebihi tanggal akhir."
    )
    st.stop()

# Menerapkan filter berdasarkan tanggal mulai dan akhir
filtered_df = filtered_df[
    filtered_df["datetime"].dt.date.between(
        start_date, end_date
    )
]

if filtered_df.empty:
    st.warning(
        "Tidak ada data untuk kombinasi filter ini. "
        "Silakan ubah stasiun atau periode."
    )
    st.stop()

# =====================================================
# 6. CALCULATE METRICS
# =====================================================

total_stations = filtered_df["station"].nunique()
total_records = len(filtered_df)
valid_pm25 = filtered_df["PM2.5"].count()
average_pm25 = filtered_df["PM2.5"].mean()

missing_pm25 = filtered_df["PM2.5"].isna().sum()

pm25_station = (
    filtered_df.groupby("station")["PM2.5"]
    .mean()
    .dropna()
    .sort_values(ascending=False)
)

pm25_month = (
    filtered_df.groupby("month")["PM2.5"]
    .mean()
    .reindex(range(1, 13))
)

# =====================================================
# 7. HERO HEADER
# =====================================================

hero_html = (
    '<div class="hero">'
    '<div class="eyebrow">ENVIRONMENTAL ANALYTICS PLATFORM</div>'
    '<div class="hero-title">'
    'Explore the air.<br>'
    '<span class="accent">Reveal the patterns.</span>'
    '</div>'
    '<div class="hero-desc">'
    'Eksplorasi konsentrasi PM2.5 dari 12 stasiun pemantauan '
    'di Beijing selama Maret 2013 hingga Februari 2017. '
    'Temukan pola berdasarkan lokasi, waktu, dan distribusi '
    'pengukuran melalui visualisasi data interaktif.'
    '</div>'
    '</div>'
)

st.markdown(hero_html, unsafe_allow_html=True)

st.subheader("Environmental Overview")

st.caption(
    f"Stasiun: {selected_station} | "
    f"Pengamatan: {total_records:,} baris"
)

# =====================================================
# 8. KPI CARDS
# =====================================================

def metric_card(label, value, note):
    return (
        '<div class="kpi-card">'
        f'<div class="kpi-label">{escape(str(label))}</div>'
        f'<div class="kpi-value">{escape(str(value))}</div>'
        f'<div class="kpi-note">{escape(str(note))}</div>'
        '</div>'
    )

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        metric_card(
            "Monitoring Stations",
            total_stations,
            "Locations selected"
        ),
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        metric_card(
            "Total Records",
            f"{total_records:,}",
            "Hourly observations"
        ),
        unsafe_allow_html=True
    )

with k3:
    avg_label = (
        f"{average_pm25:.2f}"
        if pd.notna(average_pm25)
        else "N/A"
    )

    st.markdown(
        metric_card(
            "Average PM2.5",
            avg_label,
            "µg/m³"
        ),
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        metric_card(
            "Valid PM2.5",
            f"{valid_pm25:,}",
            f"{missing_pm25:,} values missing"
        ),
        unsafe_allow_html=True
    )

st.write("")

# =====================================================
# 9. CHART STYLING HELPER
# =====================================================

BG = "#102338"
GREEN = "#62E4C7"
BLUE = "#4C86BB"
ORANGE = "#F28B67"
TEXT = "#EDF5FC"

def style_chart(ax):
    ax.set_facecolor(BG)
    ax.figure.set_facecolor(BG)

    ax.tick_params(colors=TEXT)

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.grid(
        axis="x",
        linestyle="--",
        alpha=0.16,
        color="white"
    )

    ax.set_axisbelow(True)

    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    ax.title.set_color(TEXT)

# =====================================================
# 10. NAVIGATION TABS
# =====================================================

tab1, tab2, tab3 = st.tabs([
    "📍 Station Analysis",
    "📅 Monthly Patterns",
    "📊 Pollution Distribution"
])

# =====================================================
# 11. TAB 1 - STATION ANALYSIS
# =====================================================

with tab1:
    st.subheader("PM2.5 Across Monitoring Stations")

    st.markdown(
        '<div class="section-caption">'
        'Perbandingan rata-rata konsentrasi PM2.5 '
        'berdasarkan lokasi pemantauan.'
        '</div>',
        unsafe_allow_html=True
    )

    if not pm25_station.empty:
        station_sorted = pm25_station.sort_values()

        fig, ax = plt.subplots(
            figsize=(11, 6.5),
            facecolor=BG
        )

        colors = [
            ORANGE if station == pm25_station.idxmax()
            else BLUE
            for station in station_sorted.index
        ]

        bars = ax.barh(
            station_sorted.index,
            station_sorted.values,
            color=colors,
            height=0.65
        )

        for bar in bars:
            width = bar.get_width()

            ax.text(
                width + 0.6,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.2f}",
                va="center",
                color=TEXT,
                fontsize=9
            )

        ax.set_xlabel("Average PM2.5 (µg/m³)")
        ax.set_ylabel("Monitoring Station")

        ax.set_xlim(
            0,
            max(station_sorted.max() * 1.18, 1)
        )

        style_chart(ax)

        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        highest_station = pm25_station.idxmax()
        highest_value = pm25_station.max()

        st.markdown(
            '<div class="insight-card">'
            '<b>Key Finding</b><br>'
            f'{escape(str(highest_station))} memiliki rata-rata '
            f'PM2.5 tertinggi pada data terpilih, yaitu '
            f'<b>{highest_value:.2f} µg/m³</b>.'
            '</div>',
            unsafe_allow_html=True
        )

    else:
        st.info("Tidak terdapat data PM2.5 valid.")

# =====================================================
# 12. TAB 2 - MONTHLY PATTERNS
# =====================================================

with tab2:
    st.subheader("Monthly PM2.5 Concentration")

    st.markdown(
        '<div class="section-caption">'
        'Pola rata-rata berdasarkan bulan kalender '
        'dari data yang dipilih.'
        '</div>',
        unsafe_allow_html=True
    )

    month_labels = [
        "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
        "Jul", "Agu", "Sep", "Okt", "Nov", "Des"
    ]

    monthly_valid = pm25_month.dropna()

    if not monthly_valid.empty:
        fig, ax = plt.subplots(
            figsize=(11, 5.5),
            facecolor=BG
        )

        x_positions = monthly_valid.index.to_numpy() - 1

        ax.plot(
            x_positions,
            monthly_valid.values,
            color=GREEN,
            linewidth=2.8,
            marker="o",
            markersize=7
        )

        highest_month = monthly_valid.idxmax()
        lowest_month = monthly_valid.idxmin()

        ax.scatter(
            highest_month - 1,
            monthly_valid.max(),
            color=ORANGE,
            s=120,
            zorder=5
        )

        ax.scatter(
            lowest_month - 1,
            monthly_valid.min(),
            color=BLUE,
            s=120,
            zorder=5
        )

        ax.set_xticks(range(12))
        ax.set_xticklabels(month_labels)

        ax.set_xlim(-0.4, 11.4)
        ax.set_ylim(
            0,
            max(monthly_valid.max() * 1.2, 1)
        )

        ax.set_ylabel("Average PM2.5 (µg/m³)")

        style_chart(ax)

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.16,
            color="white"
        )

        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        st.markdown(
            '<div class="insight-card">'
            '<b>Monthly Insight</b><br>'
            f'Bulan {month_labels[highest_month - 1]} memiliki '
            f'rata-rata PM2.5 tertinggi pada data terpilih '
            f'({monthly_valid.max():.2f} µg/m³). '
            f'Bulan {month_labels[lowest_month - 1]} '
            f'memiliki rata-rata terendah '
            f'({monthly_valid.min():.2f} µg/m³).'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Bulan yang sama dari tahun berbeda digabungkan. "
            "Ini bukan tren kronologis tahunan."
        )

    else:
        st.info("Tidak terdapat data bulanan yang valid.")

# =====================================================
# 13. TAB 3 - ADVANCED BINNING ANALYSIS
# =====================================================

with tab3:
    st.subheader("PM2.5 Distribution Explorer")

    st.markdown(
        '<div class="section-caption">'
        'Analisis lanjutan menggunakan teknik binning.'
        '</div>',
        unsafe_allow_html=True
    )

    bins = [0, 25, 50, 100, 150, np.inf]

    labels = [
        "Sangat Rendah",
        "Rendah",
        "Sedang",
        "Tinggi",
        "Sangat Tinggi"
    ]

    valid_values = filtered_df["PM2.5"].dropna()

    categories = pd.cut(
        valid_values,
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    distribution = (
        categories.value_counts()
        .reindex(labels, fill_value=0)
    )

    if distribution.sum() > 0:
        percentage = (
            distribution / distribution.sum() * 100
        )

        fig, ax = plt.subplots(
            figsize=(10, 5.5),
            facecolor=BG
        )

        chart_colors = [
            "#4C86BB",
            "#51B8CE",
            "#62E4C7",
            "#F2B56B",
            "#F28B67"
        ]

        bars = ax.bar(
            labels,
            percentage.values,
            color=chart_colors,
            width=0.65
        )

        for bar in bars:
            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.4,
                f"{height:.1f}%",
                ha="center",
                color=TEXT,
                fontsize=10
            )

        ax.set_ylabel("Percentage of valid readings (%)")
        ax.set_ylim(
            0,
            max(percentage.max() * 1.2, 1)
        )

        ax.tick_params(axis="x", labelrotation=12)

        style_chart(ax)

        ax.grid(
            axis="y",
            linestyle="--",
            alpha=0.16,
            color="white"
        )

        fig.tight_layout()

        st.pyplot(fig)
        plt.close(fig)

        high_share = (
            (valid_values > 100).mean() * 100
        )

        st.markdown(
            '<div class="insight-card">'
            '<b>Pollution Distribution Insight</b><br>'
            f'<b>{high_share:.2f}%</b> dari pengukuran '
            'PM2.5 valid pada data terpilih berada '
            'di atas 100 µg/m³.'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Batas kategori merupakan interval analitis "
            "untuk eksplorasi, bukan klasifikasi resmi ISPU "
            "atau indeks kualitas udara lainnya."
        )

    else:
        st.info("Tidak terdapat pengukuran PM2.5 valid.")

# =====================================================
# 14. DATA QUALITY AND METHODOLOGY
# =====================================================

st.divider()

with st.expander("🔎 Data Quality & Methodology"):
    st.markdown("""
    **Dataset:** Beijing Air Quality, Maret 2013 –
    Februari 2017, dengan 12 stasiun pemantauan.

    **Metode pengolahan:**
    - Menggabungkan 12 file CSV.
    - Mengidentifikasi missing value, duplikasi,
      nilai tidak valid, dan potensi outlier.
    - Melakukan interpolasi linear PM2.5 secara
      terpisah per stasiun untuk rentetan kosong
      maksimal 3 jam yang diapit pengukuran valid.
    - Mempertahankan missing value panjang dan
      nilai ekstrem yang belum terbukti salah.
    - Menghitung rata-rata dengan mengabaikan
      nilai PM2.5 yang masih kosong.

    **Keterbatasan:**
    - Sebagian nilai PM2.5 merupakan hasil estimasi.
    - Hasil analisis bersifat deskriptif.
    - Dashboard tidak menampilkan kondisi udara
      secara real-time.
    """)

# =====================================================
# 15. RECOMMENDATIONS
# =====================================================

st.subheader("Insights to Action")

st.markdown("""
<div class="insight-card">
<b>Recommendations based on the full historical analysis</b><br>
Prioritaskan evaluasi kualitas udara di Dongsi, karena
stasiun ini memiliki rata-rata PM2.5 tertinggi dalam
analisis keseluruhan. Perhatikan pula periode Desember
yang menunjukkan rata-rata konsentrasi tertinggi
berdasarkan bulan kalender.
<br><br>
Lakukan pemantauan data secara berkelanjutan dan
analisis faktor meteorologi maupun sumber emisi
sebelum menentukan penyebab pencemaran.
</div>
""".replace("\n", " "), unsafe_allow_html=True)

st.caption(
    "Rekomendasi ini berasal dari analisis historis seluruh "
    "dataset, bukan otomatis berubah mengikuti filter."
)

# =====================================================
# 16. FOOTER
# =====================================================

st.markdown(
    '<div class="footer">'
    'AirScope · Beijing Air Quality Intelligence<br>'
    'Data Analysis Project — Dicoding Indonesia<br>'
    'Historical environmental analytics · 2013–2017'
    '</div>',
    unsafe_allow_html=True
)
