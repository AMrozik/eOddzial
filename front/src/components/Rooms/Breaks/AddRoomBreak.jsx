import React, { useState } from "react";
import RoomsBreaksService from "../../../services/RoomsBreaksService";
import {useParams} from "react-router-dom"
import './AddRoomBreak.css';

const AddRoomBreak = () => {
  const initialRoomBreakState = {
    room: 0,
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
  const [roomBreak, setRoomBreak] = useState(initialRoomBreakState);
  const [time, setTime] = useState(initialTimeState);
  const [submitted, setSubmitted] = useState(false);
  console.log(time);
  console.log(roomBreak);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setTime({ ...time, [name]: value });
  };

  const saveRoomBreak = (e) => {
//   this prevents normal behavior of form on submit
    e.preventDefault();
    var date_start = new Date(time.date_start +"T"+time.time_start);
    var date_end = new Date(time.date_end +"T"+ time.time_end);

    let data = {
        room: id,
        date_start: date_start.toISOString(),
        date_end: date_end.toISOString()
    };

    RoomsBreaksService.create(data)
        .then(response => {
          setRoomBreak({
            room: response.data.room,
            date_start: response.data.date_start,
            date_end: response.data.date_end
          });
          setSubmitted(true);
        })
        .catch(e => {
          console.log(e);
        });
  };

  const newRoomBreak = () => {
    setRoomBreak(initialRoomBreakState);
    setSubmitted(false);
  };

  return (
      <div className="submit-form form_style">
        {submitted ? (
            <div className="form_style">
              <h4>Created new roomBreak!</h4>
              <button className="btn btn-success" onClick={newRoomBreak}> Dodaj </button>
            </div>
        ) : (
            <div>
                <form onSubmit={saveRoomBreak}>
                  <div className="form-group form_style ">
                    <label htmlFor="name">poczatek</label>
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
                    <label htmlFor="name">koniec</label>
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

export default AddRoomBreak;