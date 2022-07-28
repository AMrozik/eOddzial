import React, { useState } from "react";
import PatientsService from "../../services/PatientsService";


const AddPatient = () => {
  const initialPatientState = {
    name: "",
    PESEL: ""
  };
  const [patient, setPatient] = useState(initialPatientState);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setPatient({ ...patient, [name]: value });
  };

  const savePatient = (e) => {
//   this prevents normal behavior of form on submit
    e.preventDefault();

    let data = {
      name: patient.name,
      PESEL: patient.PESEL
    };

    PatientsService.create(data)
        .then(response => {
          setPatient({
            name: response.data.name,
            PESEL: response.data.PESEL
          });
          setSubmitted(true);
        })
        .catch(e => {
          console.log(e);
        });
  };

  const newPatient = () => {
    setPatient(initialPatientState);
    setSubmitted(false);
  };

  return (
      <div className="submit-form form_style">
        {submitted ? (
            <div className="form_style">
              <h4>Pomyślne utworzono pacjenta!</h4>
              <button className="btn btn-success" onClick={newPatient}> Dodaj </button>
            </div>
        ) : (
            <div>
            <form onSubmit={savePatient}>
              <div className="form-group form_style ">
                <label htmlFor="name">Imie i nazwisko pacjenta</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    required
                    value={patient.name}
                    onChange={handleInputChange}
                    name="name"
                />
                <label htmlFor="name">Pesel pacjenta</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    minLength="11"
                    maxLength="11"
                    required
                    value={patient.PESEL}
                    onChange={handleInputChange}
                    name="PESEL"
                />
              </div>
              <button type="submit" className="btn btn-success"> Zapisz </button>
            </form>
            </div>
        )}
      </div>
  );
};

export default AddPatient;