import React, { useState } from "react";
import PatientService from "../../services/PatientService";
import './AddPatient.css';

const AddPatient = () => {
  const initialPatientState = {
    id: null,
    name: "",
    PESEL: ""
  };

  const [patient, setPatient] = useState(initialPatientState);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setPatient({ ...patient, [name]: value });
  };

  const savePatient = () => {
    let data = {
      name: patient.name,
      PESEL: patient.PESEL
    };

    PatientService.create(data)
        .then(response => {
          setPatient({
            id: response.data.id,
            name: response.data.name,
            PESEL: response.data.PESEL
          });
          setSubmitted(true);
          console.log(response.data);
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
              <h4>You submitted successfully!</h4>
              <button className="btn btn-success" onClick={newPatient}>
                Add
              </button>
            </div>
        ) : (
            <div>
              <div className="form-group form_style ">
                <label htmlFor="name">Patient Name</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    required
                    value={patient.name}
                    onChange={handleInputChange}
                    name="name"
                />
                <label htmlFor="PESEL">PESEL</label>
                <input
                    type="text"
                    className="form-control"
                    id="PESEL"
                    required
                    value={patient.PESEL}
                    onChange={handleInputChange}
                    name="PESEL"
                />
              </div>

              <button onClick={savePatient} className="btn btn-success">
                Submit
              </button>
            </div>
        )}
      </div>
  );
};

export default AddPatient;