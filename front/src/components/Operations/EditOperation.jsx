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
    const [types, setTypes] = useState();
    const [medics, setMedics] = useState();
    const [patients, setPatients] = useState();
    const [rooms, setRooms] = useState();
    const [message, setMessage] = useState("");
    console.log(currentOperation);

    const gatherData = () => {
//     Types
        TypesService.getAll()
            .then(response => {
                setTypes(response.data);
            })
            .catch(e => {
                console.log(e);
            });
//      Medics
        MedicsService.getAll()
            .then(response => {
                setMedics(response.data);
            })
            .catch(e => {
                console.log(e);
            });
//      Patients
        PatientsService.getAll()
            .then(response => {
                setPatients(response.data);
            })
            .catch(e => {
                console.log(e);
            });

//      Rooms
        RoomsService.getAll()
            .then(response => {
                setRooms(response.data);
            })
            .catch(e => {
                console.log(e);
            });

//      Operations
        OperationService.get(id)
            .then(response => {
            setCurrentOperation(response.data);
            })
            .catch(e => {
            console.log(e);
            });
    };

    useEffect(() => {
        gatherData();
    }, []);

    const handleInputChange = event => {
        const { name, value } = event.target;
        setCurrentOperation({ ...currentOperation, [name]: value });
    };

    const handleTypeChange = event => {
        const { name, value } = event.target;
        setCurrentOperation({ ...currentOperation, [name]: types[value].id });
    };
    const handleMedicChange = event => {
        const { name, value } = event.target;
        setCurrentOperation({ ...currentOperation, [name]: medics[value].id });
    };
    const handlePatientChange = event => {
        const { name, value } = event.target;
        setCurrentOperation({ ...currentOperation, [name]: patients[value].id });
    };
    const handleRoomChange = event => {
        const { name, value } = event.target;
        setCurrentOperation({ ...currentOperation, [name]: rooms[value].id });
    };


//      Index order: Type, Medic, Patient, Room
    const getTypeIndex = (typeId) => {
        var index = -1;
        for (var i = 0; i < types.length; i++) {
            if (types[i].id === typeId) {
                index = i;
            }
        }
        return index;
    }
    const getMedicIndex = (medicId) => {
        var index = -1;
        for (var i = 0; i < medics.length; i++) {
            if (medics[i].id === medicId) {
                index = i;
            }
        }
        return index;
    }
    const getPatientIndex = (patientId) => {
        var index = -1;
        for (var i = 0; i < patients.length; i++) {
            if (patients[i].id === patientId) {
                index = i;
            }
        }
        return index;
    }
    const getRoomIndex = (roomId) => {
        var index = -1;
        for (var i = 0; i < rooms.length; i++) {
            if (rooms[i].id === roomId) {
                index = i;
            }
        }
        return index;
    }

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
                    <select className="form-select" name="type" value={(types)?getTypeIndex(currentOperation.type):-1} onChange={handleTypeChange}>
                        <option value={-1} selected disabled hidden>Wybierz typ</option>
                        {(types) ? types.map((element) => <option
                            value={types.indexOf(element)}>{element.name}</option>) : <option></option>}
                    </select> <br/>

                    <label htmlFor="name">Lekarz</label>
                    <select className="form-select" name="medic" value={(medics)?getMedicIndex(currentOperation.medic):-1} onChange={handleMedicChange}>
                        <option value={-1} selected disabled hidden>Wybierz typ</option>
                        {(medics) ? medics.map((element) => <option
                            value={medics.indexOf(element)}>{element.name}</option>) : <option></option>}
                    </select> <br/>

                    <label htmlFor="name">Pacjent</label>
                    <select className="form-select" name="patient" value={(patients)?getPatientIndex(currentOperation.patient):-1} onChange={handlePatientChange}>
                        <option value={-1} selected disabled hidden>Wybierz typ</option>
                        {(patients) ? patients.map((element) => <option
                            value={patients.indexOf(element)}>{element.name}</option>) : <option></option>}
                    </select> <br/>

                    <label htmlFor="name">Pokój</label>
                    <select className="form-select" name="room" value={(rooms)?getRoomIndex(currentOperation.room):-1} onChange={handleRoomChange}>
                        <option value={-1} selected disabled hidden>Wybierz typ</option>
                        {(rooms) ? rooms.map((element) => <option
                            value={rooms.indexOf(element)}>{element.room_number}</option>) : <option></option>}
                    </select> <br/>

                    <label htmlFor="name">Data ropoczęcia operacji</label>
                    <input
                        type="date"
                        className="form-control"
                        id="date"
                        required
                        value={currentOperation.date}
                        onChange={handleInputChange}
                        name="date"
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