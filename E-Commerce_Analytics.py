#!/usr/bin/env python
# coding: utf-8

# # E-commerce Analytics

# ##### 1.Import Libraries
# ##### 2.Reading Data
# ##### 3.Explor Data
# ##### 4.Data Cleaning
# ##### 5.Exploratory Data Analysis (EDA)
# ##### 6.create Dashboard
# ##### 7.Exporting Data to SQL Database

# ## 1. Import Libraries

# In[5]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
plt.style.use("seaborn-v0_8")


# ## 2. Reading Data

# In[8]:


customers= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\customers.csv")
Orders= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\Orders.csv")
items= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\order_items.csv")
products= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\products.csv")
payments= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\order_payments_dataset.csv")
sellers= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\sellers.csv")
reviews= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\order_reviews.csv")
geo= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\geolocation.csv")
translation= pd.read_csv(r"E:\مبادرة رواد مصر الرقمية\راوند 4\مشروع التخرج\product_category_name_translation.csv")


# ## 3.Explor Data

# In[33]:


dfs = {
    "customers": customers,
    "Orders": Orders,
    "items": items,
    "products": products,
    "payments": payments,
    "sellers": sellers,
    "reviews": reviews,
    "geo": geo,
    "translation": translation
}

def explore_data(df, name="DataFrame"):
    print(f"--- Overview of {name} ---\n")
    print("Shape:", df.shape, "\n")
    print("Sample 5 rows:\n", df.sample(5), "\n")
    print("Columns:", df.columns.tolist(), "\n")
    print("Unique values per column:\n", df.nunique(), "\n")
    print("Info:\n")
    print(df.info(), "\n")
    print("Missing values per column:\n", df.isnull().sum(), "\n")
    print("Duplicate rows:", df.duplicated().sum(), "\n")
    print("-"*50, "\n")

for name, df in dfs.items():
    explore_data(df, name)


#  ## 4. Data Cleaning

# ####  Ordersتغيير نوع البيانات فى اعمدة تواريخ  جدول   

# In[47]:


date_columns=['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date']
for col in date_columns:
    Orders[col]=pd.to_datetime(Orders[col])


# In[56]:


Orders[date_columns]=Orders[date_columns].fillna(pd.NaT)
print(Orders[date_columns].info())


# In[58]:


Orders['month'] = Orders['order_purchase_timestamp'].dt.to_period('M')
Orders['day_name'] = Orders['order_purchase_timestamp'].dt.day_name()


# #### items تغيير نوع البيانات فى عمود التاريخ فى 

# In[61]:


items['shipping_limit_date']=pd.to_datetime(items['shipping_limit_date'])
items.info()


# #### reviewsتغيير نوع البيانات فى عمود التاريخ فى جدول

# In[64]:


reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_answer_timestamp'])
reviews.info()


# #### دمج الجداول

# In[67]:


df = Orders.merge(customers,on='customer_id')
df = df.merge(items,on='order_id')
df = df.merge(products,on='product_id')
df = df.merge(payments,on='order_id')
df = df.merge(reviews,on='order_id', how='left')
df.head()


# ## 5.Exploratory Data Analysis (EDA)

# ##### Q1. How many total orders do we have?
# ##### Q2: What is the distribution of order status?
# ##### Q3: How do orders change over time?
# ##### Q4: What time of day do customers place orders?
# ##### Q5: How does revenue change over time?
# ##### Q6: Which states have the highest number of customers?
# ##### Q7: Which cities have most customers?
# ##### Q8: What is the Total Revenue, Freight, and Total Payments?
# ##### Q9: Is there a relationship between product price and freight cost?
# ##### Q10: Which product categories generate highest revenue?
# ##### Q11: How are review scores distributed?
# ##### Q12: What is the average review score?
# ##### Q13: Which states have the most sellers?
# ##### Q14: Which payment methods generate the highest revenue?
# or
# ##### What is the revenue distribution by payment type?

# ## Orders Analysis

# ### Q1. How many total orders do we have?

# In[78]:


total_orders = Orders['order_id'].nunique()
print("total orders:",total_orders)


# ### Q2: What is the distribution of order status?

