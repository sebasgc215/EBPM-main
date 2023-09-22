from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from .clustering import cluster_user_stories, cluster_text_user_stories


def extract_user_story_info(data):
    # Acceder a la lista de user_stories
    user_stories = data["userStories"]

    # Crear una lista para almacenar la información de cada user story
    user_stories_info = []

    # Recorrer cada user story en la lista
    for user_story in user_stories:
        us_info = {
            "id": user_story["id"],
            "name": user_story["name"],
            "points": user_story["points"]
        }
        
        # Verificar si el user story tiene dependencias
        if "dependencies" in user_story:
            dependencies = []
            for dependency in user_story["dependencies"]:
                dependencies.append(dependency["name"])
            us_info["dependencies"] = dependencies
        
        user_stories_info.append(us_info)

    return user_stories_info

@api_view(['POST'])
def microtext(request):
    try:
        data = json.loads(request.body)
        diagram_data = data.get('diagramData', {})
        print(diagram_data)
        # Llama a la función cluster_user_stories con los datos
        clusters = cluster_text_user_stories(diagram_data)

        # Crear una lista de cadenas para representar los clusters
        cluster_strings = []

        # Iterar a través de los clusters y sus historias
        for cluster_id, stories in clusters.items():
            # Crear una cadena para representar el cluster
            cluster_string = f'Cluster {cluster_id + 1}: '

            # Agregar los nombres de las historias al cluster
            story_strings = [f'{story[0]}, {story[1]}' for story in stories]

            # Concatenar los nombres de las historias con comas y espacios
            cluster_string += ', '.join(story_strings)

            # Agregar esta cadena al resultado
            cluster_strings.append(cluster_string)

        # Unir todas las cadenas de cluster con saltos de línea
        response_data = '\n'.join(cluster_strings)

        # Devolver la respuesta como un JsonResponse
        return JsonResponse({'clusters': response_data})



    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON data is invalid'}, status=400)



@api_view(['POST'])
def microdiagram(request):
    try:
        
        data = json.loads(request.body)
        
        diagram_data = data.get('diagramData', {})  

        if 'data' in diagram_data:
            diagram_info = diagram_data['data']
            diagram_name = diagram_info.get('name', 'Nombre por defecto')  
            user_stories = diagram_info.get("json_user_histories", "historias por defecto")
                        # Acceder a la lista de user_stories
            
            user_story_info = extract_user_story_info(user_stories)
            clusters = cluster_user_stories(user_story_info)
           # clusters_array = []
            stories = []
            clusters = cluster_user_stories(user_story_info)
            for cluster_id, cluster_stories in clusters.items():
                stories.append(f"Cluster {cluster_id + 1}: {', '.join(story[0] for story in cluster_stories)}")

            response_data = {
                'success': True,
                'diagram_name': diagram_name,
                'stories': stories
            }

            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Datos de diagrama no encontrados'}, status=400)

    except Exception as e:
        # Manejo de errores
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

