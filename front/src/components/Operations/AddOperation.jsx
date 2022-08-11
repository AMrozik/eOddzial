import React, {useState, useEffect} from "react";
import {useParams} from "react-router-dom";
import OperationService from "../../services/OperationService";
import HintingAlgService from "../../services/HintingAlgService";
import TypesService from "../../services/TypesService";
import MedicsService from "../../services/MedicsService";
import PatientsService from "../../services/PatientsService";
import RoomsService from "../../services/RoomsService";

const AddOperation = () => {
    const initialOperationtState = {
        type: -1,
        medic: -1,
        patient: -1,
        date: "",
        room: -1,
        start: "",
    };

    const {date} = useParams();
    var dateToShow = new Date(date);

    const [operation, setOperation] = useState(initialOperationtState);
    const [types, setTypes] = useState();
    const [medics, setMedics] = useState();
    const [patients, setPatients] = useState();
    const [rooms, setRooms] = useState();
    const [operationHints, setOperationHints] = useState();
    const [hintIndexer, setHintIndexer] = useState(1);
    const [submitted, setSubmitted] = useState(false);
    console.log(operation);
    console.log(operationHints);
    console.log(rooms);
//     console.log((patients) ? patients[0] : "elo");

    if (operation.date === ""){
        setOperation({...operation, "date":dateToShow});
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
    };

    const getOperationHints = (e) => {
//   this prevents normal behavior of form on submit
        e.preventDefault();

//         Rooms
        RoomsService.getAll()
            .then(response => {
              setRooms(response.data);
            })
            .catch(e => {
              console.log(e);
            });

        if(operation.type !== -1 && operation.medic !== -1 && operation.patient !== -1 ){
            HintingAlgService.getDaily({
                is_child: (operation.patient.age >= 18) ? false : true,
                is_difficult: operation.type.is_difficult,
                date_year: operation.date.getFullYear(),
                date_month: operation.date.getMonth()+1,
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
        }else{
            alert("Nie wszystkie wybory zostaly dokonane!")
        }
    };

    const useDataToFillObj = (e) =>{
//   this prevents normal behavior of form on submit
        e.preventDefault();

        var roomId = -1;
        for(var i=0; i< rooms.length; i++){
            if (rooms[i].room_number === operationHints[hintIndexer].room){
                roomId = rooms[i].id;
            }
        }

        setOperation({...operation, "room": roomId, "start": operationHints[hintIndexer].start.slice(11)});
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
//             done: operation.done,
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
        setOperation(initialOperationtState);
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
                <div>
                    <form onSubmit={getOperationHints}>
                        <label htmlFor="type">Typ operacji</label>
                            <select name="type" onChange={handleTypeChange}>
                                <option value={-1} selected disabled hidden>Wybierz typ operacji</option>
                                {(types) ? types.map((element) => <option value={types.indexOf(element)}>{element.name}</option>) : <option></option> }
                            </select>
                        <label htmlFor="medic">Lekarz</label>
                            <select name="medic" onChange={handleMedicChange}>
                                <option value={-1} selected disabled hidden>Wybierz medyka</option>
                                {(medics) ? medics.map((element) => <option value={medics.indexOf(element)}>{element.name}</option>) : <option></option> }
                            </select>
                        <label htmlFor="patient">Pacjent</label>
                            <select name="patient" onChange={handlePatientChange}>
                                <option value={-1} selected disabled hidden>Wybierz pacjenta</option>
                                {(patients) ? patients.map((element) => <option value={patients.indexOf(element)}>{element.name}</option>) : <option></option> }
                            </select>
                        <input type="submit" value="Podpowiedz"/>
                    </form>
                    <hr></hr>
                    <form onSubmit={saveOperation} >
                        <div className="form-group form_style " style={{float:"left"}}>
                            <label htmlFor="room">Pokój</label>
                            <input
                                type="number"
                                className="form-control"
                                id="room"
                                required
                                value={operation.room}
                                onChange={handleInputChange}
                                name="room"
                            />
                            <label htmlFor="start">Rozpoczęcie operacji</label>
                            <input
                                type="time"
                                className="form-control"
                                id="start"
                                required
                                value={operation.start}
                                onChange={handleInputChange}
                                name="start"
                            />
                            <button type="submit" className="btn btn-success">Zapisz</button>
                        </div>
                    </form>
                    <form onSubmit={useDataToFillObj}>
                        <div className="form-group form_style " >
                            <label htmlFor="room">Pokój</label>
                            <p>{(operationHints) ? operationHints[hintIndexer].room : ""}</p>
                            <label htmlFor="start">Rozpoczęcie operacji</label>
                            <p>{(operationHints) ? operationHints[hintIndexer].start.slice(11) : ""}</p>
                            <input type="submit" value="Uzyj danych"/>
                        </div>
                    </form>
                </div>
            )}
        </div>
    );
};

export default AddOperation;