# In[81]:


order_status = Orders['order_status'].value_counts()
order_status


# In[91]:


ax=sns.countplot(x=Orders['order_status'],palette='plasma')
for i in ax.containers:
    ax.bar_label(i,)
plt.title("Orders Status Distribution")
plt.show()


# ### Q3: How do orders change over time?

# In[112]:


Orders['year'] = Orders['order_purchase_timestamp'].dt.to_period('y')
yearly_orders = Orders.groupby('year').size()

ax=sns.barplot(x=yearly_orders.index.astype(str), y=yearly_orders.values, palette='plasma')
for i in ax.containers:
    ax.bar_label(i,)
plt.title("orders over years")
plt.xlabel("year")
plt.ylabel("number of orders")
plt.show()


# In[114]:


Orders['month'] = Orders['order_purchase_timestamp'].dt.to_period('M')
Orders.groupby('month').size().plot()
plt.title("Orders Over Time")
plt.show()


# ### Orders by Day of Week

# In[117]:


orders_day = Orders.groupby('day_name')['order_id'].count()
orders_day


# In[119]:


ax=sns.barplot(x=orders_day.index,y=orders_day.values,palette='plasma')
for i in ax.containers:
    ax.bar_label(i,)

plt.title("Orders by Day")
plt.show()


# ### Q4: What time of day do customers place orders?

# In[126]:


df['hour'] = df['order_purchase_timestamp'].dt.hour

orders_hour = df.groupby('hour')['order_id'].count().reset_index()


# In[130]:


plt.figure(figsize=(10, 5))

ax=sns.barplot(data=orders_hour, x='hour',y='order_id',palette='plasma')
for i in ax.containers:
    ax.bar_label(i,)
plt.title("Orders by Hour")
plt.show()


# ### Q5: How does revenue change over time?

# In[133]:


monthly_sales = df.groupby('month')['payment_value'].sum().reset_index()

monthly_sales['month'] = monthly_sales['month'].dt.to_timestamp()

sns.lineplot(data=monthly_sales,x='month', y='payment_value')

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()


# ## Customers Analysis

# ### Q6: Which states have the highest number of customers?

# In[139]:


customers_state = customers.groupby('customer_state')['customer_id'].count().sort_values(ascending=False)[:10]

customers_state


# In[141]:


ax=sns.barplot(x=customers_state.index, y=customers_state.values, palette='plasma')

plt.title('Top 10 States by Number of Customers')
plt.xlabel('State')
plt.ylabel('Number of Customers')

for i in ax.containers:
    ax.bar_label(i,)

plt.show()


# ### Q7: Which cities have most customers?

# In[144]:


top_cities = customers.groupby('customer_city')['customer_id'].count().sort_values(ascending=False)[:10]

top_cities


# In[150]:


ax = sns.barplot(x=top_cities.index, y=top_cities.values, palette='plasma')

plt.title("Top 10 Cities by customers ")
plt.xticks(rotation=45)

for i in ax.containers:
    ax.bar_label(i, padding=3)
plt.show()


# ##  Sales,freight, and payments Analysis

# ###  Q8: What is the Total Revenue, Freight, and Total Payments?

# In[170]:


total_revenue = items['price'].sum().round()
print("total revenue:",total_revenue)


# In[172]:


payments_total = payments['payment_value'].sum().round()
print("total payments:",payments_total)


# In[174]:


freight_total = items['freight_value'].sum().round()
print("total freigt:",freight_total)


# In[176]:


avg_order_value = (total_revenue / total_orders).round(1)
print("avg order value:",avg_order_value)


# ### Q9: Is there a relationship between product price and freight cost?

# In[179]:


price_freight = items[['price','freight_value']]

sns.scatterplot(data=items,x='price',y='freight_value')
plt.title("Price vs Freight")
plt.show()
items[['price','freight_value']].corr()


# ## Products Analysis

# ### Q10: Which product categories generate highest revenue?

# In[183]:


df = df.merge(translation, on='product_category_name', how='left')

category_sales = df.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False)[:10].reset_index()
category_sales


# In[185]:


