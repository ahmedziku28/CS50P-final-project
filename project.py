# this code has been formatted using black
from art import text2art
import requests
from datetime import datetime, timedelta
import sys
from pytz import timezone


# formats time object from python's format to 24-hour, 12-hour easily readable format
def format_time(time_obj, format_24h="%H:%M", format_12h="%I:%M %p"):
    if isinstance(time_obj, str):
        time_obj = datetime.strptime(time_obj, "%Y-%m-%dT%H:%M")

    formatted_24h = time_obj.strftime(format_24h)
    formatted_12h = time_obj.strftime(format_12h)

    return formatted_24h, formatted_12h

# Approximates wind direction from API to cardinal directions for easier orientation
def approximate_wind_direction(degrees):
    if degrees >= 337.5 or degrees < 22.5:
        return "North"
    elif 22.5 <= degrees < 67.5:
        return "North-East"
    elif 67.5 <= degrees < 112.5:
        return "East"
    elif 112.5 <= degrees < 157.5:
        return "South-East"
    elif 157.5 <= degrees < 202.5:
        return "South"
    elif 202.5 <= degrees < 247.5:
        return "South-West"
    elif 247.5 <= degrees < 292.5:
        return "West"
    else:
        return "North-West"


# A dictionary containing the world's top 100 most visited cities in 2019 plus my city. I added this dict so if the user only enters the name of the city without the country in the format "City, Country" the program will still recognize the city for the user's convenience and not give an error
TOP_CITIES = {
    "Alexandria": "Egypt",
    "Hong Kong": "Hong Kong",
    "Bangkok": "Thailand",
    "London": "United Kingdom",
    "Macau": "Macau",
    "Singapore": "Singapore",
    "Paris": "France",
    "Dubai": "United Arab Emirates",
    "New York City": "United States",
    "Kuala Lumpur": "Malaysia",
    "Istanbul": "Turkey",
    "Delhi": "India",
    "Antalya": "Turkey",
    "Shenzhen": "China",
    "Mumbai": "India",
    "Phuket": "Thailand",
    "Rome": "Italy",
    "Tokyo": "Japan",
    "Pattaya": "Thailand",
    "Taipei": "Taiwan",
    "Mecca": "Saudi Arabia",
    "Guangzhou": "China",
    "Prague": "Czech Republic",
    "Medina": "Saudi Arabia",
    "Seoul": "South Korea",
    "Amsterdam": "Netherlands",
    "Agra": "India",
    "Miami": "United States",
    "Osaka": "Japan",
    "Las Vegas": "United States",
    "Shanghai": "China",
    "Ho Chi Minh City": "Vietnam",
    "Denpasar": "Indonesia",
    "Barcelona": "Spain",
    "Los Angeles": "United States",
    "Milan": "Italy",
    "Chennai": "India",
    "Vienna": "Austria",
    "Johor Bahru": "Malaysia",
    "Jaipur": "India",
    "Cancún": "Mexico",
    "Berlin": "Germany",
    "Cairo": "Egypt",
    "Orlando": "United States",
    "Moscow": "Russia",
    "Venice": "Italy",
    "Madrid": "Spain",
    "Ha Long": "Vietnam",
    "Riyadh": "Saudi Arabia",
    "Dublin": "Ireland",
    "Florence": "Italy",
    "Jerusalem": "Israel",
    "Hanoi": "Vietnam",
    "Toronto": "Canada",
    "Johannesburg": "South Africa",
    "Sydney": "Australia",
    "Munich": "Germany",
    "Jakarta": "Indonesia",
    "Beijing": "China",
    "Saint Petersburg": "Russia",
    "Brussels": "Belgium",
    "Budapest": "Hungary",
    "Athens": "Greece",
    "Lisbon": "Portugal",
    "Dammam": "Saudi Arabia",
    "Penang Island": "Malaysia",
    "Heraklion": "Greece",
    "Kyoto": "Japan",
    "Zhuhai": "China",
    "Vancouver": "Canada",
    "Chiang Mai": "Thailand",
    "Copenhagen": "Denmark",
    "San Francisco": "United States",
    "Melbourne": "Australia",
    "Warsaw": "Poland",
    "Marrakesh": "Morocco",
    "Kolkata": "India",
    "Cebu City": "Philippines",
    "Auckland": "New Zealand",
    "Tel Aviv": "Israel",
    "Guilin": "China",
    "Honolulu": "United States",
    "Hurghada": "Egypt",
    "Kraków": "Poland",
    "Muğla": "Turkey",
    "Buenos Aires": "Argentina",
    "Chiba": "Japan",
    "Frankfurt am Main": "Germany",
    "Stockholm": "Sweden",
    "Lima": "Peru",
    "Da Nang": "Vietnam",
    "Batam": "Indonesia",
    "Nice": "France",
    "Fukuoka": "Japan",
    "Abu Dhabi": "United Arab Emirates",
    "Jeju": "South Korea",
    "Porto": "Portugal",
    "Rhodes": "Greece",
    "Rio de Janeiro": "Brazil",
    "Krabi": "Thailand",
    "Bangalore": "India",
    "Mexico City": "Mexico",
    "Punta Cana": "Dominican Republic",
    "São Paulo": "Brazil",
    "Zürich": "Switzerland",
    "Montreal": "Canada",
    "Washington D.C.": "United States",
    "Chicago": "United States",
    "Düsseldorf": "Germany",
    "Boston": "United States",
    "Chengdu": "China",
    "Edinburgh": "United Kingdom",
    "San Jose": "United States",
    "Philadelphia": "United States",
    "Houston": "United States",
    "Hamburg": "Germany",
    "Cape Town": "South Africa",
    "Manila": "Philippines",
    "Bogota": "Colombia",
    "Xi'an": "China",
    "Beirut": "Lebanon",
    "Geneva": "Switzerland",
    "Colombo": "Sri Lanka",
    "Xiamen": "China",
    "Bucharest": "Romania",
    "Casablanca": "Morocco",
    "Atlanta": "United States",
    "Sofia": "Bulgaria",
    "Dalian": "China",
    "Montevideo": "Uruguay",
    "Amman": "Jordan",
    "Hangzhou": "China",
    "Pune": "India",
    "Durban": "South Africa",
    "Dallas": "United States",
    "Accra": "Ghana",
    "Quito": "Ecuador",
    "Tianjin": "China",
    "Qingdao": "China",
    "Lagos": "Nigeria",
}


