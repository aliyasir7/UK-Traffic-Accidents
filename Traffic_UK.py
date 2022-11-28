## Traffic Accidents UK ##
PROJE = "Traffic Accidents UK"

""" 1- Importing Libraries and Packages """
import numpy as np
import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt
import warnings
import functions as f
import statistics as st

# Packages settings and directory settings
sns.set_style("whitegrid")
warnings.filterwarnings("ignore")
os.getcwd()
path="C:\\Users\\hseym\\OneDrive\\Masaüstü\\Yeni klasör\\sample data and codes\\traffic_accident_UK"
os.chdir(path)
f.display()

""" 2- Loading and Viewing Data Set """
data_1 = pd.read_csv("accidents_2005_to_2007.csv", parse_dates = ["Date"])
data_2 = pd.read_csv("accidents_2009_to_2011.csv", parse_dates = ["Date"])
data_3 = pd.read_csv("accidents_2012_to_2014.csv", parse_dates = ["Date"])

print(data_1.columns.equals(data_2.columns))
print(data_1.columns.equals(data_3.columns))
data = pd.concat([data_1,data_2,data_3], ignore_index = True)
del data_1, data_2, data_3
traffic = pd.read_csv("ukTrafficAADF.csv")
traffic.head()
data.head()
data = data.sort_values("Date").reset_index(drop=True)
""" 3- Dealing with NaN Values (Imputation)"""
def null_table(data):
    print("Data Frame")
    print(pd.DataFrame(data.isnull().sum()).T)
null_table(data)

