from django.http import JsonResponse
from rest_framework.decorators import api_view
import json

@api_view(['POST'])
def pros(request):
    try:
        
        data = json.loads(request.body)
        #print(data)
        diagram_data = data.get('diagramData', {})  # Get the 'diagramData' dictionary from the received data

        if 'data' in diagram_data:
            diagram_info = diagram_data['data']
            diagram_name = diagram_info.get('name', 'Nombre por defecto')  # Access the 'name' field from the 'data' dictionary
            user_stories = diagram_info.get("json_user_histories", "historias por defecto")
            response_data = {
                'success': True,
                'diagram_name': diagram_name,
                # ...otros datos que quieras enviar al frontend...
                'User Stories': user_stories,
            }

            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Datos de diagrama no encontrados'}, status=400)

    except Exception as e:
        # Manejo de errores
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

