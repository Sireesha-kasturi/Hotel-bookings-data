# %% [markdown]
# # Title of the project - Hotel Bookings Data Analysis

# %% [markdown]
# ## Name :Sireesha Kasturi

# %%
# Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%
# load the data
Hotel_bookings = pd.read_csv(
    r"C:\Users\DELL\Desktop\Labmentix\hotel_bookings_data.csv",
    encoding="utf-8"
)
Hotel_bookings

# %%
# How many rows and columns does it have?
Hotel_bookings.shape

# %%
# Cheking for Data types
Hotel_bookings.info()

# %%
# Cheking for the null values
Hotel_bookings.isnull().sum()

# %% [markdown]
# ##### In city, agent and company columns have lots of null values 

# %%
# Lets drop columns with high missing values.
Hotel_bookings = Hotel_bookings.drop(['agent', 'company'], axis=1)
Hotel_bookings

# %%
# Country has 488 rows with the NaN values. 488 rows out of 119390 is negligible hence we will just remove.
Hotel_bookings = Hotel_bookings.dropna(axis = 0)

# %%
Hotel_bookings.isnull().sum()

# %%
# Cheking for the shape after removing columns
Hotel_bookings.shape

# %%
# Statistical Data of the hotel
Hotel_bookings.describe()

# %%
Hotel_bookings.duplicated().sum()

# %%
# Select categorical columns
cat_col = Hotel_bookings.select_dtypes(include=['str'])
cat_col

# %%
# Select numerical columns
num_col = Hotel_bookings.select_dtypes(include=['number'])
num_col

# %%
cat_col['hotel'].value_counts()

# %%

labels = Hotel_bookings['hotel'].value_counts().index.tolist()
sizes = Hotel_bookings['hotel'].value_counts().values
colors = ['yellowgreen', 'lightcoral']
plt.pie(
    sizes,
    labels=labels,
    colors=colors,
    autopct='%1.1f%%',
    startangle=90
)

plt.title('Distribution of Hotel Types')
plt.show()

# %% [markdown]
# #### City hotel count is more than resort hotels.

# %%
#replace TA/TO with Undefined in distribution_channel column
Hotel_bookings['distribution_channel'].replace("TA/TO", "Undefined", inplace = True)

# %% [markdown]
# #### Bookings by different types of hotels

# %%
d = Hotel_bookings.groupby('hotel')['hotel'].count()
sns.barplot(x=d.index, y=d)
plt.xlabel("Hotel Type")
plt.ylabel("No. of bookings")
plt.title("No of Bookings by hotel type")


# %% [markdown]
# ##### City hotel made more bookings

# %%
#Counts of Cancelled vs Not-Cancelled Bookings in different types of hotels

sns.countplot(x='hotel', hue='is_canceled', data=Hotel_bookings)
plt.legend(['Not Cancelled', 'Cancelled'])
plt.xlabel("Hotel Type")
plt.ylabel("count")

# %%
df=Hotel_bookings['arrival_year'].unique()
df

# %%
# Booking by year & type of hotel
sns.countplot(x='arrival_year', hue='hotel', data=Hotel_bookings)
plt.ylabel("No. of bookings")
plt.title("Total bookings by year")

# %%
#No. of bookings by months of year

months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]
plt.figure(figsize=(12, 6))

sns.countplot(
    data=Hotel_bookings, x="arrival_month",hue="hotel",order=months
)

plt.xticks(rotation=30)
plt.xlabel("Months")
plt.ylabel("Number of Bookings")
plt.title("Monthly Bookings by Hotel Type")

plt.tight_layout()
plt.show()

# %%
# Calculate cancellation rate for each hotel type
cancellation_rate = (
    Hotel_bookings.groupby('hotel')['is_canceled']
    .mean() * 100
)

print(cancellation_rate.round(2))

# Visualize cancellation rates
plt.figure(figsize=(3,4))
sns.barplot(
    x=cancellation_rate.index,
    y=cancellation_rate.values
)

plt.xlabel("Hotel Type")
plt.ylabel("Cancellation Rate (%)")
plt.title("Cancellation Rate by Hotel Type")
plt.tight_layout()
plt.show()

# %%
#Daily Rate by Hotel type

Hotel_bookings['adr'].describe()

# %%
plt.figure(figsize=(10,10))
df2 = Hotel_bookings.drop(Hotel_bookings[Hotel_bookings['adr']==5400].index, axis=0)
sns.boxplot(x='hotel', y='adr', data = df2 )
plt.ylabel('Average daily rate')
plt.xlabel("Hotel Type")
plt.title("Daily Rate by hotel type")

# %%
plt.figure(figsize=(9,6))
sns.histplot(x='adr', hue='hotel', data=df2, kde=True)
plt.xlabel("Average daily rate")
plt.title("Daily rate by hotel type")
     

# %%

months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

plt.figure(figsize=(12, 5))

sns.barplot(
    data=Hotel_bookings,
    x='arrival_month',
    y='adr',
    order=months,
    errorbar=None
)

