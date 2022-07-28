import React, {useState} from "react";
import OperationService from "../../services/OperationService";

const AddOperation = () => {
    const initialOperationtState = {
        type: 0,
        medic: 0,
        patient: 0,
        date: "",
        room: 0,
        start: "",
        done: 0,
    };

    const [operation, setOperation] = useState(initialOperationtState);
    const [submitted, setSubmitted] = useState(false);

    const handleInputChange = event => {
        const {name, value} = event.target;
        setOperation({...operation, [name]: value});
    };

    const saveOperation = (e) => {
//   this prevents normal behavior of form on submit
        e.preventDefault();

        let data = {
            type: operation.type,
            medic: operation.medic,
            patient: operation.patient,
            date: operation.date,
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
                    <form onSubmit={saveOperation}>
                        <div className="form-group form_style ">
                            <label htmlFor="type">Typ operacji</label>
                            <input
                                type="number"
                                className="form-control"
                                id="type"
                                required
                                value={operation.type}
                                onChange={handleInputChange}
                                name="type"
                            />
                            <label htmlFor="medic">Lekarz</label>
                            <input
                                type="number"
                                className="form-control"
                                id="medic"
                                required
                                value={operation.medic}
                                onChange={handleInputChange}
                                name="medic"
                            />
                            <label htmlFor="patient">Pacjent</label>
                            <input
                                type="number"
                                className="form-control"
                                id="patient"
                                required
                                value={operation.patient}
                                onChange={handleInputChange}
                                name="patient"
                            />
                            <label htmlFor="date">Data</label>
                            <input
                                type="date"
                                className="form-control"
                                id="date"
                                required
                                value={operation.date}
                                onChange={handleInputChange}
                                name="date"
                            />
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
                            <label htmlFor="done">Zakończona</label>
                            <input
                                type="checkbox"
                                className="form-control"
                                id="done"
                                required
                                value={operation.done}
                                onChange={handleInputChange}
                                name="done"
                            />
                        </div>
                        <button type="submit" className="btn btn-success"> Zapisz</button>
                    </form>
                </div>
            )}
        </div>
    );
};

export default AddOperation;