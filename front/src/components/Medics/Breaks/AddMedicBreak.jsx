import React, { useState } from "react";
import MedicsBreaksService from "../../../services/MedicsBreaksService";
import {useParams} from "react-router-dom"

const AddMedicBreak = () => {
  const initialMedicBreakState = {
    medic: null,
    date_start: null,
    date_end: null
  };
  const initialTimeState = {
    date_start: "",
    time_start: "",
    date_end: "",
    time_end: "",
  };
  const {id} = useParams();
  const [medicBreak, setMedicBreak] = useState(initialMedicBreakState);
  const [time, setTime] = useState(initialTimeState);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setTime({ ...time, [name]: value });
  };

  const saveMedicBreak = (e) => {
//   this prevents normal behavior of form on submit
    e.preventDefault();
    var date_start = new Date(time.date_start +"T"+time.time_start);
    var date_end = new Date(time.date_end +"T"+ time.time_end);

    let data = {
        medic: id,
        date_start: date_start.toISOString(),
        date_end: date_end.toISOString()
    };

    MedicsBreaksService.create(data)
        .then(response => {
          setMedicBreak({
            medic: response.data.medic,
            date_start: response.data.date_start,
            date_end: response.data.date_end
          });
          setSubmitted(true);
        })
        .catch(e => {
          console.log(e);
        });
  };

  const newMedicBreak = () => {
    setMedicBreak(initialMedicBreakState);
    setSubmitted(false);
  };

  return (
      <div className="submit-form form_style">
        {submitted ? (
            <div className="form_style">
              <h4>Zapisano nowy urlop lekarza</h4>
              <button className="btn btn-success" onClick={newMedicBreak}> Dodaj </button>
            </div>
        ) : (
            <div>
                <form onSubmit={saveMedicBreak}>
                  <div className="form-group form_style ">
                    <label htmlFor="name">Początek</label>
                    <input
                        type="date"
                        className="form-control"
                        id="name"
                        required
                        value={time.date_start}
                        onChange={handleInputChange}
                        name="date_start"
                    />
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={time.time_start}
                        onChange={handleInputChange}
                        name="time_start"
                    />
                    <label htmlFor="name">Koniec</label>
                    <input
                        type="date"
                        className="form-control"
                        id="name"
                        required
                        value={time.date_end}
                        onChange={handleInputChange}
                        name="date_end"
                    />
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={time.time_end}
                        onChange={handleInputChange}
                        name="time_end"
                    />
                  </div>

                  <button className="btn btn-success"> Zapisz </button>
              </form>
            </div>
        )}
      </div>
  );
};

export default AddMedicBreak;