from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Open-Meteo API endpoint
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Default coordinates for major cities
CITIES = {
    'rome': {'lat': 41.9028, 'lon': 12.4964},
    'milan': {'lat': 45.4642, 'lon': 9.1900},
    'naples': {'lat': 40.8518, 'lon': 14.2681},
    'turin': {'lat': 45.0703, 'lon': 7.6869},
    'palermo': {'lat': 38.1157, 'lon': 13.3615},
    'genoa': {'lat': 44.4056, 'lon': 8.9463},
    'bologna': {'lat': 44.4949, 'lon': 11.3426},
    'florence': {'lat': 43.7696, 'lon': 11.2558},
    'bari': {'lat': 41.1102, 'lon': 16.8544},
    'catania': {'lat': 37.5079, 'lon': 15.0833}
}

@app.route('/')
def index():
    return jsonify({
        'message': 'Weather API with Open-Meteo',
        'endpoints': {
            '/weather/<city>': 'Get weather for a city',
            '/weather': 'Get weather via query params'
        },
        'available_cities': list(CITIES.keys())
    })

@app.route('/weather/<city>')
def weather_by_city(city):
    city_lower = city.lower()
    
    if city_lower not in CITIES:
        return jsonify({'error': f'City not found. Available: {list(CITIES.keys())}'}), 404
    
    coords = CITIES[city_lower]
    return get_weather(coords['lat'], coords['lon'], city_lower.capitalize())

@app.route('/weather')
def weather_by_params():
    city = request.args.get('city', 'Rome')
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        city_lower = city.lower()
        if city_lower in CITIES:
            coords = CITIES[city_lower]
            lat = coords['lat']
            lon = coords['lon']
        else:
            lat = 41.9028
            lon = 12.4964
    
    return get_weather(lat, lon, city)

def get_weather(lat, lon, city_name):
    params = {
    'latitude': lat,
    'longitude': lon,
    'current': 'temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m',
    'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code',
    'timezone': 'auto',
    'forecast_days': 7
}
    try:
        response = requests.get(OPEN_METEO_URL, params=params)
        data = response.json()
        
        current = data.get('current', {})
        daily = data.get('daily', {})
        
        result = {
            'city': city_name,
            'latitude': lat,
            'longitude': lon,
            'current': {
                'temperature': current.get('temperature_2m'),
                'weather_code': current.get('weather_code'),
                'wind_speed': current.get('wind_speed_10m'),
                'humidity': current.get('relative_humidity_2m')
            },
            'daily': [
                {
                    'date': daily.get('time', [None] * 7)[i] if i < len(daily.get('time', [])) else None,
                    'temp_max': daily.get('temperature_2m_max', [None] * 7)[i] if i < len(daily.get('temperature_2m_max', [])) else None,
                    'temp_min': daily.get('temperature_2m_min', [None] * 7)[i] if i < len(daily.get('temperature_2m_min', [])) else None,
                    'precipitation': daily.get('precipitation_sum', [None] * 7)[i] if i < len(daily.get('precipitation_sum', [])) else None,
                    'weather_code': daily.get('weather_code', [None] * 7)[i] if i < len(daily.get('weather_code', [])) else None
                }
                for i in range(min(7, len(daily.get('time', []))))
            ]
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)