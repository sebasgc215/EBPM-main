import React from 'react';

function ModalDiagramText(props) {
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
                    <form onSubmit={props.createNewDiagram}>
                        <div className="modal-body">
                        <div className="mb-3">
                                <label className="form-label">Id historia de usuario:</label>
                                <input className="form-control" name='name' value={props.name} onChange={props.handle} />
                                
                            </div>
                            <div className="mb-3">
                                <label className="form-label">Nombre historia de usuario:</label>
                                <input className="form-control" name='name' value={props.name} onChange={props.handle} />
                                
                            </div>
                            <div className="mb-3">
                                <label className="form-label">Dependencias de la historia:</label>
                                <input className="form-control" name='name' value={props.name} onChange={props.handle} />
                                
                            </div>
                            <div className="mb-3">
                                <label className="form-label">Puntos de estimación:</label>
                                <input className="form-control" name='name' value={props.name} onChange={props.handle} />
                                <button className="btn-one py-2 m-2" >
                                    <i className="bi bi-plus-lg"></i> Agregar
                                </button>
                            </div>
                            <div>
                                <label className="form-label">Product Backlog:</label>
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