import React, { useState, useEffect } from "react";
import WardDataService from "../../services/WardDataService";
// import './AddRoom.css';

const WardData = (props) => {
  const initialWardDataState = {
    id: null,
    operation_prepare_time: "",
    working_start_hour: "",
    working_end_hour: "",
    child_interval_hour: "",
    difficult_interval_hour: ""
  };

  const [currentWardData, setCurrentWardData] = useState(initialWardDataState);
  const [message, setMessage] = useState("");
  const [exist, setExist] = useState(false);

//   const checkExistence = () => {
//       WardDataService.get()
//             .then(response => {
//                 if (response.data) { setExist(true); }
//             })
//             .catch(e => {
//                 if (e.response.status === 409) { setExist(false); }
//                 console.log(e);
//             });
//   };

  const getWardData = () => {
    WardDataService.get()
        .then(response => {
            if (response.data) {
                setExist(true);
                setCurrentWardData(response.data);
            }
        })
        .catch(e => {
            if (e.response.status === 409) { setExist(false); }
            else { console.log(e); }
        });
  };

  useEffect(() => {
//     checkExistence();
    getWardData();
  }, []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setCurrentWardData({ ...currentWardData, [name]: value });
  };

  const updateWardData = (e) => {
//   this prevents norma behavior of form on submit
    e.preventDefault();

    WardDataService.update(currentWardData)
        .then(response => {
          setMessage("The WardData was updated successfully!");
        })
        .catch(e => {
          if (e.response.status === 400){
            alert("Prosze poprawic czas przygotowania sali operacyjnej!\nFormat: HH:MM:SS");
          }
          console.log(e);
        });
  };

  return (
      <div>
        {exist ? (
            <div className="edit-form">
              <form onSubmit={updateWardData}>
                <div className="form-group">
                  <label htmlFor="name">Czas przygotowania do operacji</label>
                  <input
                      type="text"
                      className="form-control"
                      id="name"
                      required
                      name="operation_prepare_time"
                      value={currentWardData.operation_prepare_time}
                      onChange={handleInputChange}
                  />
                  <label htmlFor="name">Ward opening hour</label>
                  <input
                      type="time"
                      className="form-control"
                      id="name"
                      required
                      name="working_start_hour"
                      value={currentWardData.working_start_hour}
                      onChange={handleInputChange}
                  />
                  <label htmlFor="name">Ward ending hour</label>
                  <input
                      type="time"
                      className="form-control"
                      id="name"
                      required
                      name="working_end_hour"
                      value={currentWardData.working_end_hour}
                      onChange={handleInputChange}
                  />
                  <label htmlFor="name">Child interval ending hour</label>
                  <input
                      type="time"
                      className="form-control"
                      id="name"
                      required
                      name="child_interval_hour"
                      value={currentWardData.child_interval_hour}
                      onChange={handleInputChange}
                  />
                  <label htmlFor="name">Difficult operations starting hour</label>
                  <input
                      type="time"
                      className="form-control"
                      id="name"
                      required
                      name="difficult_interval_hour"
                      value={currentWardData.difficult_interval_hour}
                      onChange={handleInputChange}
                  />
                </div>
              <button type="submit" className="btn btn-success"> Zapisz </button>
              </form>
              <p>{message}</p>
            </div>
        ) : (
            <div>
{/*              staralem sie bawic w fajne przekierowania, ale meta w tym miejscu wywala nawet na widoku od edycji ward data*/}
{/*                 <head><meta httpEquiv="refresh" content="2; /add_ward_data"/></head> */}
                <h1>NIC TU NIE MA SAMA TRAWA</h1>
                <a href="/add_ward_data">Udaj sie do przygotowania konfiguracji</a>
            </div>
        )}

      </div>
  );
};

export default WardData;