# Modules used 
import numpy as np 
import pandas as pd 
import glob 
import matplotlib.pyplot as plt
import seaborn as sns

# Data Collection
data_all = glob.glob("D:/vs/SDA/*.csv")
df = []
for file in data_all:
    sf = pd.read_csv(file)
    df.append(sf)

df = pd.concat(df , ignore_index=True)
print(df.head())

# Data Modification and Clearing
print(df.describe())
print(df.isnull().sum())

df_fill = df.apply(lambda x: x.fillna(x.mean()) if x.dtype.kind in 'biufc' else x)
print(df_fill.isnull().sum())

df_clean = df.dropna()
print(df_clean.isnull().sum())
print(df_clean)
print(df_fill.dtypes)

# finding mean of every stock at closing period
avg_close = df_fill.groupby('Symbol')['Close'].mean()
print(avg_close)

# Finding mean value of stock weekly closing price

#converting date into datetime frame
try:
    df_fill['Date'] = pd.to_datetime(df_fill['Date'])
except:
    print(f"Error converting 'Date' to datetime : {e}")

df_fill.set_index('Date', inplace=True)

#Resampling df_fill to calculate weekly mean
try:
    weekly_mean = df_fill['Close'].resample('W').mean()
    print(weekly_mean)
except KeyError:
    print("Error: 'Close' column not found in df_fill")
except Exception as e:
    print(f"An error occurred : {e}")

# Now Calcuating MACD indicator
short_term_window = 12
long_term_window = 26
df_fill['ShortEMA'] = df_fill['Close'].ewm(span=short_term_window,adjust=False).mean()
df_fill['LongEMA'] = df_fill['Close'].ewm(span=long_term_window,adjust=False).mean()
df_fill['MACD'] = df_fill['ShortEMA'] - df_fill['LongEMA']

# Ploting MACD 

plt.figure(figsize=(25,12))
plt.plot(df_fill.index, df_fill['MACD'], label = 'MACD', color = 'Red')
plt.axhline(y=0)
plt.xlabel('Date')
plt.ylabel('MACD Value')
plt.title('MACD Indicator')
plt.legend()
plt.show()


# Average closing price
df['Date'] = df['Date'].astype(str)
df_sub = df.iloc[:len(avg_close)]

plt.figure(figsize=(25,12))
plt.plot(df_sub['Date'],avg_close,label = 'Average Closing Price',color = 'Red')
plt.title('Average Closing Price')
plt.xlabel('Date')
plt.xticks(rotation = 90, ha = 'right')
plt.ylabel('Avgerage Closing Price')
plt.legend()
plt.show()

# Box plot for close price according to different stocks

df_fill['Symbol'] = df_fill['Symbol'].astype('category')

plt.figure(figsize=(25,12))
sns.boxplot(x ='Symbol',y = 'Close', data = df_fill, whis = 1.5)
plt.xticks(rotation =90,fontsize = 7)
plt.title('Box Plot For Closing Prices Of Different Stocks')
plt.show()

# Now lets Compare some specific stocks
dn_1 = pd.read_csv('BPCL.csv')
dn_2 = pd.read_csv('GAIL.csv')
dn_3 = pd.read_csv('ONGC.csv')
dn_4 =pd.read_csv('RELIANCE.csv')

# Plot their closing price over different time 
plt.figure(figsize=(25,12))

sns.lineplot(x ='Date',y = 'Close',data = dn_1, label = 'BPCL')
sns.lineplot(x ='Date',y = 'Close',data = dn_2, label = 'GAIL')
sns.lineplot(x ='Date',y = 'Close',data = dn_3, label = 'ONGC')
sns.lineplot(x ='Date',y = 'Close',data = dn_4, label = 'RELIANCE')
plt.show()
