from fastapi import FastAPI
from fastapi.responses import JSONResponse
import socket
from datetime import datetime
import requests

app = FastAPI(
    title="Weather API",
    description="API that returns server info and live weather for Dhaka.",
    version="1.0.0",
    docs_url="/",  # Swagger UI  "/"
    redoc_url=None  
)

# OpenWeatherMap API key
WEATHER_API_KEY = "65b80ec4a582f623b479b6eef1d79d94"
WEATHER_URL = f"https://api.openweathermap.org/data/2.5/weather?q=Dhaka&appid={WEATHER_API_KEY}"

@app.get("/api/hello")
def get_hello():
    hostname = socket.gethostname()
    current_dt = datetime.now().strftime("%y%m%d%H%M")

    try:
        response = requests.get(WEATHER_URL)
        weather_data = response.json()

        temperature_k = weather_data['main']['temp']
        temperature_c = round(temperature_k - 273.15, 2)

        result = {
            "hostname": hostname,
            "datetime": current_dt,
            "version": "1.0.0",
            "weather": {
                "dhaka": {
                    "temperature": str(temperature_c),
                    "temp_unit": "c"
                }
            }
        }

        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/api/health")
def health_check():
    try:
        response = requests.get(WEATHER_URL)
        if response.status_code == 200:
            return {"status": "healthy", "weather_api": "reachable"}
        else:
            return {"status": "unhealthy", "weather_api": f"error - status code {response.status_code}"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
