import React, {useState, useEffect} from "react";
import WardDataService from "../../services/WardDataService";

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
                if (e.response.status === 409) {
                    setExist(false);
                } else {
                    console.log(e);
                }
            });
    };

    useEffect(() => {
//     checkExistence();
        getWardData();
    }, []);

    const handleInputChange = event => {
        const {name, value} = event.target;
        setCurrentWardData({...currentWardData, [name]: value});
    };

    const updateWardData = (e) => {
//   this prevents norma behavior of form on submit
        e.preventDefault();

        WardDataService.update(currentWardData)
            .then(response => {
                setMessage("The WardData was updated successfully!");
            })
            .catch(error => {
                if (e.response.status === 400) {
                    alert("Prosze poprawic czas przygotowania sali operacyjnej!\nFormat: HH:MM:SS");
                }
                console.log(error);
            });
    };

    return (
        <div className="submit-form form_style">
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
                        <button type="submit" className="btn btn-success"> Zapisz</button>
                    </form>
                    <p>{message}</p>
                </div>
            ) : (
                <div className="submit-form form_style">
                    {/*              staralem sie bawic w fajne przekierowania, ale meta w tym miejscu wywala nawet na widoku od edycji ward data*/}
                    {/*                 <head><meta httpEquiv="refresh" content="2; /add_ward_data"/></head> */}
                    <h1> Brak Konfiguracji </h1>


                    <button type="submit" className="btn btn-success table_button">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                             className="bi bi-plus-circle" viewBox="0 0 16 16">
                            <path
                                d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                            <path
                                d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                        </svg>
                        <a href="/add_ward_data"> Skonfiguruj </a>
                    </button>
                </div>
            )}

        </div>
    );
};

export default WardData;