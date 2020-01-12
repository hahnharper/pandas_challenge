#!/usr/bin/env python
# coding: utf-8

# In[56]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)


# In[58]:


purchase_data.head()


# In[59]:


#Show columns
purchase_data.columns


# In[60]:


#Count total number of players
players=purchase_data[["SN","Age","Gender"]].drop_duplicates()
#Count row by row
total_players = len(purchase_data["SN"].unique().tolist())
total_players
print(total_players)


# In[61]:


#Purchasing analysis
#Find number of unique items
unique_items = purchase_data["Item ID" ].nunique()

# Find Average Purchase Price
average_purchase_price = purchase_data["Price"].mean()

# Find Total Number of Purchases
total_number_of_purchases = purchase_data["Price"].count()
#total_number_of_purchases
# Find  Total Revenue
total_revenue=purchase_data["Price"].sum()

#Create a Dataframe to display summary
total_analysis={"Number of Unique items":unique_items,"Average Purchase Price":round(average_purchase_price,2),
                "Total Number of Purchases":total_number_of_purchases,"Total Revenue":round(total_revenue,2)}
purchasing_analysis=pd.DataFrame([total_analysis])

purchasing_analysis["Average Purchase Price"]=purchasing_analysis["Average Purchase Price"].map("${:.2f}".format)
purchasing_analysis["Total Revenue"] = purchasing_analysis["Total Revenue"].map("${:.2f}".format)
purchasing_analysis


# In[62]:


#Count amount of male players (go down list and find all occurences of 'male')
#set index to gender
#Convert into a percentage
#Count amount of female players
#Convert to percentage
#Count amount of undiscolosed
#Covert to percentage

gender_data = purchase_data.loc[:,("Gender", "SN")]
gender_data1 = gender_data.groupby("Gender")["SN"].nunique()
gender_data1 = pd.DataFrame(gender_data1)
gender_data1 = gender_data1.rename(columns={"SN":"Number"})

#calculate percents and create new dataframe
gender_totals = gender_data1.loc[:, "Number"]
gender_percent = gender_totals/total_players
gender_columns = {'Total Count': gender_totals, 'Percent of Players': gender_percent}
gendercounts_df = pd.DataFrame(gender_columns)
gendercounts_df.sort_values(by=['Total Count'],inplace = True, ascending = False)
gendercounts_df["Percent of Players"] = gendercounts_df["Percent of Players"].map("{:,.2%}".format)
gendercounts_df


# In[65]:


#Groupby Gender
gender_data_purchase_data = purchase_data.groupby(["Gender"])

#Find purchase counts by gender
gender_data_purchase_data["Purchase ID"].count().head(10)

#Find total purchase value by gender
total_purchase_value= gender_data_purchase_data["Price"].sum()
#total_purchase_value.head()

#format
format_total_purchase_value = total_purchase_value.map("${:,.2f}".format)

#Find average purchase price by gender
average_purchase_price = gender_data_purchase_data["Price"].mean()
#average_purchase_price.head()

format_average_purchase_price = average_purchase_price.map("${:.2f}".format)
#format_average_purchase_price.head()

# Find normalized totals, total purchases value by purchase count by gender
normalized_totals = total_purchase_value/gender_data_purchase_data["Purchase ID"].count()
format_normalized_totals = normalized_totals.map("${:,.2f}".format)
#format_normalized_totals.head()

#Organize data 
total_gender_purchased_data = pd.DataFrame(gender_data_purchase_data["Purchase ID"].count())
total_gender_purchased_data["Average Purchase Price"] = format_average_purchase_price
total_gender_purchased_data["Total Purchase Value"] = format_total_purchase_value
total_gender_purchased_data["Normalized Totals"] = format_normalized_totals
#fin_gender_purchased_data

#Summary of Data analysis DF grouped by Gender, rename "Purchase ID" column to "Purchase Count" with the .rename(columns={}) 
gender_summary = total_gender_purchased_data.rename(columns={"Purchase ID":"Purchase Count"})
gender_summary


# In[66]:


players.head()


# In[67]:


#Age demographics
players=purchase_data[["SN","Age","Gender"]].drop_duplicates()

#Count row by row
total_players = len(purchase_data["SN"].unique().tolist())
total_players

