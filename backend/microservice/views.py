from django.http import JsonResponse
from rest_framework.decorators import api_view
import json
from .clustering import cluster_user_stories


def extract_user_story_info(data):
    # Acceder a la lista de user_stories
    user_stories = data["userStories"]

    # Crear una lista para almacenar la información de cada user story
    user_stories_info = []
    for user_story in user_stories:
        us_info = {
            "id": user_story["id"],
            "name": user_story["name"],
            "points": user_story["points"],
            "priority":user_story["priority"],
            "actor": user_story["actor"],
            "purpose":user_story["purpose"]
        }

        if "dependencies" in user_story:
            dependencies = []
            for dependency in user_story["dependencies"]:
                dependencies.append({
                    "id": dependency["id"],
                    "name": dependency.get("name", ""),
                })
            us_info["dependencies"] = dependencies
        
        user_stories_info.append(us_info)
    return user_stories_info

# ...

@api_view(['POST'])
def microdiagram(request):
    try:
        data = json.loads(request.body)
        diagram_data = data.get('diagramData', {})

        if 'data' in diagram_data:
            diagram_info = diagram_data['data']
            diagram_name = diagram_info.get('name', 'Nombre por defecto')
            user_stories = diagram_info.get("json_user_histories", "historias por defecto")

            user_story_info = extract_user_story_info(user_stories)
            clusters = cluster_user_stories(user_story_info)
            stories = []
            print(clusters)
            for cluster_id, cluster_stories in clusters.items():
                stories.append({ 
                    "cohesionLack": 0, 
                    "cohesionGrade": 0, 
                    "couplingADS": 0,  
                    "couplingAIS": 0,  
                    "couplingSIY": 0, 
                    "complexity": sum(story[2] for story in cluster_stories), 
                    "id": f"MS {cluster_id + 1}",
                    "points": sum(int(story[2]) for story in cluster_stories), 
                    "semanticSimilarity": 100,  
                    "userStories": [{
                        "id": story[0],
                        "name": story[1],
                        "description": story[6], 
                        "actor": story[5], 
                        "points": story[2],  
                        "project": diagram_name,  
                        "priority": story[4],
                        "dependencies": story[3] if len(story) > 3 else [] 
                    } for story in cluster_stories]
                })

            return JsonResponse({'success': True, 'data': stories})
        else:
            return JsonResponse({'success': False, 'error': 'Datos de diagrama no encontrados'})

    except Exception as e:
        # Manejo de errores
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


