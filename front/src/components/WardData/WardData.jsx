import React, {useState, useEffect} from "react";
import WardDataService from "../../services/WardDataService";
import { useNavigate } from "react-router-dom";

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
    let navigate = useNavigate();

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
                    setTimeout(()=>{navigate('/add_ward_data')}, 5000);
                } else {
                    console.log(e);
                }
            });
    };

    useEffect(() => {
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
                            <label htmlFor="name">Godzina rozpoczęcia pracy</label>
                            <input
                                type="time"
                                className="form-control"
                                id="name"
                                required
                                name="working_start_hour"
                                value={currentWardData.working_start_hour}
                                onChange={handleInputChange}
                            />
                            <label htmlFor="name">Godzina zakończenia pracy</label>
                            <input
                                type="time"
                                className="form-control"
                                id="name"
                                required
                                name="working_end_hour"
                                value={currentWardData.working_end_hour}
                                onChange={handleInputChange}
                            />
                            <label htmlFor="name">Godzina zakończenia strefy dziecięcej</label>
                            <input
                                type="time"
                                className="form-control"
                                id="name"
                                required
                                name="child_interval_hour"
                                value={currentWardData.child_interval_hour}
                                onChange={handleInputChange}
                            />
                            <label htmlFor="name">Godzina rozpoczęcia strefy trudnych operacji</label>
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