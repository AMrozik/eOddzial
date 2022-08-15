import React, { useState, useEffect } from "react";
import TypesService from "../../services/TypesService";
import {useParams} from "react-router-dom"

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
          setMessage("Zaktualizowano");
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

  const check_difficulty = () => {
    if (currentType.is_difficult) {
      return "Prawda"
    }else {
      return "Fałsz"
    }
  }

  return (
      <div className="submit-form form_style">
            <div className="edit-form form_style">
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
                  <br/>
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
                  <br/>
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
                  <br/>
                <label htmlFor="name">Czy operacja jest trudna</label>
                <button className="btn btn-primary" onClick={changeDifficulty}>{check_difficulty()}</button>
                  <br/><br/>
                {/*<button onClick={changeDifficulty}>Zmień</button><br/><br/>*/}
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