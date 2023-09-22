import {
    API_URL
} from '../utils';

export const createTextDiagram = async (data) => {
    return await fetch(`${API_URL}/diagramtext/create/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data) // No necesitas anidarlos en un objeto {data}
    }).then(response => response.json());
}



export const createDiagram = async (data) => {
    return await fetch(`${API_URL}/diagrams/create/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': String(data.name),
            'description': String(data.description),
            'xml': String(data.xml),
            'svg': String(data.svg),
            'json_user_histories': data.json_user_histories,
            'id_project': String(data.id_project)
        })
    }).then(response => response.json())
}

export const listDiagram = async (projectId) => {
    return await fetch(`${API_URL}/diagrams/list/${projectId}`, {
        method: "GET",
    }).then(response => response.json())
}

export const listDiagramText = async(projectId) => {
    return await fetch(`${API_URL}/diagramtext/list/${projectId}`, {
        method: "GET",
    }).then(response => response.json())
}

export const getDiagram = async (diagramId) => {
    return await fetch(`${API_URL}/diagrams/get/${diagramId}`, {
        method: "GET",
    }).then(response => response.json())
}
export const getDiagramText = async(diagramId) =>{
    return await fetch(`${API_URL}/diagramtext/get/${diagramId}`, {
        method: "GET",
    }).then(response => response.json())
}
export const updateDiagram = async (data, diagramId) => {
    return await fetch(`${API_URL}/diagrams/update/${diagramId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'name': String(data.name),
            'description': String(data.description),
            'xml': String(data.xml),
            'svg': String(data.svg),
            'json_user_histories': data.json_user_histories

        })
    }).then(response => response.json())
}

export const deleteDiagram = async (diagramId) => {
    return await fetch(`${API_URL}/diagrams/delete/${diagramId}`, {
        method: "DELETE",
    })
}

export const deleteDiagramText = async (diagramId) => {
    return await fetch(`${API_URL}/diagramtext/delete/${diagramId}`, {
        method: "DELETE",
    })
}