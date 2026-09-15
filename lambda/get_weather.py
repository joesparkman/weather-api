"""
get_weather.py

Lambda function behind both the HTTP API and REST API in this project.
Reads optional lat/lon query string parameters, calls Open-Meteo's free
public forecast API, and returns the current weather conditions as JSON.

No API key or auth of any kind is required to call Open-Meteo itself --
that's what makes it a good "practice API" for learning API Gateway
without needing to manage upstream credentials.
"""

import json
import urllib.request


def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    lat = params.get('lat', '33.7490')   # defaults to Atlanta, GA
    lon = params.get('lon', '-84.3880')

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        return {
            'statusCode': 502,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Failed to reach upstream weather service', 'detail': str(e)})
        }

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data.get('current_weather', {}))
    }
