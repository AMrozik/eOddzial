import React, { useState, useEffect, Redirect } from "react";
import WardDataService from "../../services/WardDataService";
// import './AddRoom.css';

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

  const checkExistence = () => {
      WardDataService.get()
            .then(response => {
                if (response.data) { setExist(true); }
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
{/*                  Obviously meta should not be part of body but no one really knows that this is here XD, also redirects don't work fsr*/}
{/*                  Remember to not set content on 0 because it causes logout*/}
                <head><meta httpEquiv="refresh" content="2; /home"/></head>
                <h1>NIC TU NIE MA SAMA TRAWA</h1>
                <a href="/home"> take me home country road </a>
            </div>
        ) : (submitted ? (
                <div className="form_style">
                    <head><meta httpEquiv="refresh" content="2; /home"/></head>
                  <h4>Created new configuration!</h4>
                </div>
            ) : (
                <div>
                  <div className="form-group form_style ">
                    <label htmlFor="name">operation_prepare_time</label>
                    <input
                        type="text"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.operation_prepare_time}
                        onChange={handleInputChange}
                        name="operation_prepare_time"
                    /><label htmlFor="name">working_start_hour</label>
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.working_start_hour}
                        onChange={handleInputChange}
                        name="working_start_hour"
                    /><label htmlFor="name">working_end_hour</label>
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.working_end_hour}
                        onChange={handleInputChange}
                        name="working_end_hour"
                    /><label htmlFor="name">child_interval_hour</label>
                    <input
                        type="time"
                        className="form-control"
                        id="name"
                        required
                        value={wardData.child_interval_hour}
                        onChange={handleInputChange}
                        name="child_interval_hour"
                    /><label htmlFor="name">difficult_interval_hour</label>
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