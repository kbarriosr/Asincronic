import aiohttp
from aiohttp import web

API_KEY = '9ahhC921qryabg7sgyf5fu9xvg6511bryegf3n'

async def obtener_clima(request):
    try:
        ciudad = request.query.get('ciudad', 'Buenos Aires')
        url = f'https://api.meteosource.com/v1/free/point?place={ciudad}&key={API_KEY}&units=metric&lang=es'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:  # ✅ Correcto
                if response.status != 200:  # ❌ Aquí estaba el error de indentación
                    error_data = await response.text()
                    print(f"Error en API externa: {error_data}")
                    return web.json_response({'error': 'Error al obtener datos del clima'}, status=500)

                data = await response.json()
                print(data)
                clima_data = {
                    'ciudad': data.get('city', {}).get('name', 'Desconocido'),
                    'temperatura': data.get('data', {}).get('current', {}).get('temperature', 'N/A'),
                    'descripcion': data.get('data', {}).get('current', {}).get('weather', 'N/A'),
                    'humedad': data.get('data', {}).get('current', {}).get('humidity', 'N/A'),
                }
                return web.json_response(clima_data)

    except Exception as e:
        print(f"Error interno: {e}")
        return web.json_response({'error': 'Error interno en el servidor'}, status=500)

app = web.Application()
app.router.add_get('/clima', obtener_clima)

if __name__ == "__main__":
    web.run_app(app, port=3020)
