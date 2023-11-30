# CityWeatherInsight

## Table of Contents

1. [Project Title](##Project-Title)
2. [Description](##Description)
3. [Installation](##Installation)
4. [Usage](##Usage)
5. [Design Choices](##Design-Choices) 
6. [Contributing](##Contributing)

## CS50P
>This is my final project to conclude the CS50P introduction to programming with python course presented by harvard

## Project Title: CityWeatherInsight

## Description

CityWeatherInsight is a Python-based weather app designed to provide daily, hourly, and current weather data for cities worldwide. The app leverages three API request links to gather comprehensive weather information:

### APIs Used

1. **Geocoding API:**
    - **Endpoint:** `https://api.api-ninjas.com/v1/geocoding?city={city}&country={country}`
    - **Purpose:** Retrieves latitude and longitude coordinates for the specified city and country.

2. **TimeAPI:**
    - **Endpoint:** `https://timeapi.io/api/Time/current/coordinate?latitude={latitude}&longitude={longitude}`
    - **Purpose:** Determines the selected city's time zone based on its geographical coordinates.

3. **Open Meteo API:**
    - **Endpoint:** `https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}8&current=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation,rain,showers,windspeed_10m,winddirection_10m,windgusts_10m&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,visibility,windspeed_180m,winddirection_180m&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_sum,precipitation_probability_max,windspeed_10m_max,winddirection_10m_dominant&timezone=auto`
    - **Purpose:** The main API source containing a wealth of weather data, including temperature, humidity, precipitation, wind speed, and more.

The program features a user-friendly, step-by-step interface, guiding users through the exploration of detailed weather insights powered by Open Meteo services.


## Installation

To get started with CityWeatherInsight, follow these steps:

### Prerequisites

Make sure you have the following installed on your machine:

- [Python](https://www.python.org/) (version 3.7 or higher)

### Clone the Repository

```bash
    git clone https://github.com/ahmedziku28/CityWeatherInsight.git
```

### Navigate to the Project Directory

```bash
    cd CityWeatherInsight
```

### Obtain API key
CityWeatherInsight relies on a single external API for weather data. Obtain an API key by logging into

- [API Ninjas](https://api-ninjas.com/register)

After obtaining the API key from your profile upon signing up for free, replace it in the specified place in the code within the `api()` function at the very top of the project.

```python
    def api():
        return "YOUR_API_NINJA_KEY"
```

- _There is already an API key there for convenience if you_ **only want to try the program.**
***but please if you want to contribute to the program use your own API key, it is free to sign up.***

### Install the required Python packages
```bash
    pip install art requests pytz
```

## Usage

To use the Weather App, follow these steps:

1. **API Key:**
    - Open the `project.py` file and locate the `api()` function.
    - Replace the hardcoded API key with your own API key. If you don't have one, you can obtain it from [api-ninjas.com](https://api-ninjas.com/).

2. **Run the Program:**
    - After updating the API key, save the changes to the `project.py` file.
    - Run the program. No further changes are required within the code.

3. **City Selection:**
    - Upon running the program, you will be prompted to enter a city and country (e.g., 'London, England').
    - If the city is in the top 100 most visited cities, you can enter only the city's name.

4. **Weather Data Options:**
    - After entering the city and country, you can choose from three types of weather data:
        1. **Daily Weather:**
            - **Purpose:** Retrieves daily weather data.
            - You can choose to retrieve weather data for any day of the week, including today. The option to display the weather for the entire week at once is also available.

        2. **Hourly Weather:**
            - **Purpose:** Retrieves hourly weather data.
            - You can choose to view weather data for a specific hour or multiple hours from the current time or from a time in the future.

        3. **Current Weather:**
            - **Purpose:** Retrieves the most recent weather data for the selected city.

5. **Exiting the Program:**
    - Type 'exit' at the second prompt to choose a new city.
    - Type 'end' at the 1st or 2nd prompt to end the program.

Enjoy exploring the weather data for any city on Earth with the Weather App!


## Design Choices
The program was initially meant to be a learning exercise to improve my ability to code in Python using lists and dictionaries rather than to be my final project. I opted for a weather API JSON because it offered a large dictionary with numerous nested lists and dicts, which made it a great chance for me to improve my skills. I was inspired with ideas for improving the project after devoting around ten hours to it initially. When I dug deeper into the JSON structure, I found that it had a wealth of daily, current, and hourly meteorological data that could be applied to any city in the world given latitude, longitude, and timezone information were easily obtainable.

I started working on this project at the end of October, when I was still in the course's week 7. But after spending around 20 hours coding, improving and perfecting the program, I decided to take it a step further and turn it into my final CS50P project, going beyond its original goal of skill development.

The code didn't include any smaller functions; it was written in one big structure at first. The need for custom functions emerged as the codebase and functionality grew, requiring extensive googling and searching.

My biggest difficulties were:
- coming up with a function that could print data for multiple hours
- indexing the day the user entered with the correct day of the week in the future 
- overcoming significant obstacles while handling the hourly data in the program.
- Converting datetime objects into various string formats and vice versa was another significant challenge that required substantial study on my part.

Finally, in total the program took me about 40-50 total hours of coding work scattered across 32 days.

These design decisions are a reflection of my progress from a basic coding exercise to a powerful, all-inclusive weather application that can also handle a wide range of errors.
## Contributing

Thank you for considering contributing to the Weather App! Contributions/ modifications are essential for improving and expanding the functionality of any application.

### Getting Started

To contribute to the project, follow these steps:

1. Fork the repository to your GitHub account.
2. Clone the forked repository to your local machine:
   ```bash
   git clone https://github.com/your-username/weather-app.git
   ```
3. Create a new branch for your changes:
    ```bash
    git checkout -b feature/your-feature
4. Make your modifications and commit changes:
```bash
git commit -m "Add your commit message here"
```
### Code Style
- Ensure your code follows the existing code style of the project. The code is formatted using [Black](https://github.com/psf/black)
### Submitting changes
1- push your changes to your forked repository:
```bash
git push origin feature/your-feature
```
2- Open a pull request to the main repository and provide a clear title and description for your changes

### Code of Conduct
Please note that this project is released with a [Contributor Code of Conduct](https://github.com/syntax-tree/.github/blob/main/code-of-conduct.md). By participating in this project, you agree to abide by its terms

### Adding a GUI

I understand that creating a graphical user interface (GUI) for the Weather App can greatly enhance the user experience and since I started on this project it's been the main feature I wanted to add. Since I am still a beginner in the coding field, if you have experience in GUI development and are interested in contributing this feature, I welcome your assistance!

#### How to Contribute a GUI:

1. **Express Your Interest:**
   - If you are interested in creating a GUI for the Weather App, please open an issue to express your intention. This helps avoid duplication of efforts and allows others to provide feedback.

2. **Coordinate with Maintainers:**
   - Coordinate with the project maintainers to discuss the design, features, and compatibility of the GUI. This ensures that your contribution aligns with the goals of the project.

3. **Submit a Pull Request:**
   - Once the GUI is developed, submit a pull request to the main repository. Include detailed documentation on how to integrate and use the GUI within the existing codebase.

4. **Testing and Collaboration:**
   - Collaborate with the maintainer and the community to test the GUI thoroughly. Address any feedback or issues that may arise during the review process.

#### Important Note:

- While creating a GUI is a valuable addition, it's important to ensure that the core functionality of the Weather App remains intact and accessible via the command line interface (CLI). GUI contributions should enhance the user experience without compromising the program's primary functionality.

Thank you for considering contributing to the CityWeatherInsight's development! Your efforts are greatly appreciated.
## Reporting Issues
**If you encounter any issues or have suggestions for improvement, please open an issue on the GitHub repository.**
## Acknowledgements
I'd like to thank Harvard, Professor David J. Malan and all of the CS50 and CS50P team for their efforts and making this course free. I'd also like to thank all my friends that helped me grasp difficult computer science concepts along the way. The knowledge I gained and the experience I had throughout the course was something truly remarkable.  
  

This was CS50!

[Linkedin Ahmed Aly](https://www.linkedin.com/in/ahmed-aly-301923226/)