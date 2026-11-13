"""ISL 533 | B2B Book Distribution Intelligence.

Run: streamlit run streamlit_app.py
Revenue is Quantity * NetPrice, assuming NetPrice represents per-unit net selling price.
No stock, logistics lead-time, procurement-cost or geographic coordinates are supplied.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="B2B | Intelligence Studio", page_icon="📚", layout="wide", initial_sidebar_state="expanded")
COLORS=["#3458D4","#00A6A0","#F0A13A","#8F63CE","#E56A7A","#4C8EC8","#50A779"]
INK="#17243E"
MUTED="#596B82"
BG="#F5F7FC"
GRID="#E7EBF2"
px.defaults.template="plotly_white"
px.defaults.color_discrete_sequence=COLORS
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root {color-scheme: light;}
html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {font-family:'Inter',system-ui,sans-serif;}
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {background:#F5F7FC!important; color:#17243E!important;}
[data-testid="stHeader"] {background:#F5F7FC!important;}
[data-testid="stSidebar"], [data-testid="stSidebar"] > div {background:#FFFFFF!important;}
[data-testid="stSidebar"] {border-right:1px solid #E4E9F2!important;}
[data-testid="stSidebar"] *, [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {color:#26364E!important;}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {color:#62728B!important;}
.block-container {padding-top:1.65rem!important; padding-bottom:3.25rem!important; max-width:1600px!important;}
h1,h2,h3 {font-family:'Inter',sans-serif!important; color:#17243E!important; letter-spacing:-.035em!important;}
h1 {font-size:2.15rem!important; font-weight:800!important; margin-bottom:.25rem!important;}
h2 {font-size:1.35rem!important; font-weight:750!important;}
h3 {font-size:1.12rem!important; font-weight:700!important;}
[data-testid="stMarkdownContainer"] p, [data-testid="stCaptionContainer"] p {color:#51627C;}
[data-testid="stMetric"] {background:#FFFFFF!important;border:1px solid #E4EAF3!important;border-radius:16px!important; padding:18px 19px!important;box-shadow:0 4px 17px rgba(25,45,90,.035);min-height:119px;}
[data-testid="stMetricLabel"] p, [data-testid="stMetricLabel"] {color:#52647F!important;font-weight:650!important;font-size:.85rem!important;}
[data-testid="stMetricValue"] {color:#17243E!important;font-size:clamp(1.35rem,1.9vw,2.05rem)!important;font-weight:800!important;letter-spacing:-.045em!important;}
[data-testid="stMetricDelta"] {color:#059669!important;}
[data-testid="stTabs"] {background:transparent!important;}
.stTabs [data-baseweb="tab-list"] {gap:.6rem!important;border-bottom:1px solid #DFE5EF!important; padding-bottom:4px!important;overflow-x:auto;}
.stTabs [data-baseweb="tab"] {color:#62718B!important;font-weight:700!important;font-size:.9rem!important;background:transparent!important;padding:.7rem .9rem!important;}
.stTabs [aria-selected="true"] {color:#3458D4!important;border-bottom:3px solid #3458D4!important;}
.stTabs [data-baseweb="tab-panel"] {padding-top:1.5rem!important;}
[data-testid="stPlotlyChart"] {background:#FFFFFF!important; border:1px solid #E5EAF2!important; border-radius:17px!important; padding:10px 13px!important; box-shadow:0 4px 17px rgba(25,45,90,.025);}
[data-testid="stDataFrame"] {background:#FFFFFF!important;border:1px solid #E5EAF2!important;border-radius:14px!important;overflow:hidden;}
[data-testid="stAlert"] {border-radius:12px!important;}
[data-testid="stVerticalBlockBorderWrapper"] {border-radius:16px!important;}
[data-baseweb="select"]>div, [data-baseweb="input"]>div, [data-testid="stDateInput"] input {background:#FFFFFF!important;border-color:#DCE4F0!important;color:#17243E!important;}
[data-baseweb="select"] *, [data-baseweb="input"] *, [data-testid="stDateInput"] input {color:#17243E!important;}
[data-testid="stSidebar"] hr {border-color:#E6EBF2!important;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {color:#233553!important;}
[data-testid="stRadio"] label, [data-testid="stSlider"] label, [data-testid="stMultiSelect"] label {color:#26364E!important;}
[data-testid="stWidgetLabel"] p {font-weight:650!important;color:#33445F!important;}
[data-testid="stDownloadButton"] button {background:#3458D4!important;color:white!important;border:0!important;border-radius:10px!important;font-weight:700!important;}
[data-testid="stDownloadButton"] button p {color:white!important;}
.hero-panel {background:linear-gradient(110deg,#233A74 0%,#3458D4 67%,#447BC8 100%);padding:26px 32px;border-radius:19px;margin-bottom:22px;box-shadow:0 10px 27px rgba(52,88,212,.16);}
.hero-panel .eyebrow {color:#CBD9FF;letter-spacing:.13em;font-weight:750;font-size:.72rem;}
.hero-panel .hero-title {color:#FFFFFF!important;font-size:clamp(1.55rem,2.35vw,2.45rem)!important;letter-spacing:-.04em;line-height:1.25;margin:9px 0 8px;font-weight:800;}
.hero-panel .hero-desc {color:#E5EDFF!important;font-size:.93rem;line-height:1.6;margin:0;}
.section-note {font-weight:700;color:#17243E;font-size:1rem;letter-spacing:-.02em;margin:.65rem 0 .7rem;}
.sidebar-mark {font-size:1.25rem;font-weight:800;color:#21335B;letter-spacing:-.04em;}
.sidebar-sub {color:#728098;font-size:.76rem;margin-top:1px;}
.footer-note {color:#70819B;font-size:.76rem;margin-top:1.25rem;}
@media(max-width:900px){.block-container{padding:1rem!important}.hero-panel{padding:20px}.hero-panel .hero-title{font-size:1.65rem!important}}
</style>""", unsafe_allow_html=True)

