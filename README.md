# iDEA — IDX Economic & Earnings Analytics

Dashboard Streamlit siap di-upload ke GitHub dan dideploy ke Streamlit Community Cloud.

## Jalankan lokal
```bash
pip install -r requirements.txt
streamlit run app.py
```

## GitHub
Upload `app.py` dan `requirements.txt` ke repository. Lalu pilih repository tersebut di Streamlit Community Cloud dan gunakan `app.py` sebagai Main file.

## Google Sheets
Aplikasi membaca Google Sheet melalui endpoint CSV.
- Sheet indikator: GID `785055536`
- Sheet kategori: GID `229150555`

Jika GID atau spreadsheet berubah, ubah konstanta di bagian atas `app.py`.

## Halaman
- Home — monitoring indikator dan Top 5
- Analisis — ringkasan kinerja, IKE/PMI/IKBM, kontribusi, tabel pertumbuhan, Top/Bottom 5
- Analisis Emiten — template detail emiten
- Metadata — definisi indikator dan sumber data
