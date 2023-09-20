import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { getDiagramText as getInfoDiagram,  } from '../../service/DiagramService';
import { Toast, Modal } from 'bootstrap';
import * as ProjectService from "../../service/ProjectService";
import ModalDiagramText from "./ModalDiagramText";

// Components
import NavBar from '../NavBar';
import Footer from '../Footer';

import Alert from '../Alert';


function ModelerComponentText() {
  
  const { diagramId, projectId } = useParams();
  
  const [alertMessage, setAlertMessage] = useState('');
  const [alertType, setAlertType] = useState('');
  const [refAlertElement] = useState(React.createRef());
  
const [project, setProject] = useState({});

const [diagram, setDiagram] = useState({});

  
  const getProject = async () => {
    try {
      await ProjectService.getProject(projectId).then(res => {
        setProject(res.data)
      });
    } catch (error) {
      // console.log(error)
    }
  }

  useEffect(() => {
    getProject();
  
    getInfoDiagram(diagramId)
      .then(response => {
        const data = response.data;
  
        setDiagram({
          name: data.name,
          json_user_stories: JSON.parse(data.json_user_stories),
        });
      })
      .catch(error => {
        // Manejar el error aquí
      });
  }, []);

  return (
    <div className='bg-two'>
      <NavBar />

      <div id="model_diagram">
        {/* Options diagram */}
        <div className='d-flex justify-content-between align-items-center info py-2 px-3'>
          {/* Name and edit */}
          <div className='d-flex'>
            <h4 className='mb-0'>{project.name} / {diagram.name}</h4>
            <button className='btn-transparent ms-2' data-bs-toggle="modal" data-bs-target="#modalDiagramText">
              <i className="bi bi-pencil"></i>
            </button>
          </div>
          
          <div>
            {/* Button View US */}
            
            {/* Button Save */}
            
          </div>
        </div>
        <div className="d-flex">
          <ul>
        {diagram.json_user_stories?.map((story, index) => (
          <li key={index}>
            <p>ID: {story.id_us}</p>
            <p>Name: {story.name_us}</p>
            <p>Dependencies: {story.dependencies}</p>
            <p>Points: {story.points}</p>
          </li>
        ))}
      </ul>
          </div>
        {/* Instructions 
        <div id='instructions-modeler' className='bg-one rounded shadow-lg z-index-1000 position-absolute bottom-0 start-0 m-3 p-2'>
          <p className='mb-0 text-white text-center fs-12'><strong className='text-white'>Right click (On the task)</strong> Open task properties</p>
        </div>
        */}
        

        {/* EBPM */}
        <div id="canvas"></div>
      </div>
      <Alert type={alertType} message={alertMessage} refAlertElement={refAlertElement} />
      <ModalDiagramText mode='Create' projectId={projectId} />
      <Footer></Footer>
    </div>
    
  )
}
export default ModelerComponentText;