# gets user's desired city
def get_location(inp):
    while True:
        if inp.lower() == "end":
            print(
                "\n                                                                                 Thanks for using my program!\n                                                                              I hope the weather treats you well!\n\n\n\n",
                text2art("Good Bye", "alpha"),
            )
            sys.exit()

        if "," not in inp and " " in inp:
            raise ValueError
        try:
            # Split the input into city and country
            city_country = inp.split(",")
            
            if len(city_country) == 1:
                # If only city is provided.
                city = city_country[0].strip()
                # Capitalize every word in the city
                city = " ".join(word.capitalize() for word in city.split())
                # Returns the country name if the city is in the list, else return an empty string
                country = TOP_CITIES.get(city, "")

            elif len(city_country) == 2:
                # If both city and country are provided
                city = city_country[0].strip()
                country = city_country[1].strip().capitalize()
            else:
                raise ValueError

            # Capitalize every word in the city
            city = " ".join(word.capitalize() for word in city.split())

            # Check for empty city or country
            if city == " " or city == "" or country == " " or country == "":
                raise ValueError
            return city, country

        except ValueError:
            print(
                "\nInvalid input. Please enter both the city and country separated by a comma, or type in a city which is in the top 100 most visited cities. (e.g., 'Paris')\n"
            )
            sys.exit()


# API key is hardcoded since I'm using my own API which takes about 1000 requests a month but the function can easily be editted to ask user to make an account on api-ninjas.com and use their own API
# Feel free to use my api key if you're trying out the project but please if you're going to modify the code, contribute to it or use it make your own account on api-ninjas.com and get a free api key from there 100% free.
def api():
    return "MDJcpcQ4ZAuigNGdzSV+Rg==jYP8IlbV5KgxiXXc"


