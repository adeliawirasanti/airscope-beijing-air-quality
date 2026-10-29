# Proyek Analisis Data: Beijing Air Quality

## Deskripsi Proyek

Proyek ini dibuat untuk memenuhi submission akhir kelas **Belajar Fundamental Analisis Data** di Dicoding Indonesia.

Pada proyek ini, dilakukan analisis data kualitas udara di Beijing menggunakan *Beijing Multi-Site Air Quality Dataset*. Dataset berisi data pemantauan kualitas udara dari 12 stasiun selama periode 1 Maret 2013 sampai 28 Februari 2017.

Analisis berfokus pada konsentrasi PM2.5 untuk mengetahui perbedaan rata-rata konsentrasi antarstasiun serta pola konsentrasi berdasarkan bulan.

Hasil analisis ditampilkan dalam dashboard interaktif bernama **AirScope** yang dikembangkan menggunakan Streamlit.

## Pertanyaan Bisnis

Proyek ini bertujuan menjawab dua pertanyaan bisnis berikut.

1. Bagaimana perbandingan rata-rata konsentrasi PM2.5 pada 12 stasiun pemantauan kualitas udara di Beijing selama 1 Maret 2013 hingga 28 Februari 2017, dan stasiun mana yang memiliki rata-rata tertinggi?
2. Bagaimana pola rata-rata konsentrasi PM2.5 berdasarkan bulan kalender pada 12 stasiun pemantauan selama periode tersebut, dan bulan apa yang memiliki rata-rata tertinggi?

## Dataset yang Digunakan

Dataset yang digunakan adalah *Beijing Multi-Site Air Quality Dataset*.

Sumber dataset: [UCI Machine Learning Repository – Beijing Multi-Site Air Quality Data](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data)

Dataset terdiri dari 12 file CSV yang masing-masing berisi pengukuran kualitas udara pada satu stasiun.

Setelah seluruh file digabungkan, dataset memiliki 420.768 baris dan 18 kolom.

Beberapa kolom utama yang digunakan dalam analisis adalah:

- `station`: nama stasiun pemantauan.
- `year`: tahun pengukuran.
- `month`: bulan pengukuran.
- `day`: tanggal pengukuran.
- `hour`: jam pengukuran.
- `PM2.5`: konsentrasi PM2.5 dalam µg/m³.

## Tahapan Analisis Data

### 1. Menentukan Pertanyaan Bisnis

Menentukan dua pertanyaan analisis yang berkaitan dengan perbandingan konsentrasi PM2.5 berdasarkan stasiun dan pola konsentrasi berdasarkan bulan pengamatan.

### 2. Data Wrangling

Menggabungkan 12 file CSV menjadi satu DataFrame, kemudian memeriksa missing value, data duplikat, nilai tidak valid, dan potensi outlier.

Missing value pada PM2.5 ditangani menggunakan interpolasi linear terbatas maksimal 3 jam secara terpisah untuk setiap stasiun.

Setelah proses cleaning, masih terdapat 5.285 missing value PM2.5 yang dipertahankan karena tidak memenuhi kriteria interpolasi.

### 3. Exploratory Data Analysis (EDA)

Menghitung rata-rata konsentrasi PM2.5 berdasarkan stasiun dan bulan menggunakan fungsi `groupby()` dan agregasi pada pandas.

### 4. Data Visualization

Membuat visualisasi untuk membandingkan rata-rata konsentrasi PM2.5 antarstasiun dan melihat pola rata-rata berdasarkan bulan kalender.

### 5. Analisis Lanjutan

Menggunakan teknik binning dengan `pd.cut()` untuk mengelompokkan nilai PM2.5 ke dalam beberapa interval konsentrasi guna membantu memahami distribusi data.

### 6. Conclusion & Recommendation

Menyusun kesimpulan dan rekomendasi berdasarkan hasil analisis yang telah dilakukan.

## Hasil Analisis

Berdasarkan hasil analisis selama periode pengamatan:

- Stasiun Dongsi memiliki rata-rata konsentrasi PM2.5 tertinggi, yaitu 86,07 µg/m³.
- Stasiun Dingling memiliki rata-rata konsentrasi PM2.5 terendah, yaitu 66,00 µg/m³.
- Bulan Desember memiliki rata-rata konsentrasi PM2.5 tertinggi, yaitu 104,29 µg/m³.
- Bulan Agustus memiliki rata-rata konsentrasi PM2.5 terendah, yaitu 53,40 µg/m³.

Hasil tersebut menunjukkan adanya perbedaan rata-rata konsentrasi PM2.5 berdasarkan lokasi dan bulan pengamatan.

Hasil analisis bersifat deskriptif sehingga belum dapat digunakan untuk memastikan faktor penyebab perbedaan konsentrasi PM2.5.

## Dashboard AirScope

Dashboard AirScope dikembangkan menggunakan Streamlit untuk menampilkan hasil analisis secara interaktif.

Fitur dashboard meliputi:

- Ringkasan jumlah stasiun, jumlah data, dan rata-rata PM2.5.
- Filter berdasarkan stasiun pemantauan.
- Filter tanggal mulai dan tanggal akhir.
- Grafik rata-rata PM2.5 berdasarkan stasiun.
- Grafik pola rata-rata PM2.5 berdasarkan bulan.
- Grafik distribusi kategori konsentrasi PM2.5.
- Ringkasan insight dan rekomendasi hasil analisis.

