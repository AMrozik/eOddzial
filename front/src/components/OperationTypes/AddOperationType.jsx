import React, { useState } from "react";
import OperationTypeService from "../../services/RoomService";
import "./AddOperationType.css";

const AddOperationType = () => {
  const initialOperationTypeState = {
    id: null,
    name: "",
    ICD_code: "",
    cost: 0,
    duration: 0,
    is_difficult: false
  };

  const [operationType, setOperationType] = useState(initialOperationTypeState);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setOperationType({ ...operationType, [name]: value });
  };

  const saveOperationType = () => {
    let data = {
      name: operationType.name,
      ICD_code: operationType.ICD_code,
      cost: operationType.cost,
      duration: operationType.duration,
      is_difficult: operationType.is_difficult
    };

    OperationTypeService.create(data)
        .then(response => {
          setOperationType({
            id: response.data.id,
            name: response.data.name,
            ICD_code: response.data.ICD_code,
            cost: response.data.cost,
            duration: response.data.duration,
            is_difficult: response.data.is_difficult
          });
          setSubmitted(true);
          console.log(response.data);
        })
        .catch(e => {
          console.log(e);
        });
  };

  const newOperationType = () => {
    setOperationType(initialOperationTypeState);
    setSubmitted(false);
  };

  return (
      <div className="submit-form form_style_operation_type">
        {submitted ? (
            <div className="form_style_operation_type">
              <h4>You submitted successfully!</h4>
              <button className="btn btn-success" onClick={newOperationType}>
                Add
              </button>
            </div>
        ) : (
            <div>
              <div className="form-group form_style_operation_type ">
                <label htmlFor="name">Operation type</label>
                <input
                    type="text"
                    className="form-control"
                    id="name"
                    required
                    value={operationType.name}
                    onChange={handleInputChange}
                    name="name"
                />
                <label htmlFor="ICD_code">ICD 9</label>
                <input
                    type="text"
                    className="form-control"
                    id="ICD_code"
                    required
                    value={operationType.ICD_code}
                    onChange={handleInputChange}
                    name="ICD_code"
                />
                <label htmlFor="cost">Cost</label>
                <input
                    type="number"
                    className="form-control"
                    id="cost"
                    required
                    value={operationType.cost}
                    onChange={handleInputChange}
                    name="cost"
                />
                <label htmlFor="duration">Duration</label>
                <input
                    type="time"
                    className="form-control"
                    id="duration"
                    required
                    value={operationType.duration}
                    onChange={handleInputChange}
                    name="duration"
                />
                <label htmlFor="is_difficult">Difficulty</label>
                <select
                    className="form-control"
                    value={operationType.is_difficult}
                    onChange={handleInputChange}
                    id="is_difficult"
                    required
                    name="is_difficult">
                      <option value="false">Normal</option>
                      <option value="true">Severe</option>
                </select>
              </div>

              <button onClick={saveOperationType} className="btn btn-success">
                Submit
              </button>
            </div>
        )}
      </div>
  );
};

export default AddOperationType;