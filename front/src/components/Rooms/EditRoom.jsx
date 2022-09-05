import React, { useState, useEffect } from "react";
import RoomsService from "../../services/RoomsService";
import {useParams} from "react-router-dom"

const Room = (props) => {
    const initialRoomState = {
        id: null,
        room_number: 0,
    };
    const {id} = useParams()
    const [currentRoom, setCurrentRoom] = useState(initialRoomState);
    const [message, setMessage] = useState("");

    const getRoom = () => {
        RoomsService.get(id)
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
        const {name, value} = event.target;
        setCurrentRoom({...currentRoom, [name]: value});
    };

    const updateRoom = () => {
        RoomsService.update(id, currentRoom)
            .then(response => {
                setMessage("The room was updated successfully!");
            })
            .catch(e => {
                console.log(e);
            });
    };

    return (
        <div>
            {/*        This has to be so deeep in because submit button goes crazy otherwise*/}
            <div className="submit-form form_style">
                <div className="form-group form_style">
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


                    <button
                        type="submit"
                        className="btn btn-success"
                        onClick={updateRoom}>
                        Zapisz
                    </button>
                </div>


                <p>{message}</p>
            </div>
        </div>
    );
};

export default Room;