#!/usr/bin/env python3
import json
import os
import time
import urllib.request

CACHE_FILE = "/tmp/waybar_weather_cache.json"
CACHE_DURATION = 900  # 15 minutes

WEATHER_ICONS = {
    "113": "\ue302",  # Sunny / Clear
    "116": "\ue304",  # Partly cloudy
    "119": "\ue312",  # Cloudy
    "122": "\ue312",  # Overcast
    "143": "\ue313",  # Mist
    "176": "\ue318",  # Patchy rain possible
    "179": "\ue31a",  # Patchy snow possible
    "182": "\ue31a",  # Patchy sleet possible
    "185": "\ue318",  # Patchy freezing drizzle possible
    "200": "\ue31d",  # Thundery outbreaks possible
    "227": "\ue31a",  # Blowing snow
    "230": "\ue31a",  # Blizzard
    "248": "\ue313",  # Fog
    "260": "\ue313",  # Freezing fog
    "263": "\ue318",  # Patchy light drizzle
    "266": "\ue318",  # Light drizzle
    "281": "\ue318",  # Freezing drizzle
    "284": "\ue318",  # Heavy freezing drizzle
    "293": "\ue318",  # Patchy light rain
    "296": "\ue318",  # Light rain
    "299": "\ue318",  # Moderate rain at times
    "302": "\ue318",  # Moderate rain
    "305": "\ue318",  # Heavy rain at times
    "308": "\ue318",  # Heavy rain
    "311": "\ue318",  # Light freezing rain
    "353": "\ue318",  # Light rain shower
    "356": "\ue318",  # Moderate or heavy rain shower
    "359": "\ue318",  # Torrential rain shower
    "386": "\ue31d",  # Patchy light rain with thunder
    "389": "\ue31d",  # Moderate or heavy rain with thunder
}


WEATHER_TRANSLATIONS = {
    "Sunny": "Ensolarado",
    "Clear": "Céu Limpo",
    "Partly cloudy": "Parcialmente Nublado",
    "Partly Cloudy": "Parcialmente Nublado",
    "Cloudy": "Nublado",
    "Overcast": "Encoberto",
    "Mist": "Névoa",
    "Patchy rain possible": "Possibilidade de Chuva",
    "Light Rain": "Chuva Leve",
    "Light rain": "Chuva Leve",
    "Moderate rain": "Chuva Moderada",
    "Heavy rain": "Chuva Forte",
    "Thundery outbreaks possible": "Possibilidade de Trovoadas",
    "Fog": "Neblina",
}

data = None

# Try cache
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)
            if time.time() - cache.get("time", 0) < CACHE_DURATION:
                data = cache.get("data")
    except Exception:
        pass

# Fetch if no valid cache
if not data:
    try:
        req = urllib.request.Request(
            "https://wttr.in/?format=j1",
            headers={"User-Agent": "curl/7.68.0"}
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            data = json.loads(response.read().decode("utf-8"))
            with open(CACHE_FILE, "w") as f:
                json.dump({"time": time.time(), "data": data}, f)
    except Exception:
        # Fallback to stale cache if request fails
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    data = json.load(f).get("data")
            except Exception:
                pass

if data and "current_condition" in data:
    curr = data["current_condition"][0]
    temp = curr.get("temp_C", "--")
    code = curr.get("weatherCode", "113")
    desc_raw = curr.get("weatherDesc", [{}])[0].get("value", "").strip()
    feels = curr.get("FeelsLikeC", temp)
    humidity = curr.get("humidity", "--")

    icon = WEATHER_ICONS.get(code, "")
    desc = WEATHER_TRANSLATIONS.get(desc_raw, desc_raw)

    output = {
        "text": f"{icon}  {temp}°C",
        "tooltip": f"{desc}\nSensação térmica: {feels}°C\nUmidade: {humidity}%"
    }
else:
    output = {
        "text": "  --°C",
        "tooltip": "Clima indisponível"
    }

print(json.dumps(output, ensure_ascii=False))
