# --------------------------------------------
# Student: Soam Parkash | Registration No: 12301024
# Subject Code: INT375
# Faculty: Ms. Maneet Kaur
# --------------------------------------------

# -- coding: utf-8 --

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# CSV data
df = pd.read_csv("/Users/maneetkumar/Downloads/7150_source_data.csv")

# Cleaning Part
df.columns = df.columns.str.strip()

# NA cleaning
print("Missing values before cleaning:\n", df.isna().sum())

# Filling missing numeric columns with 0
num_cols = df.select_dtypes(include=['number']).columns
df[num_cols] = df[num_cols].fillna(0)

# Filling missing object (text) columns with 'Unknown'
cat_cols = df.select_dtypes(include=['object']).columns
df[cat_cols] = df[cat_cols].fillna('Unknown')

# Converting date column to datetime format
df['As on Date'] = pd.to_datetime(df['As on Date'], errors='coerce')

# Rows where state name is missing
df = df.dropna(subset=['srcStateName'])

# After cleaning
print("\nMissing values after cleaning:\n", df.isna().sum())
print("\nCleaned DataFrame Preview:\n", df.head())

# Set plot style
sns.set(style="whitegrid")

# 1. Line Chart - Pending cases over the years
yearly_pending = df.groupby('srcYear')['Pending cases'].sum().reset_index()
plt.figure(figsize=(10, 6))
sns.lineplot(data=yearly_pending, x='srcYear', y='Pending cases', marker='o', color='darkblue')
plt.title("Total Pending Cases Over the Years")
plt.xlabel("Year")
plt.ylabel("Pending Cases")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Bar Chart - Top 10 states with most pending cases
top_states = df.groupby('srcStateName')['Pending cases'].sum().nlargest(10).reset_index()
plt.figure(figsize=(10, 6))
sns.barplot(data=top_states, x='Pending cases', y='srcStateName', palette='viridis')
plt.title("Top 10 States by Pending Cases")
plt.xlabel("Pending Cases")
plt.ylabel("State")
plt.tight_layout()
plt.show()

# 3. Horizontal Bar - Age-wise pending cases distribution
age_columns = [
    'Pending cases for a period of 0 to 1 Years',
    'Pending cases for a period of 1 to 3 Years',
    'Pending cases for a period of 3 to 5 Years',
    'Pending cases for a period of 5 to 10 Years',
    'Pending cases for a period of 10 to 20 Years',
    'Pending cases for a period of 20 to 30 Years',
    'Pending cases over 30 Years'
]
age_wise_pending = df[age_columns].sum().sort_values()
plt.figure(figsize=(10, 6))
sns.barplot(x=age_wise_pending.values, y=age_wise_pending.index, palette='coolwarm')
plt.title("Pending Cases by Age Group")
plt.xlabel("Number of Cases")
plt.tight_layout()
plt.show()

# 4. Pie Chart - Case type distribution
case_types = ['Pending Appeal cases', 'Pending Application cases', 'Pending Execution cases']
case_counts = df[case_types].sum()
plt.figure(figsize=(8, 8))
plt.pie(case_counts, labels=case_types, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
plt.title("Case Type Distribution")
plt.tight_layout()
plt.show()

# 5. Histogram - Monthly case movement
plt.figure(figsize=(10, 6))
sns.histplot(df[['Cases instituted in last month', 'Cases disposed in last month']], kde=True, element="step", palette='Set2')
plt.title("Cases Instituted vs Disposed in a Month")
plt.xlabel("Number of Cases")
plt.tight_layout()
plt.show()

# 6. Box Plot - Special category cases (Women & Seniors)
plt.figure(figsize=(10, 6))
sns.boxplot(data=df[['Cases filed by Senior Citizens', 'Cases filed by women']], palette='pastel')
plt.title("Distribution of Cases Filed by Women and Senior Citizens")
plt.tight_layout()
plt.show()

# 7. Scatter Plot - Delayed vs Total Pending
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='Cases delayed in disposal', y='Pending cases', color='teal')
plt.title("Cases Delayed vs Total Pending Cases")
plt.xlabel("Delayed Disposals")
plt.ylabel("Pending Cases")
plt.tight_layout()
plt.show()

# 8. Heatmap - State vs Year
heatmap_data = df.groupby(['srcStateName', 'srcYear'])['Pending cases'].sum().unstack(fill_value=0)
plt.figure(figsize=(14, 10))
sns.heatmap(
    heatmap_data,
    cmap='YlOrRd',
    linewidths=0.5,
    linecolor='gray',
    annot=True,
    fmt=".0f",
    cbar_kws={'label': 'Pending Cases'}
)
plt.title("Pending Cases Heatmap by State and Year")
plt.xlabel("Year")
plt.ylabel("State")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 9. Bar Chart - Pending cases by case stage
stage_columns = [
    'Cases pending at Appearance or Service-Related stage',
    'Cases pending at Compliance or Steps or stay stage',
    'Cases pending at Evidence or Argument or Judgement stage',
    'Cases pending at Pleadings or Issues or Charge stage'
]
stages_total = df[stage_columns].sum()
plt.figure(figsize=(10, 6))
plt.bar(stages_total.index, stages_total.values, color=sns.color_palette("Set2"))
plt.title("Pending Cases by Stage")
plt.xticks(rotation=45, ha='right')
plt.ylabel("Number of Cases")
plt.tight_layout()
plt.show()