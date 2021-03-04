import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
st.set_option('deprecation.showPyplotGlobalUse', False)
import streamlit.components.v1 as stc
#--------------------------------#
#Utils 

@st.cache
def load_dataset():
	df = pd.read_excel('https://github.com/luishernand/crypto_analysis/blob/main/data/crypto_data.xlsx', sheet_name='data')
	df.set_index('Date', inplace=True)
	return df

#-------------------------------------------------#
# Title 
HTML_BANNER = """
    <div style="background-color:#8B0000;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Crypto Currency Analysis</h1>
    <p style="color:white;text-align:center;">Built with: luishernadezmatos@yahoo.com</p>
    </div>
    """

stc.html(HTML_BANNER)

st.markdown('''
	**Description:** This is web app `Crypto Coins` currency Analysis
	''')

#-----------------------------------------------------------------#
#main
df= load_dataset()



menu = ['Analysis', 'Visualizations']
choice = st.sidebar.selectbox('Menu', menu)
analysis_menu= ['Show Data Structure', 'Daily Analysis']

#### Analysis
DSR = df.pct_change(1)
DCSR = (DSR+1).cumprod()



#Body

if choice == 'Analysis':
	st.subheader("Crypto Analysis")
	sub_menu = st.sidebar.radio('Sub_Menu', analysis_menu)

	if sub_menu =='Show Data Structure':
		st.table(df.head())
		dimension=  st.radio('Dimension',options =['Rows', 'Columns'])
		if dimension =='Rows':
			st.write(df.shape[0])
		elif dimension =='Columns':
			st.write(df.shape[1])
		else:
			st.write(df.shape)

	#See columns
		view_columns= st.checkbox('View Columns')
		if view_columns:
			all_columns = df.columns.tolist()
			select_columns = st.multiselect('Select a Column', all_columns, default=['BTC'])
			new_df = df[select_columns]
			st.write(new_df)

	#tats
		if st.checkbox('Stat'):
			st.write(df.describe())

## Submenu Daily Analysis
	else:	
		if st.checkbox('Daily Simple Return'):
			st.write(DSR)

		if st.checkbox('Volativity'):
			st.write(DSR.std())

		if st.checkbox('Daily Simple Return Mean'):
			st.write(DSR.mean())

		if st.checkbox('Daily Acumualtive Return'):
			st.write(DCSR)


else:
	st.subheader('Visualizations plots')
	all_columns = df.columns.tolist()
	select_columns = st.sidebar.multiselect("Select to Visualizations plots", all_columns, default=all_columns)
	new_df = df[select_columns]
	
	if st.checkbox('Graph  Data Frame'):
		st.subheader('Crypto Currency Price USD($)')
		st.line_chart(new_df)
	if st.checkbox('Scale Data'):
		minmax = MinMaxScaler()
		scale = minmax.fit_transform(df)
		df_scale = pd.DataFrame(scale, columns= df.columns)
		df_scale.set_index(pd.DatetimeIndex(df.index), inplace=True)
		st.subheader('Crypto Currency scale')
		df_scale_new = df_scale[select_columns]
		st.line_chart(df_scale_new)

	if st.checkbox('Get the dailys plots'):
		dailys = st.radio('Plot Daily Return',  ['Simple', 'Acumualtive'])
	
		if dailys == 'Simple':
			df_DR = DSR[select_columns]
		else:
			df_DR = DCSR[select_columns]

		st.line_chart(df_DR)

	if st.checkbox('Correlations plots'):
		st.subheader('Correlations of dataset')
		sns.heatmap(new_df.corr(), annot=True, fmt='.2%', cmap = 'viridis')
		st.pyplot()


