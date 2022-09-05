import React, { useState, useEffect } from "react";
import RoomsBreaksService from "../../../services/RoomsBreaksService";
import {useParams} from "react-router-dom"

const RoomBreak = (props) => {
  const initialRoomBreakState = {
    id: null,
    date_start: "",
    date_end: ""
  };
  const initialTimeState = {
    date_start: "",
    time_start: "",
    date_end: "",
    time_end: "",
  };
  const {id} = useParams()
  const [currentRoomBreak, setCurrentRoomBreak] = useState(initialRoomBreakState);
  const [time, setTime] = useState(initialTimeState);
  const [message, setMessage] = useState("");

  const getRoomBreak = () => {
    RoomsBreaksService.get(id)
        .then(response => {
          setCurrentRoomBreak(response.data);
          var date_start = response.data["date_start"];
          var date_end = response.data["date_end"];
          let tempTimeState = {
            date_start: date_start.slice(0,10),
            time_start: date_start.slice(11,16),
            date_end: date_end.slice(0,10),
            time_end: date_end.slice(11,16)
          };
          setTime(tempTimeState);
        })
        .catch(e => {
          console.log(e);
        });
  };

  useEffect(() => {
    getRoomBreak();
  }, []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setTime({ ...time, [name]: value });
  };

  const updateRoomBreak = () => {
    var date_start = new Date(currentRoomBreak.date_start);
    date_start.setDate(time.date_start.slice(8,10));
    date_start.setMonth(time.date_start.slice(5,7)-1);
    date_start.setFullYear(time.date_start.slice(0,4));
    date_start.setHours(time.time_start.slice(0,2));
    date_start.setMinutes(time.time_start.slice(3,5));

    var date_end = new Date(currentRoomBreak.date_end);
    date_end.setDate(time.date_end.slice(8,10));
    date_end.setMonth(time.date_end.slice(5,7)-1);
    date_end.setFullYear(time.date_end.slice(0,4));
    date_end.setHours(time.time_end.slice(0,2));
    date_end.setMinutes(time.time_end.slice(3,5));

    let data = {
        id: currentRoomBreak.id,
        room: currentRoomBreak.room,
        date_start: date_start.toISOString(),
        date_end: date_end.toISOString()
    };
//     console.log(data)

    RoomsBreaksService.update(id, data)
        .then(response => {
          setMessage("Zaktualizowano");
        })
        .catch(e => {
          console.log(e);
        });
  };

  return (
      <div class="submit-form form_style">
{/*        This has to be so deeep in because submit button goes crazy otherwise*/}
            <div className="submit-form form_style">
              <form>
                <div className="form-group">
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
                    <br/>
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
              </form>

              <button
                  type="submit"
                  className="btn btn-success"
                  onClick={updateRoomBreak}
              >
                Zapisz
              </button>
              <p>{message}</p>
            </div>
      </div>
  );
};

export default RoomBreak;