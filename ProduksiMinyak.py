#Salsabila Tiara Putri
#12220113

from os import name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit as st
from PIL import Image
import json

#########Title#########
st.set_page_config(layout="wide") #this needs to be the first streamlit command called
st.title("Statistik Produksi Minyak Mentah Suatu Negara")
st.markdown("*Sumber data berisi kode negara dan produksi minyak mentah suatu negara untuk setiap tahunnya.*")
#########Title#########

#########Sidebar#########
image = Image.open('oilrig.png')
st.sidebar.image(image)
st.sidebar.title("Pengaturan")

## User inputs on the control panel
st.sidebar.subheader("Pengaturan konfigurasi tampilan")
file = "produksi_minyak_mentah.csv"
df = pd.read_csv(file)

kode = pd.read_json('kode_negara_lengkap.json')
data = pd.DataFrame(kode, columns= ['name','alpha-3'])
kode_dict = dict(data.values.tolist())
list_kode = list(df['kode_negara'].unique())

list_negara=[]
kode_dict2 = {value:key for key, value in kode_dict.items()}
list_negara = list(map(kode_dict2.get, list_kode))

list_tahun = list(range(1971,2016))

negara = st.sidebar.selectbox("Pilih negara:", list_negara)
tahun = st.sidebar.selectbox("Pilih tahun:", list_tahun)
B_besar = st.sidebar.slider("Banyak negara:", min_value=1, max_value=137, value=10)
############### sidebar ###############

############### upper left column (1) ###############
col1, col2 = st.columns(2)
col1.subheader(f"Tabel representasi data produksi minyak mentah negara {negara}")

if negara in kode_dict.keys():
    group = dict(tuple(df.groupby('kode_negara')))
    df_negara = (group[kode_dict[negara]])
else: print('error')
col1.dataframe(df_negara.head(len(list_tahun)))
with open('produksi_minyak_mentah.csv', 'rb') as my_file:
    col2.download_button(label = 'Download data', data = my_file, file_name = 'ProduksiMinyakMentah.csv', mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
############### upper left column (1)###############

############### upper right column (2)###############
col2.subheader("Grafik produksi minyak mentah negara terhadap tahun")

cmap_name = 'tab20b'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(df_negara['tahun'])]
produksinegara = df_negara['produksi'].tolist()
x = np.arange(len(list_tahun))
fig, ax = plt.subplots()
ax.bar(x, produksinegara, color=colors, label='produksi negara')
ax.set_ylabel("Produk Minyak Mentah", fontsize=12)
ax.set_title(negara)
ax.set_xticks(x)
ax.set_xticklabels(list_tahun, rotation=90, fontsize = 8)
col2.pyplot(fig)
############### upper right column (2)###############

############### lower left column (3) ###############
col3, col4 = st.columns(2)
col3.subheader("Grafik produksi minyak mentah kumulatif terbesar")

total_produksi = []
for i in list_negara:
    if i not in kode_dict.keys():
        continue
    group = dict(tuple(df.groupby('kode_negara')))
    df_negara = (group[kode_dict[i]])
    jumlah_produksi = df_negara['produksi'].astype(int).sum()
    total_produksi.append(jumlah_produksi)

cmap_name = 'tab20b'
cmap = cm.get_cmap(cmap_name)
colors = cmap.colors[:len(list_negara)]
fig, ax = plt.subplots()
dataproduksi = pd.DataFrame({'negara': list_negara,'produksi':total_produksi})
terbesarproduksi = dataproduksi.nlargest(B_besar,'produksi')
ax.barh(terbesarproduksi['negara'],terbesarproduksi['produksi'] , color=colors)
ax.set_yticklabels(terbesarproduksi['negara'], rotation=0, fontsize=8)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel("Jumlah Produksi Kumulatif ", fontsize=12)
ax.set_ylabel("Negara", fontsize=12)
for labels in ax.containers:
    ax.bar_label(labels, fontsize=6)
plt.tight_layout()

col3.pyplot(fig)
############### lower left column (3) ###############

############### lower right column (4) ###############
col4.subheader(f"Grafik jumlah produksi minyak mentah terbesar pada {tahun}")

produksi_tahun =[]
for i in list_negara:
    if i not in kode_dict.keys():
        continue
    group = dict(tuple(df.groupby('kode_negara')))
    df_negara = (group[kode_dict[i]])
    prodtahun = df_negara.loc[df['tahun'] == tahun]
    produksiterbesar  = prodtahun['produksi'].sum()
    produksi_tahun.append(produksiterbesar)
dataproduksi2 = pd.DataFrame({'negara': list_negara,'produksi':produksi_tahun})
produksitahun = dataproduksi2.nlargest(B_besar,'produksi')
fig, ax = plt.subplots()
ax.barh(produksitahun['negara'],produksitahun['produksi'] , color=colors)
ax.set_yticklabels(produksitahun['negara'], rotation=0)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_title(tahun, fontsize=14)
ax.set_xlabel("Jumlah Produksi Tahunan", fontsize=12)
ax.set_ylabel("Negara", fontsize=12)
ax.set_title(tahun)
for labels in ax.containers:
    ax.bar_label(labels, fontsize=6)
plt.tight_layout()

col4.pyplot(fig)
############### lower right column (4) ###############