ROOT=Path(__file__).resolve().parent
DATA=ROOT/'b2b_transactions.csv.gz'
@st.cache_data(show_spinner="664 bin işlem kaydı hazırlanıyor…")
def load_data():
    if not DATA.exists():
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {DATA}")
    types={c:'string' for c in ['InvoiceNo','CustomerID','StockCode','Description','Category','City']}
    df=pd.read_csv(DATA, dtype=types, low_memory=False)
    quality={'rows':len(df), 'duplicates':int(df.duplicated().sum()),
             'missing_city':int(df.City.isna().sum()),'missing_category':int(df.Category.isna().sum()),
             'missing_qty':int(df.Quantity.isna().sum())}
    df['InvoiceDate']=pd.to_datetime(df.InvoiceDate, errors='coerce')
    for c in ['Quantity','NetPrice','UnitPrice']:
        df[c]=pd.to_numeric(df[c],errors='coerce')
    quality['invalid_rows']=int((df.InvoiceDate.isna() | df.CustomerID.isna() | df.StockCode.isna() |
                                 df.Quantity.isna() | (df.Quantity<=0) | df.NetPrice.isna() |
                                 (df.NetPrice<0)).sum())
    # Do not automatically remove identical entries: invoice line number is absent.
    df=df.loc[df.InvoiceDate.notna() & df.CustomerID.notna() & df.StockCode.notna() &
              df.Quantity.notna() & (df.Quantity>0) & df.NetPrice.notna() & (df.NetPrice>=0)].copy()
    df['Category']=df.Category.fillna('Bilinmiyor').str.strip().replace('', 'Bilinmiyor')
    df['City']=df.City.fillna('Bilinmiyor').str.strip().str.upper().replace('', 'Bilinmiyor')
    df['Description']=df.Description.fillna('Tanımsız')
    df['Revenue']=df.Quantity*df.NetPrice
    df['GrossListValue']=df.Quantity*df.UnitPrice.clip(lower=0)
    df['Month']=df.InvoiceDate.dt.to_period('M').dt.to_timestamp()
    df['YearMonth']=df.InvoiceDate.dt.strftime('%Y-%m')
    quality['valid_rows']=len(df)
    return df,quality

