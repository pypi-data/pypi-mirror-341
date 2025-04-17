# 📦 Weather Data Client

This package includes a function to fetch and preprocess historical weather data from [Weatherunderground.com](https://www.wunderground.com/).

## Installation
`pip install get-weather-api`

## 📘 Usage

For a single month, the data is correct.
```python
from get_weather.client import get_weather_data
import os
os.environ["API_KEY"] = "API_KEY"

df = get_weather_data(
    weather_station="RJAA",
    country_code="JP",
    startDate="20190201",
    endDate="20190301",
    timezone="US/Pacific"
)
print(df.head())
```

However, for multiple months, you need to split the queries and concatenate it after.
```python
starts = pd.date_range(start='20220101', end='20230301', freq="ME")
ends = pd.date_range(start='20220101', end='20230301', freq="ME")
starts = [s.replace(day=1) for s in starts]
s_e = zip(starts, ends)

df_arr = []
for s, e in s_e:
    s = s.strftime("%Y%m%d")
    e = e.strftime("%Y%m%d")

    df = c.get_weather_data(
        startDate=s,
        endDate=e,
        weather_station="KCHA",
        timezone="US/Eastern",
        country_code="US",
        number=2
    )

    df_arr.append(df)
    
df = pd.concat(df_arr)
```
---

### Parameters
Parameters can be obtained from https://www.wunderground.com/. For a desired location follow these steps.
1. Search locations in the upper right. For example Manila, Philippines.
2. Click the history tab and identify the weather station which would be the last parameter in the URL:
    ```
    https://www.wunderground.com/history/daily/ph/manila/RPLL
    ```
    Here it would be RPLL.
3. The country code would be the third to the last parameter: `PH`
4. Timezone would be what you want the data to be encoded in, for Manila it would be `'Asia/Manila'`
5. Start and end dates must be strings in the form of `YYYYMMDD`. The minimum window should be 1 month. i.e., `20201001` to `20201101`.

Thus the arguments you would use would be:
`df = get_weather_data(weather_station="RPLL", country_code="PH", startDate="20201001", endDate="20201101", timezone="Asia/Manila")`

#### 📊 Weather Feature Descriptions

| Column           | Description |
|------------------|-------------|
| **Time**         | The timestamp of the weather observation, converted from GMT to your specified timezone. This is usually reported in hourly intervals and used as the index for the DataFrame. |
| **tempf**        | Air temperature in degrees Fahrenheit at the time of observation. |
| **dewPt**        | Dew point in degrees Fahrenheit – the temperature at which air becomes saturated and dew can form. Used to assess humidity. |
| **rh**           | Relative Humidity in percentage (%). Indicates how much moisture is in the air compared to the maximum possible at that temperature. |
| **wdir_cardinal**| Wind direction as a cardinal compass point (e.g., "N", "NE", "W"). Reflects the direction from which the wind is blowing. |
| **wspd**         | Wind speed in miles per hour (mph). Average wind speed during the observation window. |
| **gust**         | Wind gust in mph. Peak wind speed recorded during the observation window. May be missing or zero if conditions were calm. |
| **pressure**     | Atmospheric pressure in inches of mercury (inHg). Often used in weather forecasting (e.g., identifying high/low pressure systems). |
| **precip**       | Total precipitation during the hour in inches (rain, snow water equivalent, etc.). May be "0.0" if no measurable precipitation occurred. |
| **wx_phrase**    | Textual weather summary, e.g., "Partly Cloudy", "Rain Showers", "Snow", etc. Useful for quick human-readable interpretation of the weather conditions. |

---


### 🔧 Setup

1. Create a `.env` file with your API key:
    ```bash
    echo "API_KEY=your_actual_api_key_here" > .env
    ```

2. Install the package:
    ```bash
    pip install .
    ```

3. (Optional) Install dev dependencies:
    ```bash
    pip install .[dev]
    ```

---
