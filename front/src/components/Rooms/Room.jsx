import React, { useState, useEffect } from "react";
import RoomService from "../../services/RoomService";

const Room = props => {
  const initialRoomState = {
    id: null,
    room_number: 0,
  };
  const [currentRoom, setCurrentRoom] = useState(initialRoomState);
  const [message, setMessage] = useState("");

  const getRoom = id => {
    RoomService.get(id)
        .then(response => {
          setCurrentRoom(response.data);
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
  };

  useEffect(() => {
    getRoom(props.match.params.id);
  }, [props.match.params.id]);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setCurrentRoom({ ...currentRoom, [room_number]: value });
  };

  const updateActive = status => {
    let data = {
      id: currentRoom.id,
      room_number: currentRoom.room_number,
    };

    RoomService.update(currentRoom.id, data)
        .then(response => {
          setCurrentRoom({ ...currentRoom, active: status });
          console.log(response.data);
          setMessage("The status was updated successfully!");
        })
        .catch(e => {
          console.log(e);
        });
  };

  const updateRoom = () => {
    RoomService.update(currentRoom.id, currentRoom)
        .then(response => {
          console.log(response.data);
          setMessage("The room was updated successfully!");
        })
        .catch(e => {
          console.log(e);
        });
  };

  const deleteRoom = () => {
    RoomService.remove(currentRoom.id)
        .then(response => {
          console.log(response.data);
          props.history.push("/rooms");
        })
        .catch(e => {
          console.log(e);
        });
  };

  return (
      <div>
        {currentRoom ? (
            <div className="edit-form">
              <h4>Tutorial</h4>
              <form>
                <div className="form-group">
                  <label htmlFor="name">Name</label>
                  <input
                      type="text"
                      className="form-control"
                      id="name"
                      name="name"
                      value={currentRoom.room_number}
                      onChange={handleInputChange}
                  />
                </div>
              </form>

              <button className="badge badge-danger mr-2" onClick={deleteRoom}>
                Delete
              </button>

              <button
                  type="submit"
                  className="badge badge-success"
                  onClick={updateRoom}
              >
                Update
              </button>
              <p>{message}</p>
            </div>
        ) : (
            <div>
              <br />
              <p>Please click on a Room...</p>
            </div>
        )}
      </div>
  );
};

export default Room;