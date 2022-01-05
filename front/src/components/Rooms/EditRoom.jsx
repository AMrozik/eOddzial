import React, { useState } from "react";
import RoomService from "../../services/RoomService";
import './AddRoom.css';

// TODO: Make edit work
const EditRoom = () => {
  const initialRoomState = {
    id: null,
    name: "",
    active: true
  };
  const [room, setRoom] = useState(initialRoomState);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setRoom({ ...room, [name]: value });
  };

  const editRoom = () => {
    let data = {
      name: room.name
    };

    RoomService.create(data)
        .then(response => {
          setRoom({
            id: response.data.id,
            name: response.data.name,
            active: response.data.active
          });
          setSubmitted(true);
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
  };

  const saveRoom = () => {
    setRoom(initialRoomState);
    setSubmitted(false);
  };

  return (
      <div className="submit-form form_style">
        {submitted ? (
            <div className="form_style">
              <h4>You submitted successfully!</h4>
              <button className="btn btn-success" onClick={saveRoom}>
                Add
              </button>
            </div>
        ) : (
            <div>
              <div className="form-group form_style ">
                <label htmlFor="name">Room Name</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    required
                    value={room.name}
                    onChange={handleInputChange}
                    name="name"
                />
              </div>

              <div className="form-group form_style ">
                <label htmlFor="name">Room Status</label>
                <input
                    type="select"
                    className="form-control"
                    id="active"
                    required
                    value={room.active}
                    onChange={handleInputChange}
                    name="active"
                />
              </div>

              <button onClick={editRoom} className="btn btn-success">
                Submit
              </button>
            </div>
        )}
      </div>
  );
};

export default EditRoom;