# uses a geocoding api site to get the user's city latitude and longitude (this is the only function that uses the api key)
def geocoding(original_input, api_key, city, country):
    url = f"https://api.api-ninjas.com/v1/geocoding?city={city}&country={country}"
    headers = {"X-Api-Key": api_key}

    response = requests.get(url, headers=headers)
    response = response.json()

    if not response or not isinstance(response, list):
        print(
            f"Error: Unable to retrieve geocoding data for the provided city and country. Your input was {original_input}. Please check your input and try again.\n"
        )
        sys.exit()

    if "latitude" not in response[0] or "longitude" not in response[0]:
        print(
            f"Error: Geocoding data for the provided city and country is incomplete. Your input was {original_input}. Please check your input and try again.\n"
        )
        sys.exit()

    latitude = round(response[0]["latitude"], 3)
    longitude = round(response[0]["longitude"], 3)

    return latitude, longitude


# determines the user's selected city's timezone to not have errors in the hourly data function usage and it's used so that the program doesn't determine the timezone depending on the user's current geographical location but instead depends on the selected city
def get_timezone(latitude, longitude):
    response = requests.get(
        f"https://timeapi.io/api/Time/current/coordinate?latitude={latitude}&longitude={longitude}"
    )
    data = response.json()
    timezone_str = data.get("timeZone")
    return timezone_str


# the weather API which is the program's backbone json
def weather(latitude, longitude):
    w_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}8&current=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,showers,windspeed_10m,winddirection_10m,windgusts_10m&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,visibility,windspeed_180m,winddirection_180m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_probability_max,windspeed_10m_max,winddirection_10m_dominant&timezone=auto"
    response = requests.get(w_url)
    return response.json()


