import React, {useState, useEffect} from "react";
import {useParams} from "react-router-dom";
import OperationService from "../../services/OperationService";
import HintingAlgService from "../../services/HintingAlgService";
import TypesService from "../../services/TypesService";
import MedicsService from "../../services/MedicsService";
import PatientsService from "../../services/PatientsService";
import RoomsService from "../../services/RoomsService";

const AddOperation = () => {
    const initialOperationState = {
        type: -1,
        medic: -1,
        patient: -1,
        date: "",
        room: -1,
        start: "",
    };

    const {date} = useParams();
    var dateToShow = new Date(date);

    const [operation, setOperation] = useState(initialOperationState);
    const [types, setTypes] = useState();
    const [medics, setMedics] = useState();
    const [patients, setPatients] = useState();
    const [rooms, setRooms] = useState();
    const [roomIndex, setRoomIndex] = useState();
    const [operationHints, setOperationHints] = useState();
    const [hintIndexer, setHintIndexer] = useState(1);
    const [submitted, setSubmitted] = useState(false);
//     console.log(operation);
//     console.log(operationHints);
//     console.log(rooms);
//     console.log(roomIndex);
//     console.log((patients) ? patients[0] : "elo");

    if (operation.date === "") {
        setOperation({...operation, "date": dateToShow});
    }

    const getSelectable = () => {
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

//         Rooms
        RoomsService.getAll()
            .then(response => {
                setRooms(response.data);
            })
            .catch(e => {
                console.log(e);
            });
    };

    const getOperationHints = (e) => {
//   this prevents normal behavior of form on submit
        e.preventDefault();

        if (operation.type !== -1 && operation.medic !== -1 && operation.patient !== -1) {
            HintingAlgService.getDaily({
                is_child: (operation.patient.age >= 18) ? false : true,
                is_difficult: operation.type.is_difficult,
                date_year: operation.date.getFullYear(),
                date_month: operation.date.getMonth() + 1,
                date_day: operation.date.getDate(),
                type_ICD: operation.type.ICD_code,
                medic_id: operation.medic.id
            })
                .then(response => {
                    setOperationHints(response.data);
                    setHintIndexer(0);
                })
                .catch(e => {
                    console.log(e);
                });
        } else {
            alert("Nie wszystkie wybory zostaly dokonane!")
        }
    };

    const useDataToFillObj = (e) => {
//   this prevents normal behavior of form on submit
        e.preventDefault();

        var roomId = getRoomID(operationHints[hintIndexer].room);

        setOperation({...operation, "room": roomId, "start": operationHints[hintIndexer].start.slice(11)});
        setRoomIndex(getRoomIndex(operationHints[hintIndexer].room));
    }

    useEffect(() => {
        getSelectable();
    }, []);

    const handleInputChange = event => {
        const {name, value} = event.target;
        setOperation({...operation, [name]: value});
    };

    const handleTypeChange = event => {
        const {name, value} = event.target;
        setOperation({...operation, [name]: types[value]});
    };

    const handleMedicChange = event => {
        const {name, value} = event.target;
        setOperation({...operation, [name]: medics[value]});
    };

    const handlePatientChange = event => {
        const {name, value} = event.target;
        setOperation({...operation, [name]: patients[value]});
    };

    const handleRoomChange = event => {
        const {name, value} = event.target;
        setRoomIndex(rooms.indexOf(rooms[value]));
        setOperation({...operation, [name]: rooms[value].id});
    };

    const getRoomID = number => {
        var id = -1;
        for (var i = 0; i < rooms.length; i++) {
            if (rooms[i].room_number === number) {
                id = rooms[i].id;
            }
        }
        return id;
    }

    const getRoomIndex = number => {
        var index = -1;
        for (var i = 0; i < rooms.length; i++) {
            if (rooms[i].room_number === number) {
                index = i;
            }
        }
        return index;
    }

    const saveOperation = (e) => {
//   this prevents normal behavior of form on submit
        e.preventDefault();

        let data = {
            type: operation.type.id,
            medic: operation.medic.id,
            patient: operation.patient.id,
            date: operation.date.toISOString().split('T')[0],
            room: operation.room,
            start: operation.start,
            done: operation.done,
        };


        OperationService.create(data)
            .then(response => {
                setOperation({
                    type: response.data.type,
                    medic: response.data.medic,
                    patient: response.data.patient,
                    date: response.data.date,
                    room: response.data.room,
                    start: response.data.start,
                    done: response.data.done,
                });
                setSubmitted(true);
            })
            .catch(e => {
                console.log(e);
            });
    };

    const newOperation = () => {
        setOperation(initialOperationState);
        setSubmitted(false);
    };

    return (
        <div className="submit-form form_style">
            {submitted ? (
                <div className="form_style">
                    <h4>Pomyślne utworzono operacje!</h4>
                    <button className="btn btn-success" onClick={newOperation}> Dodaj</button>
                </div>
            ) : (
                <div className="form-group">
                    <div>
                        <form onSubmit={getOperationHints}>
                            <label htmlFor="type">Typ operacji</label>
                            <select className="form-select" name="type" onChange={handleTypeChange}>
                                <option value={-1} selected disabled hidden>Wybierz typ operacji</option>
                                {(types) ? types.map((element) => <option
                                    value={types.indexOf(element)}>{element.name}</option>) : <option></option>}
                            </select> <br/>
                            <label htmlFor="medic">Lekarz</label>
                            <select className="form-select" name="medic" onChange={handleMedicChange}>
                                <option value={-1} selected disabled hidden>Wybierz medyka</option>
                                {(medics) ? medics.map((element) => <option
                                    value={medics.indexOf(element)}>{element.name}</option>) : <option></option>}
                            </select> <br/>
                            <label htmlFor="patient">Pacjent</label>
                            <select className="form-select" name="patient" onChange={handlePatientChange}>
                                <option value={-1} selected disabled hidden>Wybierz pacjenta</option>
                                {(patients) ? patients.map((element) => <option
                                    value={patients.indexOf(element)}>{element.name}</option>) : <option></option>}
                            </select> <br/>
                            <button className="btn btn-primary" type="submit">
                                Podpowiedź
                            </button>
                        </form>
                    </div>
                    <hr></hr>
                    <form onSubmit={saveOperation}>
                        <div className="form-group" style={{float: "left"}}>
                            <label htmlFor="room">Pokój</label>
                                <select className="form-select" name="room" value={roomIndex} onChange={handleRoomChange}>
                                    <option value={-1} selected disabled hidden>Wybierz pokój</option>
                                    {(rooms) ? rooms.map((element) => <option
                                        value={rooms.indexOf(element)}>{element.room_number}</option>) : <option></option>}
                                </select>
                                <br/>
                            <label htmlFor="start">Rozpoczęcie operacji</label>
                            <input
                                type="time"
                                className="form-control"
                                id="start"
                                required
                                value={operation.start}
                                onChange={handleInputChange}
                                name="start"/> <br/>
                            <button type="submit" className="btn btn-success">Zapisz</button>
                        </div>
                    </form>
                    <form onSubmit={useDataToFillObj}>
                        <div className="form-group">
                            <label htmlFor="room">Pokój</label><br/>
                            <p>{(operationHints) ? operationHints[hintIndexer].room : ""}</p>
                            <label htmlFor="start">Rozpoczęcie operacji</label><br/>
                            <p>{(operationHints) ? operationHints[hintIndexer].start.slice(11) : ""}</p>
                            <button className="btn btn-primary" type="submit"> Użyj danych</button>
                        </div>
                    </form>
                </div>
            )}
        </div>
    );
};

export default AddOperation;