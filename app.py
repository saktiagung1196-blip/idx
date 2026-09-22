import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='iDEA — IDX Economic & Earnings Analytics', page_icon='📊', layout='wide')
SHEET_ID='1z2-UYSAGLHWb88LADmDKH4Y4pPFkM3aCJH5wPuw0Mp8'
GID_IND='785055536'
GID_CAT='229150555'

st.markdown('''<style>
.stApp{background:#f4f7fb}.block-container{max-width:1500px;padding:1.2rem 2rem 3rem}.idea{font-size:34px;font-weight:900;color:#073b78}.sub{font-size:11px;color:#7186a0}.title{font-size:30px;font-weight:850;color:#073b78}.section{font-size:23px;font-weight:800;color:#073b78;margin:22px 0 12px}.card{background:#fff;border:1px solid #dbe5f0;border-radius:14px;padding:17px 20px;box-shadow:0 5px 18px rgba(28,65,110,.06)}.label{font-size:11px;font-weight:700;color:#75869d;text-transform:uppercase}.value{font-size:28px;font-weight:850;color:#073b78;margin-top:5px}.note{font-size:11px;color:#91a0b2}.up{color:#169b62;font-weight:800}.down{color:#ef4050;font-weight:800}
</style>''', unsafe_allow_html=True)

@st.cache_data(ttl=300)
def csv(gid):
    try:return pd.read_csv(f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}')
    except Exception:return pd.DataFrame()

def number(x):
    return pd.to_numeric(x.astype(str).str.replace('%','',regex=False).str.replace('.','',regex=False).str.replace(',','.',regex=False),errors='coerce')

def indicators():
    d=csv(GID_IND)
    if d.empty:return demo_ind()
    d.columns=[str(x).strip() for x in d.columns]
    for c in ['IKE BEI','PMI','IKBM','QtQ','YoY','CtoC']:
        if c in d:d[c]=number(d[c])
    return d.drop_duplicates('Periode') if 'Periode' in d else demo_ind()

def categories():
    d=csv(GID_CAT)
    if d.empty:return demo_cat()
    d.columns=[str(x).strip() for x in d.columns]
    for c in d.columns:
        if c.lower().replace(' ','')=='qtoq':d=d.rename(columns={c:'QtQ'})
        if 'jumlahperusaha' in c.lower().replace(' ',''):d=d.rename(columns={c:'Jumlah Perusahaan'})
    for c in ['Kontribusi','YoY','QtQ','CtoC','Jumlah Perusahaan']:
        if c in d:d[c]=number(d[c])
    return d if 'Kategori' in d else demo_cat()

def demo_ind():
    return pd.DataFrame({'Periode':['2025Q1','2025Q2','2025Q3','2025Q4','2026Q1','2026Q2'],'IKE BEI':[57.12,57.68,58.91,54.61,56.97,68.52],'PMI':[52.63,47,50.37,51.9,52.17,48.67],'IKBM':[np.nan,np.nan,50.48,52.21,51.37,52.31],'QtQ':[np.nan,np.nan,np.nan,6.13,-2.62,5.42],'YoY':[np.nan,np.nan,np.nan,7.75,10.84,11.54],'CtoC':[np.nan,np.nan,np.nan,5.96,10.84,10.64]})

def demo_cat():
    c=['Industri Pengolahan','Informasi dan Komunikasi','Pertambangan dan Penggalian','Perdagangan','Keuangan','Jasa Perusahaan','Konstruksi','Real Estat','Lainnya','Transportasi','Pengadaan Listrik Gas dan Air']
    return pd.DataFrame({'Periode':['2026Q2']*11,'Kategori':c,'Kontribusi':[41.48,15.62,12.11,11.38,6.57,6.40,1.98,1.73,1.27,.94,.53],'YoY':[17.16,24.22,-6.19,23.78,4.13,-5.08,3.06,13.43,6.95,5.30,6.27],'QtQ':[3.78,7.62,-15.34,.90,2.65,11.63,-34.62,-15.67,-2.90,-6.23,-7.28],'CtoC':[17.16,24.22,-6.19,23.78,3.79,-3.07,3.06,13.43,-1.59,5.30,6.27],'Jumlah Perusahaan':[305,46,73,59,52,17,27,77,8,33,8]})

ind=indicators(); cat=categories()
periods=sorted(ind['Periode'].dropna().astype(str).unique())
years=sorted({p[:4] for p in periods},reverse=True)

with st.sidebar:
    st.markdown('<div class="idea">iDEA↗</div><div class="sub">IDX Economic & Earnings Analytics</div>',unsafe_allow_html=True)
    st.markdown('---')
    page=st.radio('Menu',['🏠 Home','📊 Analisis','🏢 Analisis Emiten','ℹ️ Metadata'])
    st.markdown('---')
    st.markdown('### 📅 Filter Periode')
    year=st.selectbox('Tahun',years)
    q=st.selectbox('Triwulan',['Semua']+[p[-2:] for p in periods if p.startswith(year)])
    selected=year+q if q!='Semua' else None
    if st.button('🔄 Refresh Data',use_container_width=True):st.cache_data.clear();st.rerun()

