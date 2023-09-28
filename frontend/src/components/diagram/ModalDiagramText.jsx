import React from 'react';
import {  useState } from "react";
import * as DiagramService from "../../service/DiagramService"

function ModalDiagramText(props) {
    const [userStories,setUserStories] = useState(
        []
    );
    const [title, setTitle] = useState("");
    const [id_us, setID] =useState("");
    const [name_us, setName] =useState("");
    const [dependencies, setDependencies] =useState("");
    const [points, setPoints] =useState("");
    const [priority, setPriority] = useState("");
    const [purpose, setPurpose] = useState("");
    const [developer, setDeveloper] = useState("");
    const [contentPriority] = useState(['Very low', 'Low', 'Medium', 'High', 'Very high']);
    const [contentPoints] = useState([1, 2, 3, 5, 8, 13, 21]);
    const handlePriority = (event) =>{
        setPriority(event.target.value)
    }
    const handlePurpose = (event) =>{
        setPurpose(event.target.value)
    }
    const handleDeveloper = (event) =>{
        setDeveloper(event.target.value)
    }
    
    const handleTitle = (event) =>{
        setTitle(event.target.value)
    }
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
        console.log(points)
    }

    const addUS = (event) =>{
        event.preventDefault()        
        const usObject = {
            id_us: id_us,
            name_us: name_us,
            dependencies: dependencies,
            points: points,
            developer: developer,
            purpose: purpose,
            priority: priority,
        }
        setUserStories([...userStories, usObject]);

        alert(`${name_us} is already added to Backlog`)
        setDependencies("")
        setID("")
        setName("")
        setPoints("")
        console.log(props.projectId)
    }

    const createTextDiagram = async (e) => {
        e.preventDefault();
        try {
          if (userStories.length === 0) {
            alert("Debes agregar al menos una historia de usuario.");
            return;
          }
        const data = {
            "name": title,
            "json_user_stories": JSON.stringify(userStories),
            "id_project": props.projectId
        }
        
          const diagram = await DiagramService.createTextDiagram(data);
          alert(`${title} is already added to the Project`);
        } catch (error) {
          console.log(error);
        }
      };
      
    

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
                    <form onSubmit={createTextDiagram}>
                        <div className="modal-body">
                            <div className="mb-3">
                                        <label className="form-label">Diagram title:</label>
                                        <input className="form-control" name='diagram_us' onChange={handleTitle} />
                                    </div>

                                <div className="mb-3">
                                        <label className="form-label">User Story ID:</label>
                                        <input className="form-control" name='id_us' onChange={handleId} />
                                        
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">User Story Name:</label>
                                        <input className="form-control" name='name_us'  onChange={handleName} />
                                        
                                    </div>
                                    <div className="mb-3">
                                        <label className="form-label">Dependencies:</label>
                                        <input className="form-control" name='dependencies'  onChange={handleDependencies} />
                                        
                                    </div>
                                    <div className='d-flex pb-3'>
                                <div className="w-33 me-2">
                                    <label className="form-label">Priority:</label>
                                    <select className="form-select" name='uh:priority' onChange={handlePriority} >
                                        {
                                            contentPriority.map((element, i) => <option key={i} value={`${element}`}>{element}</option>)
                                        }
                                    </select>
                                </div>
                                <div className="w-33 ms-2 me-2">
                                    <label className="form-label">Points:</label>
                                    <select className="form-select" name='uh:points' onChange={handlePoint}>
                                        {
                                            contentPoints.map((element, i) => <option key={i} value={`${element}`}>{element}</option>)
                                        }
                                    </select>
                                </div>
                            </div>
                                        <div className="pb-3 mb-3">
                                        <label className="form-label">Developer:</label>
                                        <input className="form-control" name='uh:developer'  onChange={handleDeveloper}/>
                                    </div>
                                    <div className="pb-3 mb-3">
                                        <label className="form-label">Purpose:</label>
                                        <textarea className="form-control" rows="3" name='uh:purpose' onChange={handlePurpose}></textarea>
                                    </div> 
                                    <button  type="submit" className="btn-one py-2 m-2" onClick={addUS}>
                                    <i className="bi bi-plus-lg"></i> Add US
                                </button>
                                    <div>
                                        <label className="form-label">Product Backlog:</label>
                                        <ul>
                                        {Array.isArray(userStories) ? (
                                                userStories.map((story, i) => (
                                                <li key={i}>
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
                                        <button type="submit" className="btn-one shadow-lg py-1" data-bs-dismiss="modal" >Create</button> :
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