plt.title('Average Daily Rate (ADR) by Month')
plt.xlabel('Month')
plt.ylabel('Average Daily Rate (ADR)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# #### As the observation suggests adr is more in october  and less in march.
# #### So as we observed earlier cancelations and bookigs are also more in october and less in march

# %%

#Price variation over the year
d = df2.groupby(['hotel', 'arrival_month'])['adr'].mean().reset_index()
d['arrival_month'] = pd.Categorical(d['arrival_month'], categories=months, ordered=True)
d.sort_values('arrival_month', inplace=True)
d

# %%
plt.figure(figsize=(9,6))
sns.lineplot(x='arrival_month', y='adr', hue='hotel', data=d)
plt.ylabel("Average daily price")
plt.xlabel("Months")
p = plt.xticks(rotation=30)
plt.title("Average Daily rate by months")

# %% [markdown]
# ##### For Resort Hotel, ADR is more fluctuated and price is high compare with city hotel
# ##### For City Hotel, ADR is in mid with less fluctuations 

# %%
#Bookings by market segment

d = Hotel_bookings['market_segment'].value_counts()
plt.figure(figsize=(5,5))
p = plt.pie(d, labels=d.index, autopct="%.0f%%")
plt.title("Bookings by market segment")

# %%
Hotel_bookings['market_segment'].value_counts()

# %%
#Monthly hotel bookings and cancellations 
months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

plt.figure(figsize=(12, 5))

sns.countplot(
    x='arrival_month',
    hue='is_canceled',
    data=Hotel_bookings,
    order=months
)

plt.title('Monthly Hotel Bookings and Cancellations')
plt.xlabel('Arrival Month')
plt.ylabel('Number of Bookings')
plt.xticks(rotation=45)
plt.legend(title='Is Canceled', labels=['Not Canceled', 'Canceled'])
plt.tight_layout()
plt.show()

# %% [markdown]
# ##### Almost half of bookings was done through Online Travel Agents (TA). 
# ##### More than 90% bookings was done by Online TA, Offline TA/TO, Groups & Direct.

# %%
#Cancellations per months

d = Hotel_bookings.groupby(['hotel','arrival_month']).agg({'is_canceled':'sum', 'meal':'count'}).reset_index().rename(columns={'is_canceled':'cancelled_bookings', 'meal':'total_bookings'})
d['cancellation_percentage'] = (d['cancelled_bookings']/d['total_bookings'])*100
d.head()
     

# %%
d.tail()

# %% [markdown]
# #### october has more cancelations and more bookings also
# #### March has less cancelations and least bookings

# %%
#Effect of Lead time on Cancellations

d = Hotel_bookings.groupby('lead_time').agg({'is_canceled':'sum', 'hotel':'count'}).reset_index().rename(columns={'is_canceled':'cancelled_bookings', 'hotel':'total_bookings'})
d['cancellation_percentage'] = (d['cancelled_bookings']/d['total_bookings'])*100
d.head()
     

# %%
d.tail()

# %%
plt.figure(figsize=(10,5))
sns.scatterplot(x='lead_time', y='cancellation_percentage', data=d)
plt.ylim((0,100))
plt.xlabel("Lead Time (days)")
plt.ylabel("% Cancellation")
plt.title("Effect of Lead time on Cancellations")

# %% [markdown]
# ##### Bookings having less lead time are less often cancelled 
# ##### whereas high lead time bookings are more often cancelled. 

# %%
#Cancellations by type of Guests (Repeated/NonRepeated)

plt.figure(figsize=(8,5))
sns.countplot(x = "is_canceled", hue = 'is_repeated_guest', data = Hotel_bookings)
plt.legend(['New Guest', 'Repeated Guest'])
plt.xticks(ticks=[0,1], labels=['Not Cancelled', 'Cancelled'])
plt.title("Cancellations by repeated guests")

# %% [markdown]
# ##### We observe that repeated guests cancels their bookings less often than new guests.

# %%
# Filter Resort Hotel bookings
resort_bookings = Hotel_bookings[
    Hotel_bookings['hotel'] == 'Resort Hotel'
]

# Calculate cancellation percentage
cancellation_percentage = (
    resort_bookings['is_canceled'].mean() * 100
)

print(f"Resort Hotel Cancellation Rate: {cancellation_percentage:.2f}%")

# %%
# Filter Resort Hotel bookings
resort_bookings = Hotel_bookings[
    Hotel_bookings['hotel'] == 'City Hotel'
]

# Calculate cancellation percentage
cancellation_percentage = (
    resort_bookings['is_canceled'].mean() * 100
)

print(f"City Hotel Cancellation Rate: {cancellation_percentage:.2f}%")

# %%
# Calculate total length of stay
Hotel_bookings['total_stay'] = (
    Hotel_bookings['stays_in_weekend'] +
    Hotel_bookings['stays_in_weekdays']
)

# Calculate cancellation rate by length of stay
stay_cancellation = (
    Hotel_bookings.groupby('total_stay')['is_canceled']
    .mean()
    .mul(100)
    .reset_index(name='cancellation_rate')
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=stay_cancellation,
    x='total_stay',
    y='cancellation_rate',
    marker='o'
)

plt.title('Cancellation Rate by Length of Stay')
plt.xlabel('Total Length of Stay (Nights)')
plt.ylabel('Cancellation Rate (%)')
plt.tight_layout()
plt.show()

# %% [markdown]
# #### Cancelation rates are high during long stay like between 20 to 30 days.

# %%
#Car Parking Space

plt.figure(figsize = (12,8))
sns.countplot(x='required_car_parking_spaces', hue='hotel', data=Hotel_bookings)
plt.xlabel("No. of Car Parking Space Req.")
plt.legend(loc=1)
plt.title("Car Parking Spaces Demand")
     

# %%
d = Hotel_bookings.groupby('required_car_parking_spaces')['hotel'].count().reset_index().rename(columns={'hotel':'total_demand'})
d['demand_percentage'] = (d['total_demand']/sum(d['total_demand']))*100
d
     

# %% [markdown]
# ##### We can see that more than 93% guests don't need parking space and almost 6% guests need parking space for 1 car.

# %%
#repeated guests by hotel
plt.figure(figsize = (6,3))
sns.countplot(x='is_repeated_guest', hue='hotel', data=Hotel_bookings)
plt.xlabel("Repeated guests.")
plt.legend(loc=1)
plt.title("Repeated guests by hotel")


# %%



