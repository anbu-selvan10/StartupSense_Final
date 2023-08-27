import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('F:\\StartupSense_Final\\StartupSenseModels\\startup_funding.csv')

df['Investors Name']= df['Investors Name'].fillna('Undisclosed')
df.drop(columns=['Remarks'], inplace = True)
df.set_index('Sr No', inplace = True)

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

df['Amount'] = df['Amount'].fillna('0')
df['Amount'] = df['Amount'].str.replace(',','')
df['Amount'] = df['Amount'].str.replace('undisclosed','0')
df['Amount'] = df['Amount'].str.replace('unknown','0')
df['Amount'] = df['Amount'].str.replace('Undisclosed','0')
df = df[df['Amount'].str.isdigit()]
df['Amount'] = df['Amount'].astype('float')

def to_inr_crore(dollar):
    inr = dollar * 82.74
    return inr/10000000

df['Amount'] = df['Amount'].apply(to_inr_crore)
df['Date'] = df['Date'].str.replace('05/072018','05/07/2018')
df['Date'] = pd.to_datetime(df['Date'], dayfirst = True, errors = 'coerce')
df = df.dropna(subset=['Date','Startup','Vertical','City','Investors','Round','Amount'])

df[(df['Vertical'] == 'eCommerce') | (df['Vertical'] == 'ECommerce') | (df['Vertical'] == 'Ecommerce')] = 'E-Commerce'
df[df['City'] == 'Bengaluru'] = 'Bangalore'
df = df.drop(columns=['Subvertical'])


def city(investor):
    investor_dup = f" {investor}"

    data = df[(df['Investors'].str.contains(investor)) | (df['Investors'].str.contains(investor_dup))].groupby('City')['Amount'].sum()

    sizes = data
    labels = data.index

    plt.figure(figsize=(12,6))

    plt.title('City')

    plt.pie(sizes)

    percentages = [f'{label} - {size/sum(sizes)*100:.1f}%' for label, size in zip(labels, sizes)]

    plt.legend(percentages, loc='upper left', bbox_to_anchor=(1,1))


def round(investor):
    investor_dup = f" {investor}"

    data = df[(df['Investors'].str.contains(investor)) | (df['Investors'].str.contains(investor_dup))].groupby('Round')['Amount'].sum()

    sizes = data
    labels = data.index

    plt.figure(figsize=(12,6 ))  #changing fig  

    plt.title('Rounds')

    plt.pie(sizes)

    percentages = [f'{label} - {size/sum(sizes)*100:.1f}%' for label, size in zip(labels, sizes)]

    plt.legend(percentages, loc='upper left', bbox_to_anchor=(1,1))


def date(investor):

    investor_dup = f" {investor}"

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    grouped_data = df[
        (df['Investors'].str.contains(investor)) | 
        (df['Investors'].str.contains(investor_dup))
    ].groupby(df['Date'].dt.year)['Amount'].sum()

    plt.figure(figsize=(12,6))
    plt.plot(grouped_data.index, grouped_data.values, marker='o', linestyle='-')
    plt.title('Yearly investments')
    plt.xlabel('Year')
    plt.ylabel('Sum of Amounts In Crores')
    plt.grid(True)
    plt.tight_layout()


def vertical(investor):
    investor_dup = f" {investor}"
    
    data = df[(df['Investors'].str.contains(investor)) | (df['Investors'].str.contains(investor_dup))].groupby('Vertical')['Amount'].sum()

    sizes = data
    labels = data.index

    plt.figure(figsize=(12,6))

    plt.title('Industry')

    plt.pie(sizes)

    percentages = [f'{label} - {size/sum(sizes)*100:.2f}%' for label, size in zip(labels, sizes)]

    plt.legend(percentages, loc='upper left', bbox_to_anchor=(1,1))
