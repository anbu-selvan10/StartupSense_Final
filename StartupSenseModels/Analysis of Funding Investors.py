#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv('F:\\StartupSenseModels\\startup_funding.csv')


# In[3]:


df.head()


# In[4]:


df['Investors Name']= df['Investors Name'].fillna('Undisclosed')


# In[5]:


df.drop(columns=['Remarks'], inplace = True)


# In[6]:


df.set_index('Sr No', inplace = True)


# In[7]:


df.head(2)


# In[8]:


df.rename(columns={
    'Date dd/mm/yyyy':'Date',
    'Startup Name':'Startup',
    'Industry Vertical':'Vertical',
    'Sub Vertical':'Subvertical',
    'City Location':'City',
    'Investors Name':'Investors',
    'Investment Type':'Round',
    'Amount in USD':'Amount'    
},inplace=True)


# In[9]:


df.head(10)


# In[10]:


df['Amount'] = df['Amount'].fillna('0')


# In[11]:


df['Amount'] = df['Amount'].str.replace(',','')
df['Amount'] = df['Amount'].str.replace('undisclosed','0')
df['Amount'] = df['Amount'].str.replace('unknown','0')
df['Amount'] = df['Amount'].str.replace('Undisclosed','0')


# In[12]:


df = df[df['Amount'].str.isdigit()]


# In[13]:


df['Amount'] = df['Amount'].astype('float')


# In[14]:


df.info()


# In[15]:


df.head()


# In[16]:


def to_inr_crore(dollar):
    inr = dollar * 82.74
    return inr/10000000


# In[17]:


df['Amount'] = df['Amount'].apply(to_inr_crore)


# In[18]:


df.head()


# In[19]:


df['Date'] = df['Date'].str.replace('05/072018','05/07/2018')


# In[20]:


df['Date'] = pd.to_datetime(df['Date'], dayfirst = True, errors = 'coerce')


# In[21]:


df['Date'].dt.month


# In[22]:


df['Date'].dt.year


# In[23]:


df = df.dropna(subset=['Date','Startup','Vertical','City','Investors','Round','Amount'])


# In[24]:


df.info()


# In[25]:


df[(df['Vertical'] == 'eCommerce') | (df['Vertical'] == 'ECommerce') | (df['Vertical'] == 'Ecommerce')] = 'E-Commerce'
df[df['City'] == 'Bengaluru'] = 'Bangalore'


# In[26]:


df = df.drop(columns=['Subvertical'])


# # Data Visualization

# In[72]:


investor = "SoftBank Vision Fund"
investor_dup = " SoftBank Vision Fund"


# In[73]:


data = df[(df['Investors'].str.contains(investor)) | (df['Investors'].str.contains(investor_dup))].groupby('City')['Amount'].sum()
 
sizes = data
labels = data.index

plt.figure(figsize=(10,8))

plt.title('City')

plt.pie(sizes)

percentages = [f'{label} - {size/sum(sizes)*100:.1f}%' for label, size in zip(labels, sizes)]

plt.legend(percentages, loc='upper left', bbox_to_anchor=(1,1))

plt.show()


# In[74]:


data = df[(df['Investors'].str.contains(investor)) | (df['Investors'].str.contains(investor_dup))].groupby('Round')['Amount'].sum()

sizes = data
labels = data.index

plt.figure(figsize=(10,8))

plt.title('Rounds')

plt.pie(sizes)

percentages = [f'{label} - {size/sum(sizes)*100:.1f}%' for label, size in zip(labels, sizes)]

plt.legend(percentages, loc='upper left', bbox_to_anchor=(1,1))

plt.show()


# In[75]:


df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

grouped_data = df[
    (df['Investors'].str.contains(investor)) | 
    (df['Investors'].str.contains(investor_dup))
].groupby(df['Date'].dt.year)['Amount'].sum()

plt.figure(figsize=(10,6))
plt.plot(grouped_data.index, grouped_data.values, marker='o', linestyle='-')
plt.title('Yearly investments')
plt.xlabel('Year')
plt.ylabel('Sum of Amounts In Crores')
plt.grid(True)
plt.tight_layout()

plt.show()


# In[76]:


data = df[(df['Investors'].str.contains(investor)) | (df['Investors'].str.contains(investor_dup))].groupby('Vertical')['Amount'].sum()

sizes = data
labels = data.index

plt.figure(figsize=(10,8))

plt.title('Industry')

plt.pie(sizes)

percentages = [f'{label} - {size/sum(sizes)*100:.2f}%' for label, size in zip(labels, sizes)]

plt.legend(percentages, loc='upper left', bbox_to_anchor=(1,1))

plt.show()


# In[71]:


df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df.dropna(subset=['Amount'], inplace=True)
top_investors = df.groupby('Investors')['Amount'].sum().sort_values(ascending=False).head(20)
print(top_investors)


# In[ ]:




