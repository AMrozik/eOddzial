import React, { useState, useEffect } from "react";
import OperationService from "../../services/OperationService";
import HintingAlgService from "../../services/HintingAlgService";
import TypesService from "../../services/TypesService";
import MedicsService from "../../services/MedicsService";
import PatientsService from "../../services/PatientsService";
import RoomsService from "../../services/RoomsService";
import {useParams} from "react-router-dom"


const Operations = (props) => {
    const initialOperationState = {
        id: null,
        type: "",
        medic: "",
        patient: "",
        date: "",
        room: "",
        start: "",
        done: "",
    };
    const {id} = useParams()
    const [currentOperation, setCurrentOperation] = useState(initialOperationState);
    const [message, setMessage] = useState("");
    console.log(currentOperation);

    const getOperation = () => {
        OperationService.get(id)
            .then(response => {
            setCurrentOperation(response.data);
            })
            .catch(e => {
            console.log(e);
            });
    };

    useEffect(() => {
        getOperation();
    }, []);

    const handleInputChange = event => {
        const { name, value } = event.target;
        setCurrentOperation({ ...currentOperation, [name]: value });
    };

    const updateOperation = (e) => {
        e.preventDefault();

        OperationService.update(id, currentOperation)
            .then(response => {
            setMessage("The operation was updated successfully!");
            })
            .catch(e => {
            console.log(e);
            });
    };
    const changeDone = (e) => {
      e.preventDefault();

      currentOperation.done ? (currentOperation.done = false):(currentOperation.done = true);
      setCurrentOperation({...currentOperation});
    }

    const check_done = () => {
      if (currentOperation.done) {
        return "Tak"
      }else {
        return "Nie"
      }
    }

    return (
        <div className="submit-form form_style">
                <div className="edit-form form_style">
                  <form onSubmit={updateOperation}>
                    <div className="form-group">
                    <label htmlFor="name">Edytuj typ operacji</label>
                    <input
                        type="text"
                        className="form-control"
                        id="type"
                        required
                        value={currentOperation.type}
                        onChange={handleInputChange}
                        name="type"
                    />
                      <br/>
                    <label htmlFor="name">Lekarz</label>
                    <input
                        type="text"
                        className="form-control"
                        id="medic"
                        required
                        value={currentOperation.medic}
                        onChange={handleInputChange}
                        name="medic"
                    />
                      <br/>
                    <label htmlFor="name">Pacjent</label>
                    <input
                        type="text"
                        className="form-control"
                        id="patient"
                        required
                        value={currentOperation.patient}
                        onChange={handleInputChange}
                        name="patient"
                    />
                      <br/>
                    <label htmlFor="name">Pokój</label>
                    <input
                        type="number"
                        className="form-control"
                        id="room"
                        required
                        value={currentOperation.room}
                        onChange={handleInputChange}
                        name="room"
                    />
                      <br/>
                    <label htmlFor="name">Czas ropoczęcia operacji</label>
                    <input
                        type="time"
                        className="form-control"
                        id="start"
                        required
                        value={currentOperation.start}
                        onChange={handleInputChange}
                        name="start"
                    />
                    <br/>
                        <label htmlFor="name">Czy operacja jest zakończona</label>
                        <button className="btn btn-primary" onClick={changeDone}>{check_done()}</button>
                    <br/><br/>
                    </div>
                    <button type="submit" className="btn btn-success"> Zapisz </button>
                  </form>
                  <p>{message}</p>
                </div>
          </div>
      );
    };

export default Operations;