age_demographics = players.loc[:,("Age","SN")]
age_demographics_totals = age_demographics.sort_values("Age")
age_bins = [0,9.90,14.90,19.90,24.90,29.90,34.90,39.90,99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

#Create age bins
age_demographics_totals["Age Ranges"] = pd.cut(age_demographics["Age"], age_bins, labels=group_names)

#Calculate Age Group numbers
age_demographics_totals = age_demographics_totals["Age Ranges"].value_counts()
age_demographics_percents = age_demographics_totals / total_players
age_demographics = pd.DataFrame({"Total Count": age_demographics_totals, "Percentage of Players":age_demographics_percents})

#Format
age_demographics["Percentage of Players"] = age_demographics["Percentage of Players"].map("{:,.2%}".format)

age_demographics = age_demographics.sort_index()
age_demographics


# In[69]:


#Purchasing analysis
# Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below

purchase_data["Age Ranges"] = pd.cut(purchase_data["Age"], age_bins, labels=group_names)
average_purchase_total= purchase_data.groupby(["Age Ranges"]).sum()["Price"].rename("Total Purchase Value")
age_average=purchase_data.groupby(["Age Ranges"]).mean()["Price"].rename("Average Purchase Price")
age_counts=purchase_data.groupby(["Age Ranges"]).count()["Price"].rename("Purchase Count")

#conversion to a DataFrame
normalized_total = average_purchase_total / age_demographics["Total Count"]
#create the index
age_data = pd.DataFrame({"Purchase Count": age_counts, "Average Purchase Price": age_average, "Total Purchase Value": average_purchase_total, "Normalized Totals": normalized_total})

age_data["Average Purchase Price"]= age_data["Average Purchase Price"].map("${:,.2f}".format)
age_data["Total Purchase Value"]= age_data["Total Purchase Value"].map("${:,.2f}".format)
age_data["Purchase Count"]= age_data["Purchase Count"]
age_data["Average Total Purchase per Person"]= age_data["Normalized Totals"].map("${:,.2f}".format)
#create the DataFrame
age_data = age_data.loc[:, ["Purchase Count", "Average Purchase Price", "Total Purchase Value", "Average Total Purchase per Person" ]]

age_data


# In[51]:


#Top spenders
# top 5 spenders in the game by total purchase value, then list (in a table):
#SN
#Purchase Count
#Average Purchase Price
#Total Purchase Value

#Extract item Data
item_data = pd.DataFrame(file_path_df)

#item_data.head()
top_spendors = item_data.groupby("SN")
top_spendors.count()
analysis_per_spendor = pd.DataFrame(top_spendors["Purchase ID"].count())
total_purchase_SN = top_spendors["Price"].sum()
average_purchase_price_SN = top_spendors["Price"].mean()
avg_purchase_price = average_purchase_price_SN.map("${:,.2f}".format)
analysis_per_spendor["Average Purchase Price"] = avg_purchase_price
analysis_per_spendor["Total Purchase Value"] = total_purchase_by_SN
summary_SN_purchase_data = analysis_by_spendor.rename(columns={"Purchase ID": "Purchase Count"})
Top_Spendors = summary_SN_purchase_data.sort_values("Total Purchase Value", ascending=False)
total_purchase = total_purchase_by_SN.map("${:,.2f}".format)
Top_Spendors["Total Purchase Value"] = total_purchase
Top_Spendors.head(5)


# In[52]:


#Most popular items
#extract item data
item_data = file_path_df.loc[:,["Item ID", "Item Name","Price"]]
#perform calculations
tot_item_purchase= item_data.groupby(["Item ID", "Item Name"]).sum()["Price"].rename("Total Purchase Value")
avg_item_purchase= item_data.groupby(["Item ID", "Item Name"]).mean()["Price"]
item_count = item_data.groupby(["Item ID", "Item Name"]).count()["Price"].rename("Purchase Count")
#Create the DataFrame
item_data_df = pd.DataFrame({"Total Purchase Value": tot_item_purchase, "Item Price": avg_item_purchase, "Purchase Count": item_count})
#sort the values
idc_sorted = item_data_df.sort_values("Purchase Count", ascending=False)
#Data Manipulation
idc_sorted["Item Price"]=idc_sorted["Item Price"].map("${:,.2f}".format)
idc_sorted["Purchase Count"]=idc_sorted["Purchase Count"].map("{:,}".format)
idc_sorted["Total Purchase Value"]=idc_sorted["Total Purchase Value"].map("${:,.2f}".format)
item_pop = idc_sorted.loc[:,["Purchase Count", "Item Price", "Total Purchase Value"]]
item_pop.head(5)


# In[54]:


#Most profitable items
item = item_data_df.sort_values("Total Purchase Value", ascending = False)
item["Item Price"]= item["Item Price"].map("${:,.2f}".format)
item["Purchase Count"]= item["Purchase Count"].map("{:,}".format)
item["Total Purchase Value"]= item["Total Purchase Value"].map("${:,.2f}".format)
profit = item.loc[:,["Purchase Count","Item Price","Total Purchase Value" ]]
profit.head()