def money(v):
    return f"₺{v:,.0f}" if pd.notna(v) else '—'

def chart(fig, height=370):
    fig.update_layout(
        template="plotly_white", height=height,
        margin=dict(l=12,r=15,t=26,b=20),
        paper_bgcolor="#FFFFFF",plot_bgcolor="#FFFFFF",
        font=dict(family="Inter, Arial, sans-serif",color=INK,size=13),
        legend_title_text="",legend=dict(font=dict(size=12,color=MUTED)),
        hoverlabel=dict(bgcolor="#FFFFFF",font_color=INK,font_size=13),
        xaxis=dict(showgrid=False,zeroline=False,linecolor=GRID,tickfont=dict(size=12,color=MUTED),title_font=dict(color=MUTED,size=12)),
        yaxis=dict(showgrid=True,gridcolor=GRID,zeroline=False,tickfont=dict(size=12,color=MUTED),title_font=dict(color=MUTED,size=12))
    )
    fig.update_traces(selector=dict(type="bar"),marker_line_width=0,opacity=.95)
    st.plotly_chart(fig,use_container_width=True,config={"displayModeBar":False,"responsive":True})

def kpis(d):
    revenue=d.Revenue.sum(); units=d.Quantity.sum(); orders=d.InvoiceNo.nunique(); customers=d.CustomerID.nunique()
    for c,label,val in zip(st.columns(5),['Net satış*','Fatura sayısı','Satılan adet','Aktif müşteri','Fatura başı satış'],
                            [money(revenue),f'{orders:,}',f'{units:,.0f}',f'{customers:,}',money(revenue/orders) if orders else '—']):
        c.metric(label,val)

def rfm_table(d):
    if d.empty:return pd.DataFrame()
    reference=d.InvoiceDate.max()+pd.Timedelta(days=1)
    r=d.groupby('CustomerID',observed=True).agg(Last=('InvoiceDate','max'),Frequency=('InvoiceNo','nunique'),Monetary=('Revenue','sum'))
    r['Recency']=(reference-r.Last).dt.days
    # Rank based quantiles ensure deterministic 1–5 bins even with tied observations.
    for name,reverse in [('Recency',True),('Frequency',False),('Monetary',False)]:
        ranks=r[name].rank(method='first',ascending=not reverse)
        r[name[0]+'Score']=pd.qcut(ranks,5,labels=[1,2,3,4,5]).astype(int)
    r['RFM_Score']=r[['RScore','FScore','MScore']].sum(axis=1)
    r['Segment']=np.select([ (r.RScore>=4)&(r.FScore>=4),
                            (r.RScore>=3)&(r.FScore>=3),
                            (r.RScore<=2)&(r.FScore>=3),
                            (r.RScore<=2)&(r.FScore<=2)],
                          ['Şampiyonlar','Sadık müşteriler','Risk altındakiler','Uyuyan müşteriler'],
                          default='Gelişim potansiyeli')
    return r.reset_index()

def abc_table(d):
    t=d.groupby(['StockCode','Description'],observed=True,dropna=False).agg(Revenue=('Revenue','sum'),
        Units=('Quantity','sum'),Invoices=('InvoiceNo','nunique')).reset_index()
    t=t.sort_values('Revenue',ascending=False).reset_index(drop=True)
    total=t.Revenue.sum()
    t['CumulativeShare']=t.Revenue.cumsum()/total if total else 0
    t['ABC']=np.select([t.CumulativeShare<=.8,t.CumulativeShare<=.95],['A','B'],default='C')
    # First crossing product belongs to preceding tier so A/B classes include their targets.
    if total:
        prev=(t.Revenue.cumsum()-t.Revenue)/total
        t['ABC']=np.select([prev<.8,prev<.95],['A','B'],default='C')
    return t

