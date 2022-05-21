import React, { useState } from "react";
import RoomService from "../../services/RoomService";
import './AddRoom.css';

const AddRoom = () => {
  const initialRoomState = {
    room_number: ""
  };
  const [room, setRoom] = useState(initialRoomState);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setRoom({ ...room, [name]: value });
  };

  const saveRoom = () => {
    let data = {
      room_number: room.room_number
    };

    RoomService.create(data)
        .then(response => {
          setRoom({
            room_number: response.data.room_number
          });
          setSubmitted(true);
        })
        .catch(e => {
          console.log(e);
        });
  };

  const newRoom = () => {
    setRoom(initialRoomState);
    setSubmitted(false);
  };

  return (
      <div className="submit-form form_style">
        {submitted ? (
            <div className="form_style">
              <h4>Created new room!</h4>
              <button className="btn btn-success" onClick={newRoom}>
                Dodaj
              </button>
            </div>
        ) : (
            <div>
              <div className="form-group form_style ">
                <label htmlFor="name">Numer Pokoju</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    required
                    value={room.name}
                    onChange={handleInputChange}
                    name="room_number"
                />
              </div>

              <button onClick={saveRoom} className="btn btn-success"> Zapisz </button>
            </div>
        )}
      </div>
  );
};

export default AddRoom;