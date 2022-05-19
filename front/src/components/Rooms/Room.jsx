import React, { useState, useEffect } from "react";
import RoomService from "../../services/RoomService";
import {useParams} from "react-router-dom"
import './AddRoom.css';

const Room = (props) => {
  const initialRoomState = {
    id: null,
    room_number: 0,
  };
  const {id} = useParams()
  const [currentRoom, setCurrentRoom] = useState(initialRoomState);
  const [message, setMessage] = useState("");

  const getRoom = () => {
    RoomService.get(id)
        .then(response => {
          setCurrentRoom(response.data);
        })
        .catch(e => {
          console.log(e);
        });
  };

  useEffect(() => {
    getRoom();
  }, []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setCurrentRoom({ ...currentRoom, [name]: value });
  };

// Maybe, we have to consider it in later version
//   const updateActive = status => {
//     let data = {
//       id: currentRoom.id,
//       room_number: currentRoom.room_number,
//     };
//
//     RoomService.update(currentRoom.id, data)
//         .then(response => {
//           setCurrentRoom({ ...currentRoom, active: status });
//           console.log(response.data);
//           setMessage("The status was updated successfully!");
//         })
//         .catch(e => {
//           console.log(e);
//         });
//   };

  const updateRoom = () => {
    RoomService.update(id, currentRoom)
        .then(response => {
//        TODO: Chciales tutaj andrzeju wrzucic redirecta na liste pokoi (i chyba mozna wywalic ten message ale to jak juz chcesz)
          setMessage("The room was updated successfully!");
        })
        .catch(e => {
          console.log(e);
        });
  };

  return (
      <div>
{/*        This has to be so deeep in because submit button goes crazy otherwise*/}
            <div className="edit-form">
              <form>
                <div className="form-group">
                  <label htmlFor="name">Edytuj numer pokoju</label>
                  <input
                      type="text"
                      className="form-control"
                      id="name"
                      required
                      name="room_number"
                      value={currentRoom.room_number}
                      onChange={handleInputChange}
                  />
                </div>
              </form>

              <button
                  type="submit"
                  className="btn btn-success"
                  onClick={updateRoom}
              >
                Zapisz
              </button>
              <p>{message}</p>
            </div>
      </div>
  );
};

export default Room;