def forecast_monthly(series, horizon=3):
    """Compare naive and linear-trend with rolling-origin validation; never train on holdout."""
    vals=series.to_numpy(dtype=float); n=len(vals)
    if n<5:return None
    errors={'Son dönem (naive)':[],'Doğrusal trend':[]}
    for stop in range(max(3,n-4),n):
        train=vals[:stop]; true=vals[stop]
        naive=train[-1]
        coef=np.polyfit(np.arange(stop),train,1)
        trend=max(0.,np.polyval(coef,stop))
        errors['Son dönem (naive)'].append(abs(true-naive))
        errors['Doğrusal trend'].append(abs(true-trend))
    maes={k:np.mean(v) for k,v in errors.items()}
    name=min(maes,key=maes.get)
    if name=='Doğrusal trend':
        coef=np.polyfit(np.arange(n),vals,1)
        pred=np.maximum(0.,np.polyval(coef,np.arange(n,n+horizon)))
    else:pred=np.repeat(vals[-1],horizon)
    future=pd.date_range(series.index[-1]+pd.offsets.MonthBegin(1),periods=horizon,freq='MS')
    return pd.DataFrame({'Month':future,'Forecast':pred}),name,maes

try:
    df,quality=load_data()
except Exception as e:
    st.error(f'Veri okunamadı: {e}');st.stop()

with st.sidebar:
    st.markdown('<div class="sidebar-mark">📚 B2B Intelligence</div><div class="sidebar-sub">ISL 533 · Karar Destek Stüdyosu</div>',unsafe_allow_html=True)
    st.divider()
    min_date,max_date=df.InvoiceDate.min().date(),df.InvoiceDate.max().date()
    date_range=st.date_input('Tarih aralığı',(min_date,max_date),min_value=min_date,max_value=max_date)
    if not isinstance(date_range,(tuple,list)) or len(date_range)!=2:
        st.info('Tarih aralığı için iki gün seçin.');st.stop()
    city_opts=sorted(df.City.unique().tolist());cat_opts=sorted(df.Category.unique().tolist())
    cities=st.multiselect('Şehir',city_opts,placeholder='Tüm şehirler')
    categories=st.multiselect('Kategori',cat_opts,placeholder='Tüm kategoriler')
    st.divider()
    st.caption('Kaynak: 2020 B2B kitap dağıtım işlemleri')
    st.caption('KPI ve tahminler seçilen filtrelere göre hesaplanır.')

mask=(df.InvoiceDate>=pd.Timestamp(date_range[0])) & (df.InvoiceDate<pd.Timestamp(date_range[1])+pd.Timedelta(days=1))
if cities:mask&=df.City.isin(cities)
if categories:mask&=df.Category.isin(categories)
d=df.loc[mask]
if d.empty:st.warning('Bu filtrelerle kayıt bulunamadı.');st.stop()

st.markdown('''<div class="hero-panel"><div class="eyebrow">ISL 533 · DATA ANALYTICS PROJECT</div><div class="hero-title">B2B Book Distribution Intelligence</div><p class="hero-desc">Satış performansı · Müşteri analitiği · Ürün portföyü · Talep tahmini<br>Veriye dayalı, etkileşimli yönetim karar destek paneli</p></div>''',unsafe_allow_html=True)
kpis(d)
st.caption('* Net satış = Quantity × NetPrice. NetPrice birim net fiyat kabul edilmiştir; para birimi TL varsayımı kaynak dosyada doğrulanmalıdır.')

