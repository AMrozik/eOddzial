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
  },
//   Nie mam pojecia co to jest! ale [] trzeba zostawic bo inaczej mamy refresh loop
//   [props.match.params.id]
  []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setCurrentRoom({ ...currentRoom, [name]: value });
  };

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
          console.log(response.data);
//        Redirect/Link na "/rooms/"
          setMessage("The room was updated successfully!");
        })
        .catch(e => {
          console.log(e);
        });
  };

//   const deleteRoom = () => {
//     RoomService.remove(currentRoom.id)
//         .then(response => {
//           console.log(response.data);
//           props.history.push("/rooms");
//         })
//         .catch(e => {
//           console.log(e);
//         });
//   };

  return (
      <div>
{/*        {currentRoom ? ( */}
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

{/*               <button className="badge badge-danger mr-2" onClick={deleteRoom}> */}
{/*                 Delete */}
{/*               </button> */}

              <button
                  type="submit"
                  className="btn btn-success"
                  onClick={updateRoom}
              >
                Zapisz
              </button>
              <p>{message}</p>
            </div>
{/*         ) : ( */}
{/*             <div> */}
{/*               <br /> */}
{/*               <p>Please click on a Room...</p> */}
{/*             </div> */}
{/*         )} */}
      </div>
  );
};

export default Room;