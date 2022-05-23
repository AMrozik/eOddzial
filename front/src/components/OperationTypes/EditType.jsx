import React, { useState, useEffect } from "react";
import TypesService from "../../services/TypesService";
import {useParams} from "react-router-dom"
import './AddTypes.css';

const Type = (props) => {
  const initialTypeState = {
    id: null,
    name: "",
    ICD_code: "",
    cost: "",
    is_difficult: "",
    duration: "",
  };
  const {id} = useParams()
  const [currentType, setCurrentType] = useState(initialTypeState);
  const [difficulty, setDifficulty] = useState(false);
  const [message, setMessage] = useState("");

  const getType = () => {
    TypesService.get(id)
        .then(response => {
          setCurrentType(response.data);
        })
        .catch(e => {
          console.log(e);
        });
  };

  useEffect(() => {
    getType();
  }, []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setCurrentType({ ...currentType, [name]: value });
  };

// Maybe, we have to consider it in later version
//   const updateActive = status => {
//     let data = {
//       id: currentType.id,
//       room_number: currentType.room_number,
//     };
//
//     RoomService.update(currentType.id, data)
//         .then(response => {
//           currentType({ ...currentType, active: status });
//           console.log(response.data);
//           setMessage("The status was updated successfully!");
//         })
//         .catch(e => {
//           console.log(e);
//         });
//   };

  const updateType = (e) => {
//   this prevents norma behavior of form on submit
    e.preventDefault();

    TypesService.update(id, currentType)
        .then(response => {
//        TODO: Chciales tutaj andrzeju wrzucic redirecta na liste pokoi (i chyba mozna wywalic ten message ale to jak juz chcesz)
          setMessage("The type was updated successfully!");
        })
        .catch(e => {
          console.log(e);
        });
  };

  const changeDifficulty = (e) => {
//   this is for button on button delete -> cascade
    e.preventDefault();

    currentType.is_difficult ? (currentType.is_difficult = false):( currentType.is_difficult = true);
    setCurrentType({ ...currentType});
  }

  return (
      <div>
            <div className="edit-form">
              <form onSubmit={updateType}>
                <div className="form-group">
                <label htmlFor="name">Nazwa typu</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    required
                    value={currentType.name}
                    onChange={handleInputChange}
                    name="name"
                />
                <label htmlFor="name">Kod ICD</label>
                <input
                    type="text"
                    className="form-control"
                    id="ICD_code"
                    required
                    value={currentType.ICD_code}
                    onChange={handleInputChange}
                    name="ICD_code"
                />
                <label htmlFor="name">Koszt</label>
                <input
                    type="number"
                    className="form-control"
                    id="cost"
                    required
                    value={currentType.cost}
                    onChange={handleInputChange}
                    name="cost"
                />
                <label htmlFor="name">Czy operacja jest trudna</label>
                <p id="difficulty" onClick={changeDifficulty}>{currentType.is_difficult.toString()}</p>
                <button onClick={changeDifficulty}>Change</button>
                <label htmlFor="name">Czas trwania</label>
                <input
                    type="text"
                    className="form-control"
                    id="duration"
                    required
                    value={currentType.duration}
                    onChange={handleInputChange}
                    name="duration"
                />
                </div>
                <button type="submit" className="btn btn-success"> Zapisz </button>
              </form>
              <p>{message}</p>
            </div>
      </div>
  );
};

export default Type;