tabs=st.tabs(['📈 Genel Bakış','🎯 Müşteri & RFM','📦 Ürün & ABC','🔮 Talep Tahmini','🧹 Veri Kalitesi & Metodoloji'])
with tabs[0]:
    monthly=d.groupby('Month',as_index=False).agg(Revenue=('Revenue','sum'),Units=('Quantity','sum'),Invoices=('InvoiceNo','nunique'))
    last=monthly.Revenue.iloc[-1];prev=monthly.Revenue.iloc[-2] if len(monthly)>1 else np.nan
    if pd.notna(prev) and prev>0:st.info(f'**Son gözlenen ay değişimi:** %{(last/prev-1)*100:+.1f} (önceki aya kıyasla).')
    a,b=st.columns([1.7,1])
    with a:
        st.subheader('Aylık satış trendi')
        fig=px.area(monthly,x='Month',y='Revenue',markers=True,labels={'Month':'Ay','Revenue':'Net satış (₺)'})
        fig.update_traces(line=dict(color=COLORS[0],width=3),fillcolor='rgba(52,88,212,.12)',marker=dict(size=8,color=COLORS[0]));chart(fig,420)
    with b:
        st.subheader('En yüksek satışlı kategoriler')
        top=d.groupby('Category').Revenue.sum().nlargest(9).sort_values()
        chart(px.bar(x=top.values,y=top.index,orientation='h',labels={'x':'Net satış (₺)','y':''},color_discrete_sequence=[COLORS[0]]),height=420)
    a,b=st.columns(2)
    with a:
        st.subheader('Şehirlere göre satış')
        t=d.groupby('City').Revenue.sum().nlargest(12).sort_values()
        chart(px.bar(x=t.values,y=t.index,orientation='h',labels={'x':'Net satış (₺)','y':''},color_discrete_sequence=[COLORS[1]]),height=450)
    with b:
        st.subheader('Aylık fatura ve birim hareketi')
        option=st.radio('Ölçü',['Fatura','Adet'],horizontal=True,key='general_measure')
        col='Invoices' if option=='Fatura' else 'Units'
        chart(px.bar(monthly,x='Month',y=col,labels={'Month':'Ay',col:option},color_discrete_sequence=[COLORS[0]]),height=400)
    st.markdown('**Yönetim yorumu:** Aylık satış değişimleri, yoğun bölgeler ve büyük kategoriler birlikte izlenerek satış hedefleri ve kampanya odağı belirlenebilir.')

with tabs[1]:
    st.subheader('Müşteri segmentasyonu | RFM')
    st.caption('Recency: son işleme kadar gün; Frequency: farklı fatura sayısı; Monetary: tahmini net satış. Eşikler seçilen veri alt kümesinden hesaplanır.')
    r=rfm_table(d)
    a,b,c=st.columns(3)
    a.metric('Müşteri sayısı',f'{len(r):,}')
    b.metric('Müşteri başına satış',money(r.Monetary.mean()))
    c.metric('En büyük %20 müşteri satış payı',f'%{r.nlargest(max(1,int(np.ceil(len(r)*.2))),"Monetary").Monetary.sum()/r.Monetary.sum()*100:.1f}' if r.Monetary.sum()>0 else '—')
    a,b=st.columns(2)
    with a:
        seg=r.groupby('Segment',as_index=False).agg(Customers=('CustomerID','count'),Revenue=('Monetary','sum'))
        st.subheader('Segment büyüklükleri')
        chart(px.bar(seg,x='Segment',y='Customers',color='Segment',labels={'Customers':'Müşteri sayısı','Segment':''}),400)
    with b:
        st.subheader('Segmentlerin satış payı')
        chart(px.pie(seg,values='Revenue',names='Segment',hole=.55),400)
    st.subheader('Müşteri önceliklendirme listesi')
    chosen=st.multiselect('Segment seçimi',sorted(r.Segment.unique()),default=sorted(r.Segment.unique()))
    show=r.loc[r.Segment.isin(chosen),['CustomerID','Recency','Frequency','Monetary','RFM_Score','Segment']].sort_values('Monetary',ascending=False)
    st.dataframe(show.head(1500),hide_index=True,use_container_width=True,column_config={'Monetary':st.column_config.NumberColumn('Satış (₺)',format='%.2f')})
    st.download_button('⬇️ Tüm RFM analizini indir',r.to_csv(index=False).encode('utf-8-sig'),'rfm_segments.csv','text/csv')
    st.info('**Aksiyon:** Risk altındaki değerli müşteriler için geri kazanım; şampiyonlar için sadakat ve çapraz satış kampanyaları tasarlanabilir.')

