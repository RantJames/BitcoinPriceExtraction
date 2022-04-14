import pandas as pd
import matplotlib.pyplot as plt
import requests
import streamlit as st


API_URL="https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=cad&days=90&interval=daily"

st.title("Bitcoin Prices")
num_days=st.slider('No. of Days', 1, 365, 90)

currency_list = ['cad','usd', 'inr']
currency = st.radio('Currency',currency_list)

payload = {'vs_currency': currency,'days': num_days,'interval':'daily'}

@st.cache
def load_data():
    req = requests.get(API_URL, payload)
    if(req.status_code==200):
        data=req.json()
    raw_data = data['prices']
    cols = ['Date','Price']
    dataFrame = pd.DataFrame(data=raw_data, columns=cols)
    dataFrame['Date'] = pd.to_datetime(dataFrame['Date'], unit='ms')
    dataFrame.head()
    return dataFrame

df = load_data()

fig, ax = plt.subplots(figsize=(16,6))
ax.plot(df['Date'], df['Price'])
ax.set_ylim(ymin=0)
ax.set_xlabel('Date', fontsize=18)
ax.set_ylabel(f"Price in {currency}",fontsize=18)
st.pyplot(fig)

st.text(f"Average price during this period is {df['Price'].mean()} {currency}")
