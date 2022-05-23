import React, { useState } from "react";
import TypesService from "../../services/TypesService";
import './AddTypes.css';

const AddTypes = () => {
  const initialTypeState = {
    name: "",
    ICD_code: "",
    cost: 0,
    is_difficult: false,
    duration: "",
  };
  const [type, setType] = useState(initialTypeState);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setType({ ...type, [name]: value });
  };

  const saveType = (e) => {
//   this prevents normal behavior of form on submit
    e.preventDefault();

    let data = {
      name: type.name,
      ICD_code: type.ICD_code,
      cost: type.cost,
      is_difficult: type.is_difficult,
      duration: type.duration,
    };

    TypesService.create(data)
        .then(response => {
          setType({
            name: response.data.name,
            ICD_code: "",
            cost: 0,
            is_difficult: false,
            duration: "",
          });
          setSubmitted(true);
        })
        .catch(e => {
          alert("popraw czas trwania.\nFormta: 00:00:00")
          console.log(e);
        });
  };

  const newType = () => {
    setType(initialTypeState);
    setSubmitted(false);
  };

  const changeDifficulty = (e) => {
//   this is for button on button delete -> cascade
    e.preventDefault();

    type.is_difficult ? (type.is_difficult = false):( type.is_difficult = true);
    setType({ ...type});
  }

  return (
      <div className="submit-form form_style">
        {submitted ? (
            <div className="form_style">
              <h4>Created new type!</h4>
              <button className="btn btn-success" onClick={newType}> Dodaj </button>
            </div>
        ) : (
            <div>
            <form onSubmit={saveType}>
              <div className="form-group form_style ">
                <label htmlFor="name">Nazwa typu</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    required
                    value={type.name}
                    onChange={handleInputChange}
                    name="name"
                />
                <label htmlFor="name">Kod ICD</label>
                <input
                    type="text"
                    className="form-control"
                    id="ICD_code"
                    required
                    value={type.ICD_code}
                    onChange={handleInputChange}
                    name="ICD_code"
                />
                <label htmlFor="name">Koszt</label>
                <input
                    type="number"
                    className="form-control"
                    id="cost"
                    required
                    value={type.cost}
                    onChange={handleInputChange}
                    name="cost"
                />
                <label htmlFor="name">Czy operacja jest trudna</label>
                <p id="is_difficult" onClick={changeDifficulty}> {type.is_difficult.toString()} </p>
                <button onClick={changeDifficulty}>Change</button>
                <label htmlFor="name">Czas trwania</label>
                <input
                    type="text"
                    className="form-control"
                    id="duration"
                    required
                    value={type.duration}
                    onChange={handleInputChange}
                    name="duration"
                />
              </div>
              <button type="submit" className="btn btn-success"> Zapisz </button>
            </form>
            </div>
        )}
      </div>
  );
};

export default AddTypes;