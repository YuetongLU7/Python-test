import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# sheet_name spécifie le table à lire
df = pd.read_excel(r'input_data/test.csv', sheet_name='TableauPrincipal')

# Extraire le partie date
df['date_only'] = pd.to_datetime(df['StrTime']).dt.date

# Regrouper par date et compter le nombre d'enrgistrements de message
chat_count = df.groupby('date_only').size().reset_index(name='count')
# print(chat_count)

#
# D: calendar day frequency
date_range = pd.date_range(chat_count['date_only'].min(), chat_count['date_only'].max(), freq='D')
# print(date_range)

full_date_range = pd.DataFrame(date_range, columns=['date_only'])
# print(full_date_range)

# Assurer que les deux colonnes de date sont de type datetime
full_date_range['date_only'] = pd.to_datetime(full_date_range['date_only'])
chat_count['date_only'] = pd.to_datetime(chat_count['date_only'])


chat_count_full = pd.merge(full_date_range, chat_count, on='date_only', how='left').fillna(0)

# Convertir en vue calendrier
chat_count_full['month'] = chat_count_full['date_only'].dt.month
chat_count_full['day'] = chat_count_full['date_only'].dt.day
chat_count_full['weekday'] = chat_count_full['date_only'].dt.weekday  # 0: Monday, 6: Sunday

# Ajuster le jour de la semaine de lundi à dimanche au dimanche au samedi pour un arrangement facile
chat_count_full['weekday'] = (chat_count_full['weekday'] + 1) % 7

# Créer une nouvelle colonne indiquant à quelle semaine appartient la date
chat_count_full['week'] = chat_count_full['date_only'].apply(lambda x: x.strftime('%Y-%U'))


heatmap_data = chat_count_full.pivot_table(index='week', columns='weekday', values='count', aggfunc='sum', fill_value=0)

fig_width = 12
fig_height = max(20, len(date_range) // 7)


plt.figure(figsize=(fig_width, fig_height))


ax = sns.heatmap(heatmap_data, cmap='YlGnBu', annot=False, fmt=".0f", cbar_kws={'label': 'Number of Messages'},
                 linewidths=0.5, square=True, annot_kws={"size": 10},
                 xticklabels=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])


for y in range(heatmap_data.shape[0]):
    for x in range(heatmap_data.shape[1]):
        week = heatmap_data.index[y]
        weekday = heatmap_data.columns[x]

        day_data = chat_count_full[(chat_count_full['week'] == week) & (chat_count_full['weekday'] == weekday)]

        if not day_data.empty:

            month = day_data['month'].values[0]
            day_of_month = day_data['day'].values[0]
            ax.text(x + 0.5, y + 0.5, f"{month}-{day_of_month}", ha='center', va='center', fontsize=8, color='orange')


plt.title('Chat Record Frequency Heatmap')


plt.xticks(rotation=0)
plt.yticks(rotation=0)

plt.savefig(f'figs/HeatMap.png')