# the hourly data json main function, it handles all errors in the hourly selection accordingly and it contains all the different options the user can choose for hourly weather data, where the user can choose specific hour of data either now or ahead or a number of hours ahead
def get_hourly_data(response_json, current_datetime_obj, city, country):
    flag = False
    current_datetime_isoformat = current_datetime_obj.strftime("%Y-%m-%dT%H:00")
    formatted_time_24h, formatted_time_12h = format_time(
        current_datetime_isoformat, format_24h="%H:%M", format_12h="%I:%M %p"
    )

    while True:
        if flag:
            break
        choice_1 = input(
            "\nDo you want to view multiple hours of weather data or only a specific hour? (type 'multiple' or 'specific' or 'exit' to go back): "
        )

        print(
            f"\nthe current time in the city of your choice is {formatted_time_12h} / {formatted_time_24h}"
        )

        #user chose to view multiple hours of data
        if choice_1 == "multiple":
            while True:
                if flag:
                    break

                try:
                    hours_no = input(
                        "\nHow many hours do you want to view? '(1 hour of data, 2, 3....24) Be mindful that after every hour from now, one less hour of data is available. So, from now, there are 24 available hours of data; from an hour after now, there's only 23, and so on: (type 'exit' to exit) "
                    )

                    if hours_no == "exit":
                        break
                    else:
                        hours_no = int(hours_no)

                    if hours_no > 24 or hours_no < 0:
                        raise ValueError

                    time_frame_input = input(
                        f"\nYou chose to display {hours_no} hours of weather data.\nEnter the number of hours from now to start getting data. You can enter '0' or 'now' to start from the current hour, or you can enter a specific number (e.g., '14') to start getting {hours_no} hours of weather data starting from that many hours in the future: "
                    )
                    if time_frame_input == "now":
                        time_frame_input = "0"

                    #convert the current hour into the hour after time_frame_input is added to current one
                    current_hour_plus_hours = current_datetime_obj + timedelta(
                        hours=int(time_frame_input)
                    )

                    #format the hour into the format the API accepts
                    current_hour_isoformat = current_hour_plus_hours.strftime(
                        "%Y-%m-%dT%H:00"
                    )

                    # since in weather API minutes aren't taken into account in showing hourly data they'll be taken out of display for the user to avoid confusion

                    hour_only24 = current_hour_plus_hours.strftime("%H:00")

                    hour_only12 = current_hour_plus_hours.strftime("%I:00 %p")

                    if not time_frame_input.isdigit():
                        print("Invalid input. Please enter a valid number or 'now'.")
                        continue
                    else:
                        print(
                            f"\nThe time {hours_no} hours of data will be shown starting from is {hour_only24} / {hour_only12}"
                        )

                    try:
                        try_range = 24 - int(time_frame_input)

                        if hours_no > try_range:
                            print(
                                f"\nInvalid, the number of hours of data requested is more than available. You only have a maximum of {try_range} hours of data available from {hour_only24} / {hour_only12}"
                            )
                            break

                    except ValueError:
                        print(
                            "\nInvalid input for the starting hour. Please enter a valid number or 'now'."
                        )
                        break

                    while True:
                        if flag:
                            break

                        else:
                            try:
                                yes = input(
                                    f"\nAre you sure you want to start getting {hours_no} hours of weather data starting from {hour_only24} / {hour_only12}? (yes/no): "
                                ).lower()

                                if yes == "yes":
                                    if "now" == time_frame_input:
                                        time_frame_input = "0"

                                    try:
                                        time_frame = int(time_frame_input)
                                        if time_frame < 0 or time_frame > 23:
                                            raise ValueError(
                                                "\nInvalid hour. Please enter a value between 0 and 23."
                                            )

                                    except ValueError as e:
                                        print(e)
                                        return

                                    else:
                                        if time_frame <= time_frame + hours_no:
                                            flag = True
                                            for hour_offset in range(
                                                int(time_frame_input),
                                                int(time_frame_input) + hours_no,
                                            ):
                                                current_datetime = (
                                                    current_datetime_obj
                                                    + timedelta(hours=hour_offset)
                                                )
                                                current_hour_isoformat = (
                                                    current_datetime.strftime(
                                                        "%Y-%m-%dT%H:00"
                                                    )
                                                )

                                                try:
                                                    current_hour_index = response_json[
                                                        "hourly"
                                                    ]["time"].index(
                                                        current_hour_isoformat
                                                    )
                                                except ValueError:
                                                    print(
                                                        f"Error: {current_hour_isoformat} is not in the list of available times."
                                                    )
                                                    break

                                                hourly_data_list = []

                                                for index in range(
                                                    current_hour_index,
                                                    current_hour_index + 1,
                                                ):
                                                    hourly_data = {}

                                                    for key in response_json["hourly"]:
                                                        hourly_data[
                                                            key
                                                        ] = response_json["hourly"][
                                                            key
                                                        ][
                                                            index
                                                        ]

                                                    hourly_data_list.append(hourly_data)

                                                for hour_data in hourly_data_list:
                                                    display_hourly_data(
                                                        hour_data,
                                                        city,
                                                        country,
                                                        current_datetime_obj,
                                                    )

                                            continue

                                        else:
                                            break

                                elif yes == "no":
                                    break
                                else:
                                    print("Invalid input. Please enter 'yes' or 'no'.")
                                    continue
                            except ValueError as e:
                                print("Invalid input. Please enter 'yes' or 'no'.")
                                break

                except ValueError:
                    print(
                        "\nInvalid number of hours, please choose a number between 1 and 23"
                    )

        elif choice_1 == "specific":
            while True:
                try:
                    hours_no = int(
                        input(
                            "Enter the number of hours from now you wish to view the data of: "
                        )
                    )
                    current_datetime = current_datetime_obj + timedelta(hours=hours_no)
                    current_datetime_isoformat = current_datetime.strftime(
                        "%Y-%m-%dT%H:00"
                    )
                    break
                except ValueError:
                    print(
                        "Invalid input. Please enter a valid integer for the number of hours."
                    )

            try:
                current_hour_index = response_json["hourly"]["time"].index(
                    current_datetime_isoformat
                )
                hourly_data_list = []

                for index in range(current_hour_index, current_hour_index + 1):
                    hourly_data = {}

                    for key in response_json["hourly"]:
                        hourly_data[key] = response_json["hourly"][key][index]

                    hourly_data_list.append(hourly_data)

                for hour_data in hourly_data_list:
                    formatted_time_24h, formatted_time_12h = format_time(
                        hour_data["time"]
                    )

                    yes = input(
                        f"\nAre you sure you want to get data for {formatted_time_12h} / {formatted_time_24h} ? (yes/no): "
                    )

                    if yes.lower() == "no":
                        break
                    elif yes.lower() == "yes":
                        display_hourly_data(
                            hour_data,
                            city,
                            country,
                            current_datetime_obj,
                        )
                        flag = True
                    else:
                        print("Invalid input. Please enter 'yes' or 'no'.")
                        return  # Back to the main question of daily, hourly, or current

            except ValueError:
                print(
                    f"Error: {current_datetime_isoformat} is not in the list of available times."
                )
                return  # Prompt the user again for hourly or daily data

        elif choice_1 == "exit":
            break

        else:
            print("Invalid choice. Please enter 'multiple' or 'specific'.")


