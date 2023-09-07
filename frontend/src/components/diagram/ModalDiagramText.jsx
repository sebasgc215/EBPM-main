import React from 'react';
import { useEffect, useState } from "react";

function ModalDiagramText(props) {
    const [userStories,setUserStories] = useState(
        []
    );

    const [id_us, setID] =useState("");
    const [name_us, setName] =useState("");
    const [dependencies, setDependencies] =useState("");
    const [points, setPoints] =useState("");

    const handleName = (event) => {
        setName(event.target.value)
    }

    const handleId = (event) => {
        console.log(event.target.value)
        setID(event.target.value)
    }

    const handleDependencies = (event) => {
        setDependencies(event.target.value)
    }

    const handlePoint = (event) => {
        setPoints(event.target.value)
    }

    const addUS = (event) =>{
        event.preventDefault()
        const usObject = {
            id_us: id_us,
            name_us: name_us,
            dependencies: dependencies,
            points: points
        }
        if (Array.isArray(userStories)) {
            setUserStories([...userStories, usObject]);
        } else {
            setUserStories([usObject]); // Si no es un arreglo, crea uno nuevo con el nuevo objeto
        }

        setDependencies("")
        setID("")
        setName("")
        setPoints("")
        alert(`${name_us} is already added to Backlog`)
        
    }

    useEffect(() => {
        console.log(userStories); // Realiza el console.log aquí
    }, [userStories]);
    
    return (
        <div className="modal fade" id="modalDiagramText" aria-labelledby="tittleModalDiagram" aria-hidden="true">
            <div className="modal-dialog modal-dialog-centered">
                <div className="modal-content bg-two border-0">
                    <div className="modal-header bg-one">
                        <h5 className="modal-title text-white" id="tittleModalDiagram">{props.mode} Diagram via Text</h5>
                        <button type="button" className="btn-one px-1" data-bs-dismiss="modal" aria-label="Close">
                            <i className="bi bi-x-lg"></i>
                        </button>
                    </div>
                    <form onSubmit={addUS}>
                        <div className="modal-body">
                        
                        <div className="mb-3">
                                <label className="form-label">Id historia de usuario:</label>
                                <input className="form-control" name='id_us' onChange={handleId} />
                                
                            </div>
                            <div className="mb-3">
                                <label className="form-label">Nombre historia de usuario:</label>
                                <input className="form-control" name='name_us'  onChange={handleName} />
                                
                            </div>
                            <div className="mb-3">
                                <label className="form-label">Dependencias de la historia:</label>
                                <input className="form-control" name='dependencies'  onChange={handleDependencies} />
                                
                            </div>
                            <div className="mb-3">
                                <label className="form-label">Puntos de estimación:</label>
                                <input className="form-control" name='points'  onChange={handlePoint} />
                                <button  type="submit" className="btn-one py-2 m-2" >
                                    <i className="bi bi-plus-lg"></i> Agregar
                                </button>
                            </div>
                            <div>
                                <label className="form-label">Product Backlog:</label>
                                <ul>
                                 {Array.isArray(userStories) ? (
                                         userStories.map((story) => (
                                         <li key={story.id}>
                                               {story.name_us}
                                         </li>
                                         ))
                                 ) : null}
                                </ul>
                            </div>
                        </div>
                        <div className="modal-footer border-0">
                            <button type="button" className="btn-two shadow-lg py-1" data-bs-dismiss="modal">Close</button>
                            {props.mode === 'Create' ?
                                <button type="submit" className="btn-one shadow-lg py-1" data-bs-dismiss="modal">Create</button> :
                                null
                            }
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default ModalDiagramText;