Dashboard menggunakan data hasil cleaning yang disimpan dalam file `main_data.csv`.

## Struktur Folder Proyek

Struktur direktori proyek yang digunakan adalah sebagai berikut.

```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── PRSA_Data_Aotizhongxin_20130301-20170228.csv
│   ├── PRSA_Data_Changping_20130301-20170228.csv
│   ├── PRSA_Data_Dingling_20130301-20170228.csv
│   ├── PRSA_Data_Dongsi_20130301-20170228.csv
│   ├── PRSA_Data_Guanyuan_20130301-20170228.csv
│   ├── PRSA_Data_Gucheng_20130301-20170228.csv
│   ├── PRSA_Data_Huairou_20130301-20170228.csv
│   ├── PRSA_Data_Nongzhanguan_20130301-20170228.csv
│   ├── PRSA_Data_Shunyi_20130301-20170228.csv
│   ├── PRSA_Data_Tiantan_20130301-20170228.csv
│   ├── PRSA_Data_Wanliu_20130301-20170228.csv
│   └── PRSA_Data_Wanshouxigong_20130301-20170228.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Cara Menjalankan Dashboard

Bagian ini menjelaskan langkah-langkah menyiapkan environment, menginstal library, dan menjalankan dashboard AirScope pada komputer lokal.

### 1. Persiapan

Pastikan Python sudah terinstal pada komputer. Disarankan menggunakan Python 3.11 agar sesuai dengan environment pengembangan proyek.

Untuk memeriksa instalasi Python dan pip, buka terminal lalu jalankan:

```bash
python --version
python -m pip --version
```

Jika perintah `python` tidak dikenali pada Windows, coba gunakan perintah `py`.

Unduh atau salin folder proyek ke komputer, kemudian buka folder utama `submission` menggunakan VS Code atau terminal.

### 2. Setup Environment

Gunakan virtual environment agar dependensi proyek terpisah dari proyek Python lainnya dan risiko konflik library dapat dikurangi.

**Windows (PowerShell)**

Pastikan terminal berada di folder utama `submission`, yaitu folder yang berisi `requirements.txt`.

Buat virtual environment:

```powershell
python -m venv .venv
```

Aktifkan virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Jika berhasil, nama environment biasanya muncul sebagai `(.venv)` di awal baris terminal.

Jika PowerShell menolak menjalankan skrip aktivasi karena kebijakan eksekusi, gunakan Command Prompt dan jalankan:

```bat
.venv\Scripts\activate.bat
```

**Alternatif: Anaconda atau Miniconda**

Jika menggunakan Anaconda atau Miniconda, buat environment terpisah dengan perintah:

```bash
conda create --name airscope-env python=3.11
conda activate airscope-env
```

Gunakan salah satu metode setup environment saja.

### 3. Instalasi Library

Pastikan environment sudah aktif dan terminal berada di folder utama `submission`.

Jalankan perintah berikut:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Perintah tersebut menginstal library yang tercantum dalam `requirements.txt`, termasuk Streamlit, pandas, NumPy, Matplotlib, dan Seaborn beserta versi yang ditentukan.

### 4. Menjalankan Dashboard

Setelah instalasi selesai, jalankan perintah berikut dari folder utama `submission`:

```bash
python -m streamlit run dashboard/dashboard.py
```

Jika dashboard berhasil dijalankan, terminal akan menampilkan alamat lokal, misalnya:

```text
Local URL: http://localhost:8501
```

Buka alamat tersebut melalui browser untuk mengakses dashboard AirScope.

Pastikan file `main_data.csv` berada di dalam folder `dashboard` bersama file `dashboard.py`.

### 5. Menghentikan Dashboard

Untuk menghentikan aplikasi yang sedang berjalan, tekan `Ctrl + C` pada terminal.

Jika menggunakan virtual environment `venv`, keluar dari environment dengan perintah:

```bash
deactivate
```

Jika menggunakan Conda, keluar dari environment dengan perintah:

```bash
conda deactivate
```

## Dashboard Online

Dashboard AirScope tersedia secara online melalui Streamlit Community Cloud.

Tautan dashboard:

[https://airscope-beijing-air-quality.streamlit.app/](https://airscope-beijing-air-quality.streamlit.app/)

Dashboard menampilkan analisis berdasarkan data historis kualitas udara Beijing dari Maret 2013 hingga Februari 2017, sehingga tidak merepresentasikan kondisi kualitas udara secara real-time.

## Library yang Digunakan

Library Python yang digunakan dalam proyek ini meliputi:

- pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

Versi library yang digunakan dicantumkan dalam file `requirements.txt`.

## Catatan

Dataset yang digunakan merupakan data historis tahun 2013 hingga 2017, sehingga hasil analisis tidak menunjukkan kondisi kualitas udara Beijing secara real-time.

Sebagian missing value PM2.5 telah diisi menggunakan interpolasi terbatas. Nilai yang masih kosong tidak disertakan dalam perhitungan rata-rata.

Hasil analisis bersifat deskriptif. Kategori PM2.5 pada teknik binning merupakan kategori analitis yang dibuat untuk kebutuhan eksplorasi data, bukan standar resmi indeks kualitas udara.
