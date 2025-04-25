import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on April 24th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

#Step 1: Add a dropdown for Category selection**
categories = df["Category"].unique()  # Get unique categories
selected_category = st.selectbox(
    "Select a Category",  
    options=categories,  
    index=0  # Default selection (first item)
)

st.write(f"You selected: {selected_category}")  # Display selected category


# Filter data based on the selected category
df_filtered = df[df["Category"] == selected_category]

# Step 2: Select Sub-Categories (Multiselect)
sub_categories = df_filtered["Sub_Category"].unique()
selected_sub_categories = st.multiselect(
    "Select Sub-Categories",
    options=sub_categories,
    default=sub_categories
)

# Filter based on selected Sub-Categories
df_filtered = df_filtered[df_filtered["Sub_Category"].isin(selected_sub_categories)]


# Step 3: Show a line chart of sales for the selected sub-categories over time
if selected_sub_categories:
    # Filter the data based on selected sub-categories
    filtered_sales = df_filtered[df_filtered["Sub_Category"].isin(selected_sub_categories)]
    
    # Make sure 'Order_Date' is in datetime format
    filtered_sales['Order_Date'] = pd.to_datetime(filtered_sales['Order_Date'])
    
    # Group by 'Order_Date' (monthly) and 'Sub_Category', then sum the 'Sales'
    sales_by_date = filtered_sales.groupby([filtered_sales['Order_Date'].dt.to_period('M'), 'Sub_Category'])['Sales'].sum().unstack('Sub_Category')

    # Ensure we drop rows with missing data (if any)
    sales_by_date = sales_by_date.fillna(0)

    # Display the line chart with sub-categories
    st.write(f"### Sales for Selected Sub-Categories Over Time")
    st.line_chart(sales_by_date)




# **Step 4: Show metrics**
total_sales = df_filtered["Sales"].sum()
total_profit = df_filtered["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales else 0

st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric("Profit Margin (%)", f"{profit_margin:.2f}%")



 # Step 5: Add delta to Profit Margin
overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100 if df["Sales"].sum() else 0
delta = profit_margin - overall_profit_margin

st.metric("Profit Margin (%)", f"{profit_margin:.2f}%", delta=f"{delta:.2f}%")





# Aggregating for solid bar chart
st.dataframe(df_filtered.groupby("Category").sum())
st.bar_chart(df_filtered.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
df_filtered["Order_Date"] = pd.to_datetime(df_filtered["Order_Date"])
df_filtered.set_index('Order_Date', inplace=True)
sales_by_month = df_filtered.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