# formats the hour_data and prints it accordingly
def display_hourly_data(hour_data, city, country, current_datetime_obj):
    formatted_time_24h, formatted_time_12h = format_time(
        hour_data["time"], format_24h="%H:%M", format_12h="%I:%M %p"
    )
    formatted_wind_direction = approximate_wind_direction(
        hour_data["winddirection_180m"]
    )

    print(
        "\n"
        f"City: {city}, {country}\n"
        f"Date: {current_datetime_obj.strftime('%A %d %B %Y')}\n"
        f"Time: {formatted_time_24h} / {formatted_time_12h}\n"
        f"Temperature: {hour_data['temperature_2m']}°C\n"
        f"Relative Humidity: {hour_data['relativehumidity_2m']}%\n"
        f"Apparent Temperature: {hour_data['apparent_temperature']}°C\n"
        f"Precipitxation Probability: {hour_data['precipitation_probability']}%\n"
        f"Precipitation: {hour_data['precipitation']}mm\n"
        f"Visibility: {hour_data['visibility']}m\n"
        f"Windspeed: {hour_data['windspeed_180m']}km/h\n"
        f"Wind Direction: {formatted_wind_direction} ({hour_data['winddirection_180m']}°)\n"
        f"{'-' * 30}"
    )


# accepts answer from user and formats the daily_data and prints it accordingly
def display_daily_data(response_json, current_date_isoformat, city, country):
    today_index = datetime.now().weekday()

    while True:
        try:
            # Ask for today, tomorrow, or a specific day
            day_choice = input(
                "Enter 'today', 'tomorrow', a certain day of the next week (e.g Wednesday) or 'week' to print the weather data for all available days in the next week for daily weather data: "
            )
            daily_data = response_json["daily"]
            daily_data_today_index = daily_data["time"].index(current_date_isoformat)

            if day_choice.lower() == "today":
                daily_data_index = daily_data_today_index
            elif day_choice.lower() == "tomorrow":
                daily_data_index = daily_data_today_index + 1
            elif day_choice.lower() == "week":
                daily_data_index = daily_data_today_index
                for _ in range(daily_data_today_index, daily_data_today_index + 7):
                    daily_data = {
                        "Date": response_json["daily"]["time"][daily_data_index],
                        "Max precipitation probability": response_json["daily"][
                            "precipitation_probability_max"
                        ][daily_data_index],
                        "Max Temperature": response_json["daily"]["temperature_2m_max"][
                            daily_data_index
                        ],
                        "Min Temperature": response_json["daily"]["temperature_2m_min"][
                            daily_data_index
                        ],
                        "Sunrise": response_json["daily"]["sunrise"][daily_data_index],
                        "Sunset": response_json["daily"]["sunset"][daily_data_index],
                        "Precipitation Sum": response_json["daily"][
                            "precipitation_sum"
                        ][daily_data_index],
                        "Max Windspeed": response_json["daily"]["windspeed_10m_max"][
                            daily_data_index
                        ],
                        "Dominant Wind Direction": response_json["daily"][
                            "winddirection_10m_dominant"
                        ][daily_data_index],
                    }

                    # Format sunrise and sunset times
                    daily_data["Sunrise"] = datetime.fromisoformat(
                        daily_data["Sunrise"]
                    )

                    daily_data["Sunset"] = datetime.fromisoformat(daily_data["Sunset"])

                    # Format sunrise and sunset times
                    formatted_sunrise_24h, formatted_sunrise_12h = format_time(
                        daily_data["Sunrise"]
                    )
                    formatted_sunset_24h, formatted_sunset_12h = format_time(
                        daily_data["Sunset"]
                    )

                    # Approximate wind direction to cardinal directions
                    approximate_direction = approximate_wind_direction(
                        daily_data["Dominant Wind Direction"]
                    )

                    date_str = daily_data["Date"]
                    date_object = datetime.strptime(date_str, "%Y-%m-%d")
                    formatted_date = date_object.strftime("%A %d %B %Y")

                    print(
                        "\n"
                        f"City: {city}, {country}\n"
                        f"Date: {formatted_date}\n"
                        f"Max Precipitation Probability: {daily_data['Max precipitation probability']}%\n"
                        f"Max Temperature: {daily_data['Max Temperature']}°C\n"
                        f"Min Temperature: {daily_data['Min Temperature']}°C\n"
                        f"Sunrise (24h): {formatted_sunrise_24h}\n"
                        f"Sunrise (12h): {formatted_sunrise_12h}\n"
                        f"Sunset (24h): {formatted_sunset_24h}\n"
                        f"Sunset (12h): {formatted_sunset_12h}\n"
                        f"Precipitation Sum: {daily_data['Precipitation Sum']}mm\n"
                        f"Max Windspeed: {daily_data['Max Windspeed']}km/h\n"
                        f"Dominant Wind Direction: {daily_data['Dominant Wind Direction']}° ({approximate_direction})\n"
                        f"{'-' * 35}"
                    )

                    daily_data_index += 1

                break  # Exit the loop if everything is successful
            else:
                # Convert the entered day of the week to the corresponding date
                days_of_week = [
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ]
                chosen_day_index = (
                    days_of_week.index(day_choice.capitalize()) - today_index
                ) % 7
                chosen_day = datetime.now() + timedelta(days=chosen_day_index)
                chosen_day_str = chosen_day.strftime("%Y-%m-%d")

                daily_data_index = response_json["daily"]["time"].index(chosen_day_str)

            daily_data = {
                "Date": response_json["daily"]["time"][daily_data_index],
                "Max precipitation probability": response_json["daily"][
                    "precipitation_probability_max"
                ][daily_data_index],
                "Max Temperature": response_json["daily"]["temperature_2m_max"][
                    daily_data_index
                ],
                "Min Temperature": response_json["daily"]["temperature_2m_min"][
                    daily_data_index
                ],
                "Sunrise": response_json["daily"]["sunrise"][daily_data_index],
                "Sunset": response_json["daily"]["sunset"][daily_data_index],
                "Precipitation Sum": response_json["daily"]["precipitation_sum"][
                    daily_data_index
                ],
                "Max Windspeed": response_json["daily"]["windspeed_10m_max"][
                    daily_data_index
                ],
                "Dominant Wind Direction": response_json["daily"][
                    "winddirection_10m_dominant"
                ][daily_data_index],
            }

            # Format sunrise and sunset times
            daily_data["Sunrise"] = datetime.fromisoformat(daily_data["Sunrise"])

            daily_data["Sunset"] = datetime.fromisoformat(daily_data["Sunset"])

            # Format sunrise and sunset times
            formatted_sunrise_24h, formatted_sunrise_12h = format_time(
                daily_data["Sunrise"]
            )
            formatted_sunset_24h, formatted_sunset_12h = format_time(
                daily_data["Sunset"]
            )

            # Approximate wind direction to cardinal directions
            approximate_direction = approximate_wind_direction(
                daily_data["Dominant Wind Direction"]
            )

            date_str = daily_data["Date"]
            date_object = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_object.strftime("%A %d %B %Y")

            print(
                "\n"
                f"City: {city}, {country}\n"
                f"Date: {formatted_date}\n"
                f"Max Precipitation Probability: {daily_data['Max precipitation probability']}%\n"
                f"Max Temperature: {daily_data['Max Temperature']}°C\n"
                f"Min Temperature: {daily_data['Min Temperature']}°C\n"
                f"Sunrise (24h): {formatted_sunrise_24h}\n"
                f"Sunrise (12h): {formatted_sunrise_12h}\n"
                f"Sunset (24h): {formatted_sunset_24h}\n"
                f"Sunset (12h): {formatted_sunset_12h}\n"
                f"Precipitation Sum: {daily_data['Precipitation Sum']}mm\n"
                f"Max Windspeed: {daily_data['Max Windspeed']}km/h\n"
                f"Dominant Wind Direction: {daily_data['Dominant Wind Direction']}° ({approximate_direction})\n"
            )

            break
        except ValueError:
            print("Invalid input. Please enter a valid day.")
        except IndexError:
            print("Invalid input. Please enter a valid day.")


