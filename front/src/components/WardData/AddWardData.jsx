import React, { useState, useEffect, Redirect } from "react";
import WardDataService from "../../services/WardDataService";
import { useNavigate } from "react-router-dom";

const AddWardData = () => {
  const initialWardDataState = {
    id: null,
    operation_prepare_time: "",
    working_start_hour: "",
    working_end_hour: "",
    child_interval_hour: "",
    difficult_interval_hour: ""
  };

  const [wardData, setWardData] = useState(initialWardDataState);
  const [submitted, setSubmitted] = useState(false);
  const [exist, setExist] = useState(false);
    let navigate = useNavigate();

  const checkExistence = () => {
      WardDataService.get()
            .then(response => {
                if (response.data) { setExist(true); setTimeout(()=>{navigate('/home')}, 5000)}
            })
            .catch(e => {
                if (e.response.status === 409) {  setExist(false); }
                console.log(e);
            });
  };

  useEffect(() => {
    checkExistence();
  }, []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setWardData({ ...wardData, [name]: value });
  };

  const saveWardData = () => {
    let data = {
      operation_prepare_time: wardData.operation_prepare_time,
      working_start_hour: wardData.working_start_hour,
      working_end_hour: wardData.working_end_hour,
      child_interval_hour: wardData.child_interval_hour,
      difficult_interval_hour: wardData.difficult_interval_hour
    };

    WardDataService.create(data)
        .then(response => {
          setWardData({
            operation_prepare_time: wardData.operation_prepare_time,
            working_start_hour: wardData.working_start_hour,
            working_end_hour: wardData.working_end_hour,
            child_interval_hour: wardData.child_interval_hour,
            difficult_interval_hour: wardData.difficult_interval_hour
          });
          setSubmitted(true);
        })
        .catch(e => {
            if (e.response.status === 400){
                alert("Prosze poprawic czas przygotowania sali operacyjnej!\nFormat: HH:MM:SS");
            }
          console.log(e);
        });
  };

  const newWardData = () => {
    setWardData(initialWardDataState);
    setSubmitted(false);
  };

  return (
      <div className="submit-form form_style">
        {exist ? (
            <div>
                <h1>Już Skonfigurowano</h1>
            </div>
        ) : (submitted ? (
                <div className="form_style">
                    <head><meta httpEquiv="refresh" content="2; /home"/></head>
                  <h4>Created new configuration!</h4>
                </div>
            ) : (
                <div>
                  <div className="form-group form_style ">
                    <label htmlFor="name">Czas przygotowania operacji</label>
                    <input
                        type="text"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.operation_prepare_time}
                        onChange={handleInputChange}
                        name="operation_prepare_time"
                    /><label htmlFor="name">Godzina rozpoczęcia pracy</label>
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.working_start_hour}
                        onChange={handleInputChange}
                        name="working_start_hour"
                    /><label htmlFor="name">Godzina zakończenia pracy</label>
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.working_end_hour}
                        onChange={handleInputChange}
                        name="working_end_hour"
                    /><label htmlFor="name">Godzina zakończenia strefy dziecięcej</label>
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.child_interval_hour}
                        onChange={handleInputChange}
                        name="child_interval_hour"
                    /><label htmlFor="name">Godzina rozpoczęcia strefy trudnych operacji</label>
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.difficult_interval_hour}
                        onChange={handleInputChange}
                        name="difficult_interval_hour"
                    />
                  </div>

                  <button onClick={saveWardData} className="btn btn-success"> Zapisz </button>
                </div>
            )
        )}

      </div>
  );
};

export default AddWardData;