with tabs[2]:
    st.subheader('Ürün portföyü ve ABC analizi')
    abc=abc_table(d)
    summary=abc.groupby('ABC',as_index=False).agg(Products=('StockCode','count'),Revenue=('Revenue','sum'),Units=('Units','sum'))
    a,b=st.columns(2)
    with a:
        st.subheader('ABC sınıflarının satış katkısı')
        chart(px.bar(summary,x='ABC',y='Revenue',color='ABC',category_orders={'ABC':['A','B','C']},
                     labels={'Revenue':'Net satış (₺)','ABC':'ABC sınıfı'}),385)
    with b:
        st.subheader('Ürün sayısının dağılımı')
        chart(px.pie(summary,values='Products',names='ABC',hole=.5),385)
    st.caption('ABC: Kümülatif satış payı ilk yaklaşık %80 A, sonraki %15 B, kalan %5 C. Sınırı aşan ürün ilgili üst sınıfta tutulur.')
    st.subheader('Ürün listesi')
    abc_group=st.multiselect('ABC filtresi',['A','B','C'],default=['A','B','C'])
    show=abc.loc[abc.ABC.isin(abc_group),['StockCode','Description','Units','Revenue','Invoices','CumulativeShare','ABC']]
    st.dataframe(show.head(2000),use_container_width=True,hide_index=True)
    st.download_button('⬇️ ABC ürün listesini indir',abc.to_csv(index=False).encode('utf-8-sig'),'abc_products.csv','text/csv')
    st.info('**Aksiyon:** A ürünleri tedarik önceliğine alınabilir; düşük hareketli C ürünleri için katalog ve promosyon değerlendirmesi yapılabilir. Gerçek stok seviyesi bilinmiyor.')

with tabs[3]:
    st.subheader('Öngörüsel analiz | Aylık talep tahmini')
    st.warning('Veri yalnızca 2020 yılını kapsıyor. Tahminler kısa geçmişe dayalı senaryo niteliğindedir; geleceğe ilişkin kesin beklenti değildir.')
    measure=st.radio('Tahmin hedefi',['Satış tutarı','Satılan adet'],horizontal=True)
    periods=st.slider('Tahmin ufku (ay)',1,6,3)
    target='Revenue' if measure=='Satış tutarı' else 'Quantity'
    # Resample to continuous month starts and explicitly include zero-activity months in the selected period.
    s=d.set_index('InvoiceDate')[target].resample('MS').sum()
    if len(s)<5:
        st.warning('Tahmin için seçili tarihlerde en az 5 aylık dönem bulunmalıdır.')
    else:
        result=forecast_monthly(s,periods)
        f,method,maes=result
        histor=pd.DataFrame({'Ay':s.index,'Gerçek':s.values})
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=histor.Ay,y=histor.Gerçek,mode='lines+markers',name='Gözlenen',line=dict(color=COLORS[1],width=3)))
        fig.add_trace(go.Scatter(x=[s.index[-1],*f.Month],y=[s.iloc[-1],*f.Forecast],mode='lines+markers',name='Tahmin',line=dict(color=COLORS[3],width=3,dash='dash')))
        fig.update_layout(yaxis_title='TL' if target=='Revenue' else 'Adet',xaxis_title='Ay')
        chart(fig,460)
        a,b,c=st.columns(3)
        a.metric('Seçilen model',method)
        b.metric('Geriye dönük MAE',f'{maes[method]:,.1f}')
        c.metric('Gelecek ay tahmini',f'{f.Forecast.iloc[0]:,.0f}')
        display=f.copy();display.columns=['Ay','Öngörü'];display['Ay']=display['Ay'].dt.strftime('%Y-%m')
        st.dataframe(display,use_container_width=True,hide_index=True)
        st.download_button('⬇️ Tahmini indir',display.to_csv(index=False).encode('utf-8-sig'),'monthly_forecast.csv','text/csv')
        with st.expander('Model seçimi ve doğrulama ayrıntısı'):
            st.write('Zaman sıralı ileriye dönük test: Son en fazla dört ay için her adımda yalnızca geçmiş dönemlerle model kurulur; tek dönem ileri tahminin mutlak hatası ölçülür. Ortalama mutlak hatası (MAE) küçük olan model seçilir. Modeller: son ayı tekrar eden naive yöntem ve doğrusal trend. Gelecek tahminler sıfırın altına düşmez.')
            st.dataframe(pd.DataFrame({'Yöntem':list(maes),'MAE':list(maes.values())}),hide_index=True)
        st.info('**Tedarik planlama:** Aylık adet talebinin yönü için kullanılabilir; stok, temin süresi, maliyet ve teslimat verileri olmadan güvenlik stoğu veya sipariş noktası hesaplanamaz.')

