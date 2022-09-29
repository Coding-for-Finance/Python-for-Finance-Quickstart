# %% Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% Data loading preprocesing and exploration

# load excel with pandas, recognizing the tabular format
raw_prices = pd.read_excel('spy_nasdaq_prices.xlsx', header=0)

# use index locator (iloc) of 0 (first entry) to see what first date is
first_date = raw_prices.iloc[0,0]
# use index locator (iloc) of -1 (last entry) to see what last date is
last_date = raw_prices.iloc[-1,0]

# make a quick check whether data is in the right order
if first_date < last_date:
    print('Data is in the correct order')
else:
    print('Data is in the incorrect order, needs to be flipped!')

raw_prices_flipped = raw_prices.iloc[::-1]

## let's set up a function for checking and flipping if necessary

def check_flip(df, index_col):
    first_date = df.iloc[0,0]
    last_date = df.iloc[-1,0]

    if first_date < last_date:
        print('Data is in the correct order')
        df_to_return = df
    else:
        print('Data is in the incorrect order, returning flipped df')
        df_to_return = df.iloc[::-1]
    return df_to_return

raw_prices_flipped_from_function = check_flip(raw_prices,0)

# test the function with correct order
test = check_flip(raw_prices_flipped_from_function,0)

# use "Date" column as index
df_prices = raw_prices_flipped.set_index('Date')

# define another more desirable start for our prices df
new_start = '2012-02-02'
# we use "loc" which takes the concrete label of an index in comparison to "iloc" which
# take the positional value. new_start: means from our defined date till the end
df_prices_cut = df_prices.loc[new_start:,:]

# let's now calculate the returns and drop the first NA observation
df_returns = df_prices_cut.pct_change(1).dropna()
# explore the returns data
df_returns.describe()
# plot the performance of the indices
(1+df_returns).cumprod().plot()
plt.title('NAV of SPY and QQQ indices')
plt.ylabel('NAVs')
plt.show()

# %% For loop fore creating a moving average

# parameters, how many takes to calculate the moving average
MA_days = 120
# create an empty dataframe to store the results
df_MAs = pd.DataFrame(index=df_prices_cut.index, columns= df_prices_cut.keys() + '_MA')

# Option No.1: create a for loop to calculate and store MA
for i in range(MA_days, len(df_MAs)):
    # begin writing in position 6, taking the value of mean of prices from the past six days and go forward
    df_MAs.iloc[i, : ] = df_prices_cut.iloc[i-MA_days:i,:].mean(axis=0)

# Option No.2: use a rolling mean function
df_MAs_2 = df_prices_cut.rolling(MA_days).mean()

# concatenate the original prices and MAs dataframe
df_all = pd.concat([df_prices_cut, df_MAs], axis= 1)

# plot the prices with the moving averages
df_all.plot(style = ['-','-','--','--']) # make prices a solid and MAs a dashed line
plt.title(f'Prices and {MA_days}-Days Moving Averages of the Indices ')
plt.show()