# displays the current data using get_current_data
def display_current_data(current_data, city, country, current_datetime_obj):
    formatted_time_24h, formatted_time_12h = format_time(
        current_data["time"], format_24h="%H:%M", format_12h="%I:%M %p"
    )
    formatted_wind_direction = approximate_wind_direction(
        current_data["winddirection_10m"]
    )

    print(
        "\n"
        f"City: {city}, {country}\n"
        f"Date: {current_datetime_obj.strftime('%A %d %B %Y')}\n"
        f"Time: {formatted_time_24h} / {formatted_time_12h}\n"
        f"Temperature: {current_data['temperature_2m']}°C\n"
        f"Relative Humidity: {current_data['relativehumidity_2m']}%\n"
        f"Apparent Temperature: {current_data['apparent_temperature']}°C\n"
        f"Precipitation: {current_data['precipitation']}mm\n"
        f"Windspeed: {current_data['windspeed_10m']}km/h\n"
        f"Wind Direction: {formatted_wind_direction} ({current_data['winddirection_10m']}°)\n"
        f"Wind Gusts: {current_data['windgusts_10m']}km/h\n"
        f"{'-' * 30}"
    )


# extracts current data from the json
def get_current_data(response_json, current_datetime_obj, city, country):
    current_data = response_json["current"]
    current_data["time"] = datetime.strptime(current_data["time"], "%Y-%m-%dT%H:%M")
    display_current_data(current_data, city, country, current_datetime_obj)


