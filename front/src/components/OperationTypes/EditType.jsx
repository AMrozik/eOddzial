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

  const updateType = (e) => {
//   this prevents norma behavior of form on submit
    e.preventDefault();

    TypesService.update(id, currentType)
        .then(response => {
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