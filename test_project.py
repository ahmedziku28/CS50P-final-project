#we will only test the functions that don't depend on the weather api outputs since it changes every hour and every day.

from project import format_time, approximate_wind_direction,get_location, geocoding, get_timezone
import pytest
from datetime import datetime

def test_format_time():
    time_obj_1 = datetime(2023, 11, 22, 14, 30)  # 2:30 PM
    result_1 = format_time(time_obj_1)
    assert result_1[0] == "14:30"  # 24-hour format
    assert result_1[1] == "02:30 PM"  # 12-hour format

    time_obj_2 = "2023-11-22T08:45"
    result_2 = format_time(time_obj_2)
    assert result_2[0] == "08:45"  # 24-hour format
    assert result_2[1] == "08:45 AM"  # 12-hour format

    time_obj_3 = datetime(2023, 11, 22, 18, 15)  # 6:15 PM
    result_3 = format_time(time_obj_3, format_24h="%H-%M")
    assert result_3[0] == "18-15"  # Custom 24-hour format
    assert result_3[1] == "06:15 PM"  # 12-hour format

def test_approximate_wind_direction():
    # putting errors handling the degrees that could be outside of the realistic scope is impossible since we rely on the API to provide those values not the user themself

    assert approximate_wind_direction(350) == "North"
    assert approximate_wind_direction(200) == "South"
    assert approximate_wind_direction(100) == "East"
    assert approximate_wind_direction(250) == "West"
    assert approximate_wind_direction(230) == "South-West"
    assert approximate_wind_direction(50) == "North-East"
    assert approximate_wind_direction(150) == "South-East"
    assert approximate_wind_direction(300) == "North-West"

def test_get_location():

    with pytest.raises(SystemExit):
        get_location("end")
    
    result = get_location("Alexandria, Egypt")
    assert result[0] == "Alexandria"
    assert result[1] == "Egypt"

    result = get_location("alexandria, egypt")
    assert result[0] == "Alexandria"
    assert result[1] == "Egypt"

    result = get_location("alexandria,egypt")
    assert result[0] == "Alexandria"
    assert result[1] == "Egypt"

    result = get_location("Alexandria,egypt")
    assert result[0] == "Alexandria"
    assert result[1] == "Egypt"

    result = get_location("Alexandria, egypt")
    assert result[0] == "Alexandria"
    assert result[1] == "Egypt"

    result = get_location("alexandria, Egypt")
    assert result[0] == "Alexandria"
    assert result[1] == "Egypt"

    result = get_location("alexandria,Egypt")
    assert result[0] == "Alexandria"
    assert result[1] == "Egypt"
    
    with pytest.raises(ValueError):
        get_location("alexandria egypt")

    with pytest.raises(SystemExit):
        get_location("AlexandriaEgypt")

    with pytest.raises(SystemExit):
        get_location("alexandriaegypt")

def test_geocoding():


    api_key = "60i4xHIgm+ib684r5m36Rw==P23smQOMCVzE7zsJ"

    result = geocoding("Paris, France", api_key, "Paris", "France")
    assert isinstance(result[0], float)
    assert isinstance(result[1], float)

    with pytest.raises(SystemExit):
        geocoding("NonexistentCity, NonexistentCountry", api_key, "NonexistentCity", "NonexistentCountry")

    with pytest.raises(SystemExit):
        geocoding("City, Country", "", "City", "Country")

def test_get_timezone():
    #San francisco, USA
    assert get_timezone(37.7749, -122.4194) == "America/Los_Angeles"

    #New York, USA
    assert get_timezone(40.7128, -74.0060) == "America/New_York"

    #Paris, France
    assert get_timezone(48.8566, 2.3522) == "Europe/Paris"
    
    #Tokyo, Japan
    assert get_timezone(35.6895, 139.6917) == "Asia/Tokyo"
    
    #Cairo, Egypt
    assert get_timezone(30.0444, 31.2357) == "Africa/Cairo"

    #Sydney, Australia
    assert get_timezone(-33.8688, 151.2093) == "Australia/Sydney"

    #Rio de janeiro, Brazil
    assert get_timezone(-22.9068, -43.1729) == "America/Sao_Paulo"