ax=sns.barplot(data=category_sales,x='price',y='product_category_name_english',palette="plasma")
for i in ax.containers:
    ax.bar_label(i,)
plt.title("Top Product Categories")
plt.show()


# ## Reviews Analysis

# ### Q11: How are review scores distributed?

# In[192]:


review_scores = reviews.groupby('review_score')['review_id'].count().sort_values(ascending=False)[:10].reset_index()
review_scores


# In[194]:


ax = sns.barplot(x='review_score', y='review_id',data=review_scores, palette="plasma")
for i in ax.containers:
    ax.bar_label(i,)
plt.title("Review Score Distribution")
plt.show()


# ### Q12: What is the average review score?

# In[197]:


avg_review = reviews['review_score'].mean().round(2)

print("average review score:",avg_review)


# ## Sellers Analysis

# ### Q13: Which states have the most sellers?

# In[201]:


seller_state = sellers.groupby('seller_state')['seller_id'].count().sort_values(ascending=False)[:10].reset_index()
seller_state


# In[203]:


ax=sns.barplot(data=seller_state,x='seller_state',y='seller_id' ,palette="plasma")
for i in ax.containers:
    ax.bar_label(i,)
plt.title("Top Seller States")

plt.show()


# ## Revenue per Order

# In[206]:


revenue_order = df.groupby('order_id')['price'].sum().sort_values(ascending=False)[:10]
revenue_order


# ## Price vs Review Score

# In[209]:


price_review = df[['price','review_score']]
sns.scatterplot(data=df,x='price',y='review_score')

plt.title("Price vs Review Score")

plt.show()


# ### Q14: Which payment methods generate the highest revenue?
# or
# ### What is the revenue distribution by payment type?

# In[212]:


payment_revenue = df.groupby('payment_type')['payment_value'].sum().sort_values(ascending=False).reset_index()
payment_revenue


# In[214]:


ax=sns.barplot(data=payment_revenue, x='payment_type', y='payment_value',palette="plasma")
for i in ax.containers:
    ax.bar_label(i,)
plt.title("Revenue by Payment Type")
plt.xlabel("Payment Type")
plt.ylabel("Total Revenue")

plt.show()


# In[216]:


colors = sns.color_palette("plasma", len(payment_revenue))
plt.pie(payment_revenue['payment_value'], labels=payment_revenue['payment_type'], autopct='%1.1f%%', colors=colors)

plt.title("Revenue by Payment Type")
plt.show()


# ## 6.create Dashboard

# In[219]:


fig, axes = plt.subplots(6, 3, figsize=(24, 36))
fig.suptitle('E-commerce Dashboard', fontsize=32, fontweight='bold', y=1.02)

# ===== الصف الأول: KPI Cards =====
axes[0,0].axis('off')
axes[0,0].text(0.5,0.5,f"${total_revenue:,.0f}", ha='center', fontsize=22, fontweight='bold')
axes[0,0].text(0.5,0.3,"Total Sales", ha='center', fontsize=18)

axes[0,1].axis('off')
axes[0,1].text(0.5,0.5,f"{total_orders:,}", ha='center', fontsize=22, fontweight='bold')
axes[0,1].text(0.5,0.3,"Total Orders", ha='center', fontsize=18)

axes[0,2].axis('off')
axes[0,2].text(0.5,0.5,f"${avg_order_value:,.2f}", ha='center', fontsize=22, fontweight='bold')
axes[0,2].text(0.5,0.3,"Avg Order Value", ha='center', fontsize=18)

# ===== الصف الثاني: Orders Analysis =====
sns.countplot(ax=axes[1,0], x=Orders['order_status'], palette='plasma')
for i in axes[1,0].containers:
    axes[1,0].bar_label(i,)
axes[1,0].set_title("Orders Status Distribution")

sns.barplot(ax=axes[1,1], x=yearly_orders.index.astype(str), y=yearly_orders.values, palette='plasma')
for i in axes[1,1].containers:
    axes[1,1].bar_label(i,)
axes[1,1].set_title("Orders Over Years")

Orders.groupby('month').size().plot(ax=axes[1,2])
axes[1,2].set_title("Orders Over Time")

