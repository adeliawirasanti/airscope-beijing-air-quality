
# Proyek Analisis Data: Beijing Air Quality

## Deskripsi Proyek

Proyek ini dibuat untuk memenuhi submission akhir kelas
Belajar Fundamental Analisis Data di Dicoding Indonesia.

Pada proyek ini, saya melakukan analisis data kualitas udara
di Beijing menggunakan Beijing Multi-Site Air Quality Dataset.
Dataset ini berisi data pemantauan kualitas udara dari 12
stasiun selama periode 1 Maret 2013 sampai 28 Februari 2017.

Analisis berfokus pada konsentrasi PM2.5 untuk mengetahui
perbedaan rata-rata konsentrasi antarstasiun serta pola
konsentrasi berdasarkan bulan.

Hasil analisis kemudian ditampilkan dalam dashboard
interaktif bernama AirScope yang dibuat menggunakan Streamlit.

## Pertanyaan Bisnis

Terdapat dua pertanyaan yang ingin dijawab melalui
proyek analisis ini.

1. Bagaimana perbandingan rata-rata konsentrasi PM2.5
   pada 12 stasiun pemantauan kualitas udara di Beijing
   selama 1 Maret 2013 hingga 28 Februari 2017,
   dan stasiun mana yang memiliki rata-rata tertinggi?

2. Bagaimana pola rata-rata konsentrasi PM2.5 berdasarkan
   bulan kalender pada 12 stasiun pemantauan di Beijing
   selama periode tersebut, dan bulan apa yang memiliki
   rata-rata tertinggi?

## Dataset yang Digunakan

Dataset yang digunakan adalah Beijing Multi-Site Air
Quality Dataset.

Sumber dataset:
https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data

Dataset terdiri dari 12 file CSV yang masing-masing
berisi pengukuran kualitas udara pada satu stasiun.

Setelah seluruh file digabungkan, dataset memiliki
420.768 baris dan 18 kolom.

Beberapa kolom utama yang digunakan dalam analisis adalah:

- `station`: nama stasiun pemantauan
- `year`: tahun pengukuran
- `month`: bulan pengukuran
- `day`: tanggal pengukuran
- `hour`: jam pengukuran
- `PM2.5`: konsentrasi PM2.5 dalam µg/m³

## Tahapan Analisis Data

Proses analisis dilakukan melalui beberapa tahapan.

1. **Menentukan Pertanyaan Bisnis**

   Menentukan dua pertanyaan analisis yang berkaitan
   dengan konsentrasi PM2.5 berdasarkan stasiun
   dan bulan pengamatan.

2. **Data Wrangling**

   Menggabungkan 12 file CSV menjadi satu DataFrame,
   kemudian memeriksa missing value, data duplikat,
   nilai tidak valid, dan potensi outlier.

   Missing value pada PM2.5 ditangani menggunakan
   interpolasi linear terbatas maksimal 3 jam secara
   terpisah untuk setiap stasiun.

   Setelah proses cleaning, masih terdapat 5.285
   missing value PM2.5 yang dipertahankan karena
   tidak memenuhi kriteria interpolasi.

3. **Exploratory Data Analysis (EDA)**

   Menghitung rata-rata konsentrasi PM2.5 berdasarkan
   stasiun dan bulan menggunakan fungsi groupby()
   dan agregasi pada pandas.

4. **Data Visualization**

   Membuat grafik untuk membandingkan rata-rata
   konsentrasi PM2.5 antarstasiun serta melihat
   pola rata-rata berdasarkan bulan kalender.

5. **Analisis Lanjutan**

   Menggunakan teknik binning dengan pd.cut()
   untuk mengelompokkan nilai PM2.5 ke dalam
   beberapa interval konsentrasi.

6. **Conclusion & Recommendation**

   Menyusun kesimpulan dan rekomendasi berdasarkan
   hasil analisis yang telah dilakukan.

## Hasil Analisis

Berdasarkan hasil analisis selama periode pengamatan:

- Stasiun Dongsi memiliki rata-rata konsentrasi PM2.5
  tertinggi, yaitu 86,07 µg/m³.
- Stasiun Dingling memiliki rata-rata konsentrasi PM2.5
  terendah, yaitu 66,00 µg/m³.
- Bulan Desember memiliki rata-rata konsentrasi PM2.5
  tertinggi, yaitu 104,29 µg/m³.
- Bulan Agustus memiliki rata-rata konsentrasi PM2.5
  terendah, yaitu 53,40 µg/m³.

Dari hasil tersebut, dapat diketahui bahwa konsentrasi
PM2.5 memiliki perbedaan berdasarkan lokasi dan bulan
pengamatan.

Namun, hasil ini masih bersifat deskriptif sehingga
belum dapat digunakan untuk memastikan faktor penyebab
perbedaan konsentrasi PM2.5.

## Dashboard AirScope

Dashboard AirScope dibuat menggunakan Streamlit untuk
menampilkan hasil analisis secara interaktif.

Fitur yang tersedia pada dashboard antara lain:

- Ringkasan jumlah stasiun, jumlah data, dan rata-rata PM2.5.
- Filter berdasarkan stasiun pemantauan.
- Filter tanggal mulai dan tanggal akhir.
- Grafik rata-rata PM2.5 berdasarkan stasiun.
- Grafik pola rata-rata PM2.5 berdasarkan bulan.
- Grafik distribusi kategori konsentrasi PM2.5.
- Ringkasan insight dan rekomendasi hasil analisis.

Dashboard menggunakan data hasil cleaning yang disimpan
dalam file main_data.csv.

## Struktur Folder

    submission/
    ├── dashboard/
    │   ├── dashboard.py
    │   └── main_data.csv
    ├── data/
    │   └── 12 file CSV Air Quality
    ├── notebook.ipynb
    ├── README.md
    └── requirements.txt

## Cara Menjalankan Dashboard

Berikut langkah-langkah untuk menjalankan dashboard
AirScope di komputer.

### 1. Persiapan

Pastikan Python dan pip sudah terinstal.

Buka folder `submission` menggunakan VS Code
atau terminal.

### 2. Instal Library

Jalankan perintah berikut pada terminal:

    python -m pip install -r requirements.txt

Perintah tersebut digunakan untuk menginstal library
yang diperlukan dalam proyek.

### 3. Menjalankan Dashboard

Setelah proses instalasi selesai, jalankan:

    python -m streamlit run dashboard/dashboard.py

### 4. Membuka Dashboard

Setelah Streamlit berhasil dijalankan, buka alamat:

http://localhost:8501

Dashboard AirScope akan tampil melalui browser.

Pastikan file `main_data.csv` berada di dalam
folder `dashboard` bersama file `dashboard.py`.

## Library yang Digunakan

Beberapa library Python yang digunakan adalah:

- pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

## Catatan

Dataset yang digunakan merupakan data historis
tahun 2013 sampai 2017, sehingga hasil analisis
tidak menunjukkan kondisi kualitas udara Beijing
secara real-time.

Sebagian missing value PM2.5 telah diisi menggunakan
interpolasi terbatas. Nilai yang masih kosong tidak
disertakan dalam perhitungan rata-rata.

Kategori konsentrasi PM2.5 pada analisis binning
merupakan kategori yang dibuat untuk kebutuhan
analisis, bukan kategori resmi indeks kualitas udara.