############### loowerer left column (5) ###############
col5, col6 = st.columns(2)
col5.subheader(f"Summary produksi minyak mentah terbesar pada {tahun}")

newdata = pd.DataFrame(kode, columns= ['name','alpha-3','region','sub-region'])
newdata2 = newdata[newdata['alpha-3'].isin(list_kode)]

prodtahun = df.loc[df['tahun'] == tahun]
max_value = prodtahun['produksi'].max()
prodtahun2 = prodtahun.loc[prodtahun['produksi'] == max_value]
prodtahun2 = prodtahun2.iloc[0]['kode_negara']
datanegaramax = newdata2.loc[newdata2['alpha-3'] == str(prodtahun2)]
negaramax = datanegaramax.iloc[0]['name']
kodenegaramax = datanegaramax.iloc[0]['alpha-3']
regionmax = datanegaramax.iloc[0]['region']
subregionmax = datanegaramax.iloc[0]['sub-region']
if negaramax in kode_dict.keys():
    group = dict(tuple(df.groupby('kode_negara')))
    df_negara = (group[kode_dict[negaramax]])
    kumulatifmax = df_negara['produksi'].astype(int).sum()
col5.markdown(f"Negara: {negaramax}")
col5.markdown(f"Kode Negara: {kodenegaramax}")
col5.markdown(f"Region: {regionmax}")
col5.markdown(f"Sub-region: {subregionmax}")
col5.markdown(f"Produksi tahun {tahun}: {max_value}")
col5.markdown(f"Produksi Kumulatif Negara: {kumulatifmax}")
############### loowerer left column (5)###############

############### loowerer right column (6)###############
col6.subheader(f"Summary produksi minyak mentah terkecil pada {tahun}")
prodtahun = df.loc[df['tahun'] == tahun]
min_value = prodtahun[prodtahun['produksi']> .0001]['produksi'].min()
prodtahun3 = prodtahun.loc[prodtahun['produksi'] == min_value]
prodtahun3 = prodtahun3.iloc[0]['kode_negara']
datanegaramin = newdata2.loc[newdata2['alpha-3'] == str(prodtahun3)]
negaramin = datanegaramin.iloc[0]['name']
kodenegaramin = datanegaramin.iloc[0]['alpha-3']
regionmin = datanegaramin.iloc[0]['region']
subregionmin = datanegaramin.iloc[0]['sub-region']
if negaramin in kode_dict.keys():
    group = dict(tuple(df.groupby('kode_negara')))
    df_negara = (group[kode_dict[negaramin]])
    kumulatifmin = df_negara['produksi'].astype(int).sum()
col6.markdown(f"Negara: {negaramin}")
col6.markdown(f"Kode Negara: {kodenegaramin}")
col6.markdown(f"Region: {regionmin}")
col6.markdown(f"Sub-region: {subregionmin}")
col6.markdown(f"Produksi tahun {tahun}: {min_value}")
col6.markdown(f"Produksi Kumulatif Negara: {kumulatifmin}")
############### loowerer right column (6) ###############

############### more loowerer left column (7) ###############
col7, col8 = st.columns(2)
col7.subheader(f"Summary produksi minyak mentah sama dengan 0 pada {tahun}")

prodtahun = df.loc[df['tahun'] == tahun]
prodtahun4 = prodtahun.loc[prodtahun['produksi'] == 0]
kodenegara0 = prodtahun4['kode_negara'].tolist()
datanegara0 = newdata[newdata['alpha-3'].isin(kodenegara0)]
namanegara0 = datanegara0['name'].tolist()
kumulatifnegara0=[]
for i in namanegara0:
    if i not in kode_dict.keys():
        continue
    group = dict(tuple(df.groupby('kode_negara')))
    df_negara = (group[kode_dict[i]])
    negara0 = df_negara['produksi'].astype(int).sum()
    kumulatifnegara0.append(negara0)
datanegara0['kumulatif produksi'] = kumulatifnegara0
datanegara0.rename(columns={'name':'negara','alpha-3':'kode Negara'}, inplace=True)

col7.dataframe(datanegara0.head(len(kumulatifnegara0)))
############### more loowerer left column (7)###############

############### more loowerer right column (8)###############
col8.subheader(f"Grafik produksi minyak mentah kumulatif negara yang pada {tahun} sama dengan 0")
kumulatif0 = datanegara0[datanegara0['kumulatif produksi']>.001]['kumulatif produksi'].tolist()
kumulatifga0 = datanegara0[datanegara0['kumulatif produksi'].isin(kumulatif0)]
negarayg0 = kumulatifga0['negara'].tolist()
kumulatifprodga0 = kumulatifga0['kumulatif produksi'].tolist()
colors = cmap.colors[:len(kumulatifprodga0)]
fig, ax = plt.subplots()
def label_function(val):
    return f'{val / 100 * sum(kumulatifprodga0):.0f}'
patches, labels, texts = ax.pie(kumulatifprodga0, autopct=label_function, startangle=45, colors = colors, textprops={'fontsize': 8})
centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
ax.axis('equal')  
ax.legend(patches, negarayg0 , loc="center left", bbox_to_anchor=(1, 0.5))
plt.tight_layout()
col8.pyplot(fig)
############### more loowerer right column (8) ###############