def row():
    x=ind[ind['Periode'].astype(str)==selected] if selected else ind.iloc[[-1]]
    return x.iloc[0] if not x.empty else ind.iloc[-1]

def cats():
    if selected and 'Periode' in cat:
        x=cat[cat['Periode'].astype(str)==selected]
        if not x.empty:return x
    return cat[cat['Periode'].astype(str).str.startswith(year)] if 'Periode' in cat else cat

def kpi(label,value,note=''):
    st.markdown(f'<div class="card"><div class="label">{label}</div><div class="value">{value}</div><div class="note">{note}</div></div>',unsafe_allow_html=True)

if page=='🏠 Home':
    st.markdown('<div class="title">Dashboard IDX Analytics</div><div class="sub">Kinerja Perusahaan Tercatat Bursa Efek Indonesia</div>',unsafe_allow_html=True)
    r=row(); st.markdown('<div class="section">📈 Perkembangan Indikator</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    for col,name in zip([a,b,c],['IKE BEI','PMI','IKBM']):
        with col:kpi(name,'—' if pd.isna(r.get(name)) else f"{r[name]:.2f}",r['Periode'])
    st.markdown('<div class="section">📈 Pertumbuhan Pendapatan</div>',unsafe_allow_html=True)
    g=ind[ind['Periode'].isin(['2025Q4','2026Q1','2026Q2'])]
    cols=st.columns(3)
    for col,m,t in zip(cols,['QtQ','YoY','CtoC'],['Pertumbuhan Pendapatan (QtQ)','Pertumbuhan Pendapatan (YoY)','Pertumbuhan Pendapatan (CtoC)']):
        fig=go.Figure(go.Scatter(x=g['Periode'],y=g[m],mode='lines+markers+text',text=[f'{v:.2f}%' if pd.notna(v) else '' for v in g[m]],textposition='top center',line=dict(color='#1769c2',width=3)))
        fig.add_hline(y=0,line_dash='dot',line_color='#8995a5');fig.update_layout(title=t,height=290,margin=dict(l=10,r=10,t=45,b=15),yaxis_title='%')
        col.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    st.markdown('<div class="section">🏆 Ringkasan Kontributor</div>',unsafe_allow_html=True)
    x=cats().sort_values('Kontribusi',ascending=False).head(5); y=cats().sort_values('YoY',ascending=False).head(5)
    a,b=st.columns(2)
    with a:
        f=px.bar(x.sort_values('Kontribusi'),x='Kontribusi',y='Kategori',orientation='h',text='Kontribusi',title='Top 5 Kontributor Pendapatan');f.update_traces(marker_color='#1769c2',texttemplate='%{text:.2f}%',textposition='outside');f.update_layout(height=300,margin=dict(l=5,r=25,t=50,b=10));st.plotly_chart(f,use_container_width=True,config={'displayModeBar':False})
    with b:
        f=px.bar(y.sort_values('YoY'),x='YoY',y='Kategori',orientation='h',text='YoY',title='Top 5 Pertumbuhan YoY');f.update_traces(marker_color='#43b978',texttemplate='%{text:.2f}%',textposition='outside');f.update_layout(height=300,margin=dict(l=5,r=25,t=50,b=10));st.plotly_chart(f,use_container_width=True,config={'displayModeBar':False})

elif page=='📊 Analisis':
    st.markdown('<div class="title">📊 Analisis Indikator Ekonomi & Emiten</div><div class="sub">Analisis mendalam berdasarkan periode, indikator, kontribusi dan pertumbuhan kategori.</div>',unsafe_allow_html=True)
    r=row();st.markdown('<div class="section">📌 Ringkasan Kinerja</div>',unsafe_allow_html=True)
    vals=[('Total Pendapatan','1,383','Rp triliun'),('IKE BEI',f"{r['IKE BEI']:.2f}",'indeks'),('Jumlah Perusahaan','791','perusahaan'),('Pertumbuhan YoY',f"{r['YoY']:.2f}%",'year-on-year'),('Pertumbuhan QtQ',f"{r['QtQ']:.2f}%",'quarter-on-quarter'),('Pertumbuhan CtoC',f"{r['CtoC']:.2f}%",'cumulative')]
    for cc,(l,v,n) in zip(st.columns(6),vals):
        with cc:kpi(l,v,n)
    st.markdown('<div class="section">📈 Perkembangan IKE BEI, PMI dan IKBM</div>',unsafe_allow_html=True)
    f=go.Figure()
    for m,col in [('IKE BEI','#1769c2'),('PMI','#71b9ef'),('IKBM','#ef4050')]:f.add_trace(go.Scatter(x=ind['Periode'],y=ind[m],mode='lines+markers',name=m,connectgaps=False,line=dict(color=col,width=3)))
    f.update_layout(height=420,yaxis_title='Indeks',margin=dict(l=10,r=10,t=15,b=25));st.plotly_chart(f,use_container_width=True,config={'displayModeBar':False})
    st.markdown('<div class="section">📊 Kontribusi menurut Kategori & Pertumbuhan</div>',unsafe_allow_html=True)
    x=cats().sort_values('Kontribusi',ascending=False);a,b=st.columns([1,1.4])
    with a:
        f=px.treemap(x,path=['Kategori'],values='Kontribusi',color='Kontribusi',color_continuous_scale=['#dceeff','#1769c2']);f.update_traces(texttemplate='<b>%{label}</b><br>%{value:.2f}%');f.update_layout(height=450,margin=dict(l=5,r=5,t=5,b=5));st.plotly_chart(f,use_container_width=True,config={'displayModeBar':False})
    with b:
        z=x[['Kategori','Kontribusi','YoY','QtQ','CtoC']].copy()
        for m in ['Kontribusi','YoY','QtQ','CtoC']:z[m]=z[m].map(lambda v:'—' if pd.isna(v) else f'{v:.2f}%')
        st.dataframe(z,use_container_width=True,hide_index=True,height=450)
    st.markdown('<div class="section">🏆 Top 5 & Bottom 5 Pertumbuhan YoY</div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    for col,asc,title,color in [(a,False,'Top 5 Pertumbuhan YoY','#43b978'),(b,True,'Bottom 5 Pertumbuhan YoY','#ef4050')]:
        z=x.sort_values('YoY',ascending=asc).head(5);f=px.bar(z.sort_values('YoY'),x='YoY',y='Kategori',orientation='h',text='YoY',title=title);f.update_traces(marker_color=color,texttemplate='%{text:.2f}%',textposition='outside');f.update_layout(height=300,margin=dict(l=5,r=30,t=45,b=10));col.plotly_chart(f,use_container_width=True,config={'displayModeBar':False})

elif page=='🏢 Analisis Emiten':
    st.markdown('<div class="title">🏢 Analisis Emiten</div><div class="sub">Telusuri kinerja emiten, tren pendapatan, perbandingan sektor dan posisi emiten.</div>',unsafe_allow_html=True)
    search=st.text_input('🔎 Cari kode atau nama emiten',placeholder='Contoh: BBRI')
    code=(search.upper() if search else 'BBRI');name='PT Bank Rakyat Indonesia (Persero) Tbk' if code=='BBRI' else f'Emiten {code}'
    st.markdown(f'<div class="card"><div class="label">EMITEN</div><div class="value">{name}</div><div class="note">{code} · Template issuer-level siap dihubungkan ke data emiten.</div></div>',unsafe_allow_html=True)
    for cc,(l,v,n) in zip(st.columns(4),[('Pendapatan','Rp 208,31 T','YoY +10,24%'),('Laba Bersih','Rp 29,03 T','YoY +7,15%'),('Total Aset','Rp 1.965,01 T','YoY +6,82%'),('Jumlah Karyawan','69.711','YoY +2,31%')]):
        with cc:kpi(l,v,n)
    st.markdown('<div class="section">📈 Tren Pendapatan</div>',unsafe_allow_html=True)
    tr=pd.DataFrame({'Periode':['2025Q1','2025Q2','2025Q3','2025Q4','2026Q1','2026Q2'],'Pendapatan':[178.24,189.31,195.62,201.14,210.52,208.31]})
    f=px.bar(tr,x='Periode',y='Pendapatan',text='Pendapatan');f.update_traces(marker_color='#1769c2',texttemplate='%{text:.2f}',textposition='outside');f.update_layout(height=350,yaxis_title='Rp Triliun');st.plotly_chart(f,use_container_width=True,config={'displayModeBar':False})
    st.info('Data issuer-level pada halaman ini adalah contoh tampilan. Hubungkan ke sheet emiten ketika dataset per emiten tersedia.')

else:
    st.markdown('<div class="title">ℹ️ Metadata</div><div class="sub">Definisi indikator dan struktur sumber data iDEA.</div>',unsafe_allow_html=True)
    st.dataframe(pd.DataFrame([['Total Pendapatan','Total pendapatan perusahaan tercatat pada periode terpilih','Rp triliun'],['Jumlah Perusahaan','Jumlah perusahaan yang tercakup dalam periode','perusahaan'],['IKE BEI','Indikator kinerja sesuai dataset iDEA','indeks'],['PMI','Purchasing Managers’ Index pada dataset','indeks'],['IKBM','Indikator kinerja bursa/modal pada dataset','indeks'],['YoY','Pertumbuhan dibanding periode yang sama tahun sebelumnya','persen'],['QtQ','Pertumbuhan dibanding triwulan sebelumnya','persen'],['CtoC','Pertumbuhan kumulatif sesuai dataset','persen'],['Kontribusi','Porsi pendapatan kategori terhadap total','persen']],columns=['Indikator','Definisi','Satuan']),use_container_width=True,hide_index=True)
    st.info('Google Sheet dibaca melalui ekspor CSV. Jika spreadsheet/GID berubah, ubah SHEET_ID dan GID di bagian atas app.py.')