# ===== الصف الثالث: Day & Hour Analysis =====
ax = sns.barplot(ax=axes[2,0], x=orders_day.index, y=orders_day.values, palette='plasma')
for i in ax.containers:
    ax.bar_label(i,)
axes[2,0].set_title("Orders by Day")

ax = sns.barplot(ax=axes[2,1], data=orders_hour, x='hour', y='order_id', palette='plasma')
for i in ax.containers:
    ax.bar_label(i,)
axes[2,1].set_title("Orders by Hour")

sns.lineplot(ax=axes[2,2], data=monthly_sales, x='month', y='payment_value')
axes[2,2].set_title("Monthly Revenue")

# ===== الصف الرابع: Customers Analysis =====
ax = sns.barplot(ax=axes[3,0], x=customers_state.index, y=customers_state.values, palette='plasma')
for i in ax.containers:
    ax.bar_label(i,)
axes[3,0].set_title("Top 10 States by Customers")

ax = sns.barplot(ax=axes[3,1], x=top_cities.index, y=top_cities.values, palette='plasma')
for i in ax.containers:
    ax.bar_label(i, padding=3)
axes[3,1].set_title("Top 10 Cities by Customers")
axes[3,1].tick_params(axis='x', rotation=45)

sns.scatterplot(ax=axes[3,2], data=items, x='price', y='freight_value')
axes[3,2].set_title("Price vs Freight")

# ===== الصف الخامس: Products & Reviews & Sellers =====
ax = sns.barplot(ax=axes[4,0], data=category_sales, x='price', y='product_category_name_english', palette="plasma")
for i in ax.containers:
    ax.bar_label(i,)
axes[4,0].set_title("Top Product Categories")

ax = sns.barplot(ax=axes[4,1], x='review_score', y='review_id', data=review_scores, palette="plasma")
for i in ax.containers:
    ax.bar_label(i,)
axes[4,1].set_title("Review Score Distribution")

ax = sns.barplot(ax=axes[4,2], data=seller_state, x='seller_state', y='seller_id', palette="plasma")
for i in ax.containers:
    ax.bar_label(i,)
axes[4,2].set_title("Top Seller States")

# ===== الصف السادس: Payments =====
ax = sns.barplot(ax=axes[5,0], data=payment_revenue, x='payment_type', y='payment_value', palette="plasma")
for i in ax.containers:
    ax.bar_label(i,)
axes[5,0].set_title("Revenue by Payment Type")

colors = sns.color_palette("plasma", len(payment_revenue))
axes[5,1].pie(payment_revenue['payment_value'], labels=payment_revenue['payment_type'], autopct='%1.1f%%', colors=colors)
axes[5,1].set_title("Revenue by Payment Type (Pie)")

axes[5,2].axis('off')  # آخر خلية نتركها فارغة

plt.tight_layout()
plt.show()


# ## 7.Exporting Data to SQL Database

# In[222]:


from sqlalchemy import create_engine


SERVER_NAME   = "BUSINESS_PLUS"
DATABASE_NAME = "E-commerce_Analytics"

connection_string = (
    f"mssql+pyodbc://{SERVER_NAME}/{DATABASE_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)
engine = create_engine(connection_string)
print("✅ تم الاتصال بـ SQL Server بنجاح!")


for col in Orders.columns:
    if str(Orders[col].dtype).startswith("period"):
        Orders[col] = Orders[col].astype(str)
        print(f" تم تحويل عمود '{col}' من Period إلى String")


tables = {
    "customers"   : customers,
    "Orders"      : Orders,
    "items"       : items,
    "products"    : products,
    "payments"    : payments,
    "sellers"     : sellers,
    "reviews"     : reviews,
    "geo"         : geo,
    "translation" : translation,
}

for table_name, df in tables.items():
    print(f" بيرفع جدول: {table_name} ...")

    df.to_sql(
        name      = table_name,
        con       = engine,
        if_exists = "replace",
        index     = False,
    )

    print(f"✅ {table_name} → تم رفع {len(df)} صف!")

print("\n كل الجداول التسعة اتنقلت لـ SQL Server بنجاح!")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




