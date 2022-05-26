import React, { useState, useEffect } from "react";
import PatientsService from "../../services/PatientsService";
import {useParams} from "react-router-dom"
import './AddPatients.css';

const Patient = (props) => {
  const initialPatientState = {
    id: null,
    name: "",
    PESEL: "",
  };
  const {id} = useParams()
  const [currentPatient, setCurrentPatient] = useState(initialPatientState);
  const [message, setMessage] = useState("");

  const getPatient = () => {
    PatientsService.get(id)
        .then(response => {
          console.log(response.data);
          setCurrentPatient(response.data);
        })
        .catch(e => {
          console.log(e);
        });
  };

  useEffect(() => {
    getPatient();
  }, []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setCurrentPatient({ ...currentPatient, [name]: value });
  };

// Maybe, we have to consider it in later version
//   const updateActive = status => {
//     let data = {
//       id: currentPatient.id,
//       name: currentPatient.name,
//       PESEL: currentPatient.PESEL,
//     };
//
//     PatientsService.update(currentPatient.id, data)
//         .then(response => {
//           currentPatient({ ...currentPatient, active: status });
//           console.log(response.data);
//           setMessage("The status was updated successfully!");
//         })
//         .catch(e => {
//           console.log(e);
//         });
//   };

  const updatePatient = (e) => {
//   this prevents norma behavior of form on submit
    e.preventDefault();

    PatientsService.update(id, currentPatient)
        .then(response => {
//        TODO: Chciales tutaj andrzeju wrzucic redirecta na liste pokoi (i chyba mozna wywalic ten message ale to jak juz chcesz)
          setMessage("The patient was updated successfully!");
        })
        .catch(e => {
          console.log(e);
        });
  };

  return (
      <div>
            <div className="edit-form">
              <form onSubmit={updatePatient}>
                <div className="form-group">
                  <label htmlFor="name">Edytuj imie i nazwisko pacjenta</label>
                  <input
                      type="text"
                      className="form-control"
                      id="name"
                      required
                      name="name"
                      value={currentPatient.name}
                      onChange={handleInputChange}
                  />
                  <label htmlFor="name">Edytuj pesel pacjenta</label>
                  <input
                      type="text"
                      className="form-control"
                      id="name"
                      minLength="11"
                      maxLength="11"
                      required
                      name="PESEL"
                      value={currentPatient.PESEL}
                      onChange={handleInputChange}
                  />
                </div>
                <button type="submit" className="btn btn-success"> Zapisz </button>
              </form>
              <p>{message}</p>
            </div>
      </div>
  );
};

export default Patient;