# Time
copy = data.copy()
hour_min = copy[copy["Time"].notna()].Time.apply(lambda x: str(x).split(":"))
minute = [int(i[0])*60+int(i[1]) for i in hour_min]
median_min = st.median(minute)
mean_min = st.mean(minute)
plt.hist(minute)
median_str = str(median_min//60)+":"+str(median_min%60)
data["Time"].fillna(median_str, inplace = True)

#Carriageway_Hazards
print(copy[copy["Carriageway_Hazards"]=="None"])
print(copy[copy["Carriageway_Hazards"].isna()])
data.drop(columns="Carriageway_Hazards", inplace = True)

#Junction_Detail, LSOA_of_Accident_Location, Did_Police_Officer_Attend_Scene_of_Accident, Junction_Control
data.drop(columns = "Junction_Detail", inplace = True)
data.drop(columns = "LSOA_of_Accident_Location", inplace = True)
data.drop(columns = "Did_Police_Officer_Attend_Scene_of_Accident", inplace = True)
data.drop(columns = "Junction_Control", inplace = True)
data.drop(columns = "Accident_Index", inplace = True)
#Location_Easting_OSGR
data = data[data["Location_Easting_OSGR"].notna()].reset_index(drop = True)
# Pedestrian_Crossing-Physical_Facilities
unique_pedes = copy["Pedestrian_Crossing-Physical_Facilities"].unique()
copy["Pedestrian_Crossing-Physical_Facilities"].isnull().sum()
for i in unique_pedes:
    print(i)
    print(len(copy[copy["Pedestrian_Crossing-Physical_Facilities"]==i]))
data["Pedestrian_Crossing-Physical_Facilities"].fillna("No physical crossing within 50 meters", inplace = True)

#Pedestrian_Crossing-Human_Control
unique_pedes_human = copy["Pedestrian_Crossing-Human_Control"].unique()
for i in unique_pedes_human:
    print(i)
    print(len(copy[copy["Pedestrian_Crossing-Human_Control"]==i]))
data["Pedestrian_Crossing-Human_Control"].fillna("None within 50 metres", inplace = True)

#Special_Conditions_at_Site
copy["Special_Conditions_at_Site"].unique()
print(copy[copy["Special_Conditions_at_Site"]=="None"])
data.drop(columns = "Special_Conditions_at_Site", inplace = True)

#Weather_Conditions
wea_cond = copy["Weather_Conditions"].unique()
for i in wea_cond:
    print(i)
    print(len(copy[copy["Weather_Conditions"]==i]))
data["Weather_Conditions"].fillna("Fine without high winds", inplace = True)

#Road_Surface_Conditions
road_cond = copy["Road_Surface_Conditions"].unique()
for i in road_cond:
    print(i)
    print(len(copy[copy["Road_Surface_Conditions"]==i]))
print(copy[(copy["Road_Surface_Conditions"].isna()) & (copy["Weather_Conditions"]=="Unknown")])
data["Road_Surface_Conditions"].fillna("Dry", inplace = True)

null_table(data)
del copy,hour_min,mean_min, median_min,median_str,minute, unique_pedes

""" 4- Featuring """
#index
data["Index"]=data.index
#Time
data["Year"] = data["Date"].dt.year
data["Month"] = data["Date"].dt.month
data["Day"] = data["Date"].dt.day
data["Time"] = pd.to_datetime(data["Time"], format = "%H:%M")
data["Hour"]  = data["Time"].dt.hour
weekday = pd.DataFrame ({"Day_of_Week":[1,2,3,4,5,6,7], "Day_Name":["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]})
data = pd.merge(data,weekday, how = "left", on = "Day_of_Week")

#Number_of_Casualties
data['Number_of_Casualties'].unique()
data["Number_of_Casualties"].median()
data["Number_of_Casualties"].mean()
def group_casualty(x):
    if (x >= 5):
        return '5+'
    else:
        return x
data['Casualties'] = data['Number_of_Casualties'].apply(group_casualty)
data['Casualties'].unique()

#Number_of_Vehicles
data['Number_of_Vehicles'].unique()
data["Number_of_Vehicles"].median()
data["Number_of_Vehicles"].mean()
def group_vehicles(x):
    if (x >= 5):
        return '5+'
    else:
        return x
data['Vehicles'] = data['Number_of_Vehicles'].apply(group_vehicles)
data['Vehicles'].unique()


""" 5- Visulation """
sns.barplot(x=data.Year.value_counts().index,y=data.Year.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Accidents over the years")

print("Mean:{:.2f}   Standard Deviation:{:.2f}".format(data.Year.value_counts().mean(),
                                                      data.Year.value_counts().std()))

sns.barplot(x=data.Month.value_counts().index,y=data.Month.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Accidents over the Months")

print("Mean:{:.2f}   Standard Deviation:{:.2f}".format(data.Month.value_counts().mean(),
                                                      data.Month.value_counts().std()))

sns.barplot(x=data.Day.value_counts().index,y=data.Day.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Accidents over the Days")

print("Mean:{:.2f}   Standard Deviation:{:.2f}".format(data.Day.value_counts().mean(),
                                                      data.Day.value_counts().std()))

sns.barplot(x=data.Day_Name.value_counts().index,y=data.Day_Name.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Accidents over the Day_Names")

print("Mean:{:.2f}   Standard Deviation:{:.2f}".format(data.Day_Name.value_counts().mean(),
                                                      data.Day_Name.value_counts().std()))

sns.barplot(x=data.Hour.value_counts().index,
            y=data.Hour.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Accidents over the hour")
most_accident_hours= data.groupby("Hour")["Date"].count().reset_index().sort_values(by = "Date",ascending = False).reset_index(drop = True).head(5)
print(most_accident_hours)
print("Mean:{:.2f}   Standard Deviation:{:.2f}".format(data.Hour.value_counts().mean(),
                                                      data.Hour.value_counts().std()))

pt_month_year = data.pivot_table(index='Month', columns = 'Year', values = 'Date', aggfunc = 'count')
pt_month_year
pt_month_year.plot(xticks=[1,2,3,4,5,6,7,8,9,10,11,12])
plt.title('Accidents by Month and Year')
plt.xlabel('Month')
plt.ylabel('Number of Accidents')

sns.barplot(x=data.Casualties.value_counts().index,
            y=data.Casualties.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Casualties Groups")

sns.barplot(x=data.Vehicles.value_counts().index,
            y=data.Vehicles.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Vehicles Groups")

data.groupby('Accident_Severity').size().plot( kind = 'pie', autopct='%1.0f%%')
plt.title('Accidents Severity')
plt.ylabel('Number of Accidents')

cmap = plt.get_cmap("tab20c")
colors = cmap(np.array([1, 2, 5, 6, 9,15]))
plt.pie(data["Accident_Severity"].value_counts(),labels = ["Slight","Serious","Fatal"],autopct='%1.2f%%',colors=colors)
plt.title("Accidents Severity")

data.groupby('Light_Conditions').size().plot(kind = 'pie', autopct='%1.0f%%')
plt.title('Light Conditions')
plt.ylabel('Number of Accidents')

sns.barplot(x=data.Weather_Conditions.value_counts().index,y=data.Weather_Conditions.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Weather_Conditions")
plt.tick_params(labelrotation=20)
data.Weather_Conditions.value_counts()

sns.barplot(x=data.Road_Surface_Conditions.value_counts().index,y=data.Road_Surface_Conditions.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Road_Surface_Conditions")
plt.tick_params(labelrotation=20)
data.Road_Surface_Conditions.value_counts()

sns.barplot(x=data.Road_Type.value_counts().index,y=data.Road_Type.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Road_Type")
plt.tick_params(labelrotation=20)
data.Road_Type.value_counts()

cmap = plt.get_cmap("tab20c")
colors = cmap(np.array([1,9,15]))
plt.pie(data["Urban_or_Rural_Area"].value_counts(),labels = ["Urban","Rural","Unallocated"],autopct='%1.2f%%',colors=colors)
plt.title("Urban_or_Rural_Area")
data.Urban_or_Rural_Area.value_counts()

data.groupby('Pedestrian_Crossing-Physical_Facilities').size().plot(kind = 'pie', autopct='%1.0f%%')
plt.title('Pedestrian_Crossing-Physical_Facilities')
plt.ylabel('Number of Accidents')

data.groupby('Pedestrian_Crossing-Human_Control').size().plot(kind = "bar")
plt.title('Pedestrian_Crossing-Human_Control')
plt.ylabel('Number of Accidents')

sns.barplot(x=data.Speed_limit.value_counts().index,y=data.Speed_limit.value_counts())
plt.ylabel("Num. of Accidents")
plt.title("Speed_limit")
cmap = plt.get_cmap("tab20c")
colors = cmap(np.array([1,4,9,12,15,18,21,24,27,30]))
plt.pie(data["Speed_limit"].value_counts(),labels = data["Speed_limit"].value_counts().index,autopct='%1.2f%%',colors=colors)
plt.title("Speed_limit")
data.Speed_limit.value_counts()

highway_count = data.groupby(["Local_Authority_(Highway)"])["Date"].count().reset_index().sort_values(by=["Date"], ascending = False).reset_index(drop = True)
top_20_dangerous_highway = highway_count.head(20)
sns.barplot(x=top_20_dangerous_highway["Local_Authority_(Highway)"],y=top_20_dangerous_highway.Date)
plt.ylabel("Num. of Accidents")
plt.title("top_20_dangerous_highway")
plt.tick_params(labelrotation=20)

district_count = data.groupby(["Local_Authority_(District)"])["Date"].count().reset_index().sort_values(by=["Date"], ascending = False).reset_index(drop = True)
top_20_dangerous_district = district_count.head(20)
sns.barplot(x=top_20_dangerous_district["Local_Authority_(District)"],y=top_20_dangerous_district.Date)
plt.ylabel("Num. of Accidents")
plt.title("top_20_dangerous_district")
plt.tick_params(labelrotation=20)

location_math = data.groupby(["Longitude",  "Latitude"])["Date"].count().reset_index().sort_values(by = "Date", ascending = False).reset_index(drop = True)
dangerous_locations_math = location_math.head(20)
sns.relplot(data=dangerous_locations_math,x="Longitude",y="Latitude", color="orange")
fig, axes = plt.subplots(figsize=(6, 10))
plt.axes().set_facecolor("black")
plt.scatter(x = data["Longitude"], y = data["Latitude"],s=0.005, alpha= 0.25, color="lightyellow")
plt.scatter(x = dangerous_locations_math["Longitude"], y = dangerous_locations_math["Latitude"],s=5, alpha= 0.25, color="red")
plt.title("UK Accidents Dangerous Points")
ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)


