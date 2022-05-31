import React, { useState, useEffect } from "react";
import BudgetYearsService from "../../services/BudgetYearsService";
import {useParams} from "react-router-dom"


const Budget = (props) => {
  const initialBudgetState = {
    year: 0,
    jan: 0,
    feb: 0,
    mar: 0,
    apr: 0,
    may: 0,
    jun: 0,
    jul: 0,
    aug: 0,
    sep: 0,
    oct: 0,
    nov: 0,
    dec: 0,
    given_budget: 0
  };
  const {year} = useParams()
  const [currentBudget, setCurrentBudget] = useState(initialBudgetState);
  const [message, setMessage] = useState("");

  const getBudget = () => {
    BudgetYearsService.get(year)
        .then(response => {
//           console.log(response.data);
            const data = {
                year: response.data.year,
                jan: response.data.jan*100,
                feb: response.data.feb*100,
                mar: response.data.mar*100,
                apr: response.data.apr*100,
                may: response.data.may*100,
                jun: response.data.jun*100,
                jul: response.data.jul*100,
                aug: response.data.aug*100,
                sep: response.data.sep*100,
                oct: response.data.oct*100,
                nov: response.data.nov*100,
                dec: response.data.dec*100,
                given_budget: response.data.given_budget
              };
          setCurrentBudget(data);
        })
        .catch(e => {
          console.log(e);
        });
  };

  useEffect(() => {
    getBudget();
  }, []);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setCurrentBudget({ ...currentBudget, [name]: value });
  };

// Maybe, we have to consider it in later version
//   const updateActive = status => {
//     let data = {
//       id: currentBudget.id,
//       name: currentBudget.name,
//       PESEL: currentBudget.PESEL,
//     };
//
//     BudgetYearsService.update(currentBudget.id, data)
//         .then(response => {
//           currentBudget({ ...currentBudget, active: status });
//           console.log(response.data);
//           setMessage("The status was updated successfully!");
//         })
//         .catch(e => {
//           console.log(e);
//         });
//   };

  const updateBudget = (e) => {
//   this prevents norma behavior of form on submit
    e.preventDefault();
    const data = {
        year: currentBudget.year,
        jan: currentBudget.jan/100,
        feb: currentBudget.feb/100,
        mar: currentBudget.mar/100,
        apr: currentBudget.apr/100,
        may: currentBudget.may/100,
        jun: currentBudget.jun/100,
        jul: currentBudget.jul/100,
        aug: currentBudget.aug/100,
        sep: currentBudget.sep/100,
        oct: currentBudget.oct/100,
        nov: currentBudget.nov/100,
        dec: currentBudget.dec/100,
        given_budget: currentBudget.given_budget
      };

    BudgetYearsService.update(year, data)
        .then(response => {
//        TODO: Chciales tutaj andrzeju wrzucic redirecta na liste pokoi (i chyba mozna wywalic ten message ale to jak juz chcesz)
          setMessage("The Budget was updated successfully!");
        })
        .catch(e => {
          console.log(e);
        });
  };

  return (
      <div className="submit-form form_style">
            <div className="edit-form">
              <form onSubmit={updateBudget}>
                <div className="form-group">
                  <p htmlFor="name">Rok {currentBudget.year}</p>
                <label htmlFor="name">Roczny budzet</label>
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.given_budget}
                    onChange={handleInputChange}
                    name="given_budget"
                />
                <label htmlFor="name">Rozklad procentowy</label>
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.jan}
                    onChange={handleInputChange}
                    name="jan"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.feb}
                    onChange={handleInputChange}
                    name="feb"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.mar}
                    onChange={handleInputChange}
                    name="mar"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.apr}
                    onChange={handleInputChange}
                    name="apr"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.may}
                    onChange={handleInputChange}
                    name="may"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.jun}
                    onChange={handleInputChange}
                    name="jun"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.jul}
                    onChange={handleInputChange}
                    name="jul"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.aug}
                    onChange={handleInputChange}
                    name="aug"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.sep}
                    onChange={handleInputChange}
                    name="sep"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.oct}
                    onChange={handleInputChange}
                    name="oct"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.nov}
                    onChange={handleInputChange}
                    name="nov"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={currentBudget.dec}
                    onChange={handleInputChange}
                    name="dec"
                />%
                </div>
                <button type="submit" className="btn btn-success"> Zapisz </button>
              </form>
              <p>{message}</p>
            </div>
      </div>
  );
};

export default Budget;