# The main function of the program
def main():
    print("\n", text2art("  Weather App", font="slant"))
    print(
        "              Welcome to the Weather App! Your go-to for current, daily and hourly weather information.\n"
    )

    while True:
        try:
            # Get user input for city and country
            original_inp = input(
                "Please enter the city and country name (e.g., 'London, England') to view its weather data, or only the city's name if it's in the top 100 most visited cities (or type 'end' to end): "
            ).strip()

            city, country = get_location(original_inp)
            api_key = api()
            # Get latitude and longitude of the selected city
            latitude, longitude = geocoding(original_inp, api_key, city, country)

            # Get timezone of the selected city
            time_zone_data = get_timezone(latitude, longitude)
            weather_data = weather(latitude, longitude)

            # Convert datetime to the timezone of the selected city
            time_zone = timezone(time_zone_data)
            current_datetime_obj = datetime.now(time_zone)
            current_date_isoformat = current_datetime_obj.strftime("%Y-%m-%d")

            while True:
                choice = (
                    input(
                        "\nDo you want to view current, hourly, or daily weather data? (Type 'exit' to choose a new city, 'end' to end the program): "
                    )
                    .lower()
                    .strip()
                )
                # Check user choice and execute the corresponding function
                if choice == "exit":
                    break
                elif choice == "current":
                    get_current_data(weather_data, current_datetime_obj, city, country)
                elif choice == "hourly":
                    get_hourly_data(weather_data, current_datetime_obj, city, country)
                elif choice == "daily":
                    display_daily_data(
                        weather_data, current_date_isoformat, city, country
                    )
                elif choice == "end":
                    print(
                        "\n                                                                                 Thanks for using my program!\n                                                                              I hope the weather treats you well!\n\n\n\n",
                        text2art("Good Bye", "alpha"),
                    )
                    sys.exit()
                else:
                    print(
                        "Invalid choice. Please enter 'current', 'hourly', 'daily', 'exit', or 'end'\n"
                    )

        except Exception as e:
            print(f"An unexpected error occurred: {e}\n")
            sys.exit()


if __name__ == "__main__":
    main()
