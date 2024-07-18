import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
from scipy.interpolate import interp1d

data = pd.read_excel("C:/Users/arnav/Downloads/USA GDP Growth 1961-2021.xlsx")

year = data["Year"]
gdp = data["GDP"]
growth = data["Growth"]
gdp_capita = data["GDP per Capita"]

def clean_gdp_str(gdp_str):
    cleaned_gdp = []

    for gdp_str in gdp:
        new_gdp_str = re.sub(r"[\$B,]", "", gdp_str)
        cleaned_gdp.append(float(new_gdp_str))

    return(cleaned_gdp)

cleaned_gdp = clean_gdp_str(gdp)

def custom_floor(value, base):
    return(base * (value // base))

def custom_ceil(value, base):
    return(base * ((value + base - 1) // base))

plt.figure(1)
plt.plot(year, cleaned_gdp)
plt.title("USA GDP Growth from 1961 to 2021")
plt.xlim(year.min() - 10, year.max() + 10)
plt.xticks(range(year.min(), year.max() + 1, 10))
y_min = int(custom_floor(min(cleaned_gdp), 100))
y_max = int(custom_ceil(max(cleaned_gdp), 100))
plt.ylim(y_min, y_max)
plt.yticks(range(y_min, y_max + 1, 1500))
plt.xlabel("Year")
plt.ylabel("GDP (Billions $)")
plt.grid(True)

def interpolate_data(x, y, num_points):
    interp_func = interp1d(x, y, kind="linear")
    x_new = np.linspace(x.min(), x.max(), num_points)
    y_new = interp_func(x_new)
    
    return(x_new, y_new)

def plot_growth_with_color(year, growth):
    for i in range(len(growth)):
        color = "blue" if growth[i] >= 0 else "red"
        plt.plot(year[i:i+2], growth[i:i+2], color=color)

year_interp, growth_interp = interpolate_data(year, growth, 10)

plt.figure(2)
plot_growth_with_color(year_interp, growth_interp)
plt.title("USA GDP Growth Rate from 1961 to 2021")
plt.xlim(int(min(year_interp)) - 10, int(max(year_interp)) + 10)
plt.xticks(range(int(min(year_interp)), int(max(year_interp)) + 1, 10))
plt.xlabel("Year")
plt.ylabel("Growth Rate (%)")
plt.grid(True)

plt.figure(3)
plt.plot(year, gdp_capita)
plt.title("USA GDP Per Capita from 1961 to 2021")
plt.xlim(int(min(year)) - 10, int(max(year)) + 10)
plt.xticks(range(int(min(year)), int(max(year)) + 1, 10))
plt.xlabel("Year")
plt.ylabel("GDP Per Capita ($)")
plt.grid(True)

plt.show()