with tabs[4]:
    st.subheader('Veri kalite kontrolü')
    metrics=[('Ham satır',quality['rows']),('Analizde kullanılan satır',quality['valid_rows']),
             ('Dışlanan geçersiz satır',quality['invalid_rows']),('Aynı görünen satır',quality['duplicates']),
             ('Eksik şehir',quality['missing_city']),('Eksik kategori',quality['missing_category']),('Eksik adet',quality['missing_qty'])]
    a,b,c=st.columns(3)
    for i,(name,val) in enumerate(metrics):[a,b,c][i%3].metric(name,f'{val:,}')
    st.divider()
    st.markdown('''**Uygulanan kurallar**
- Tarih alanı tarihe; miktar ve fiyatlar sayısal türe dönüştürüldü.
- Geçersiz tarih / müşteri / ürün, boş veya sıfır-negatif adet, negatif net birim fiyat içeren satırlar dışlandı.
- Boş şehir veya kategori `Bilinmiyor` etiketiyle korundu.
- Yinelenen satırlar **silinmedi**: Fatura satır numarası olmadığı için tekrarların gerçekten hatalı olduğu doğrulanamaz.
- Net satış hesabı `Quantity × NetPrice`; ürün düzeyinde `NetPrice` birim fiyat olarak yorumlandı.
- `UnitPrice` liste/baz fiyat gibi ele alındı fakat indirim oranları kesinleşmiş ticari iskonto olarak adlandırılmadı.
- Fatura sayısı `InvoiceNo.nunique()`, müşteri sayısı `CustomerID.nunique()` şeklinde hesaplandı.
- RFM ve ABC, mevcut filtrelenen veri üzerinde yeniden hesaplanır; tarih aralığı kısaldığında segmentler değişebilir.
- Tahmin yalnızca ölçülen aylık seriye dayanır, dışsal ekonomik değişken veya tedarik verisi içermez.''')
    st.subheader('Ham veri örneği (filtrelenmiş)')
    st.dataframe(d[['InvoiceNo','CustomerID','InvoiceDate','StockCode','Description','Category','City','Quantity','NetPrice','Revenue']].head(300),use_container_width=True,hide_index=True)
    st.download_button('⬇️ Filtrelenmiş veriyi indir',d.to_csv(index=False).encode('utf-8-sig'),'filtered_transactions.csv','text/csv')
    st.caption('Not: Kaynak dosyada para birimi tanımı, maliyet, stok miktarı, sevkiyat tarihi ve iadelerin muhasebesel niteliği açıklanmamıştır.')

st.divider()
st.markdown('<div class="footer-note">ISL 533 · B2B Book Distribution Intelligence  |  Eğitim amaçlı analitik karar destek uygulaması</div>',unsafe_allow_html=True)