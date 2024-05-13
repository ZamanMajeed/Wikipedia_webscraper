from bs4 import BeautifulSoup
import requests
import pandas as pds
import matplotlib.pyplot as plt

url = 'https://en.wikipedia.org/wiki/List_of_largest_companies_in_the_United_States_by_revenue'

page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser' )

table = soup.find_all('table')[1]
world_titles = soup.find_all('th')

table_titles = [title.text.strip() for title in world_titles][0:7]

data_frame = pds.DataFrame(columns = table_titles)

col_data = table.find_all('tr')

for row in col_data[1:]:
    row_data = row.find_all('td')
    row_raw_data = [data.text.strip() for data in row_data]
    #print(row_raw_data)
    data_frame.loc[len(data_frame)] = row_raw_data

data_frame['Revenue (USD millions)'] = data_frame['Revenue (USD millions)'].str.replace(',', '').astype(float)

plt.figure(figsize=(15, 6))
plt.bar(data_frame['Name'][0:9], data_frame['Revenue (USD millions)'][0:9], color='skyblue')
plt.title('Revenue of Top 10 US Companies', fontsize=16, fontweight='bold')
plt.xlabel('Company Name',fontsize=14)
plt.ylabel('Revenue in USD (Millions)',fontsize=14)
plt.show()

data_frame.to_csv('company_data.csv', index=False)
