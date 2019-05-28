import pandas as pd

df = pd.DataFrame()
df['timestamp'] = timestamp
df['sn'] = sn
df['text'] = text
df['favcount'] = fav_count


print(df)
print('------')
print(df['favcount'].max())