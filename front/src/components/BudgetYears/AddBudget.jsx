import React, { useState } from "react";
import BudgetYearsService from "../../services/BudgetYearsService";


const AddBudget = () => {
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
  const [budget, setBudget] = useState(initialBudgetState);
  const [submitted, setSubmitted] = useState(false);

  const handleInputChange = event => {
    const { name, value } = event.target;
    setBudget({ ...budget, [name]: value });
  };

  const saveBudget = (e) => {
//   this prevents normal behavior of form on submit
    e.preventDefault();

    let data = {
    year: budget.year,
    jan: budget.jan/100,
    feb: budget.feb/100,
    mar: budget.mar/100,
    apr: budget.apr/100,
    may: budget.may/100,
    jun: budget.jun/100,
    jul: budget.jul/100,
    aug: budget.aug/100,
    sep: budget.sep/100,
    oct: budget.oct/100,
    nov: budget.nov/100,
    dec: budget.dec/100,
    given_budget: budget.given_budget
    };
    console.log(data);

    BudgetYearsService.create(data)
        .then(response => {
          setBudget({
            year: response.data.year,
            jan: response.data.jan,
            feb: response.data.feb,
            mar: response.data.mar,
            apr: response.data.apr,
            may: response.data.may,
            jun: response.data.jun,
            jul: response.data.jul,
            aug: response.data.aug,
            sep: response.data.sep,
            oct: response.data.oct,
            nov: response.data.nov,
            dec: response.data.dec,
            given_budget: response.data.given_budget
          });
          setSubmitted(true);
        })
        .catch(e => {
                if (e.response.status === 400) {  alert("Podany rok jest juz utworzony. Edycja jest dostepna tylko z widoku edycji") }
          console.log(e);
        });
  };

  const newBudget = () => {
    setBudget(initialBudgetState);
    setSubmitted(false);
  };

  return (
      <div className="submit-form form_style">
        {submitted ? (
            <div className="form_style">
              <h4>Created new Budget!</h4>
              <button className="btn btn-success" onClick={newBudget}> Dodaj </button>
            </div>
        ) : (
            <div>
            <form onSubmit={saveBudget}>
              <div className="form-group form_style ">
                <label htmlFor="name">Rok</label>
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.year}
                    onChange={handleInputChange}
                    name="year"
                />
                <label htmlFor="name">Roczny budzet</label>
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.given_budget}
                    onChange={handleInputChange}
                    name="given_budget"
                />
                <label htmlFor="name">Rozklad procentowy</label>
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.jan}
                    onChange={handleInputChange}
                    name="jan"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.feb}
                    onChange={handleInputChange}
                    name="feb"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.mar}
                    onChange={handleInputChange}
                    name="mar"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.apr}
                    onChange={handleInputChange}
                    name="apr"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.may}
                    onChange={handleInputChange}
                    name="may"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.jun}
                    onChange={handleInputChange}
                    name="jun"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.jul}
                    onChange={handleInputChange}
                    name="jul"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.aug}
                    onChange={handleInputChange}
                    name="aug"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.sep}
                    onChange={handleInputChange}
                    name="sep"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.oct}
                    onChange={handleInputChange}
                    name="oct"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.nov}
                    onChange={handleInputChange}
                    name="nov"
                />%
                <input
                    type="number"
                    className="form-control"
                    id="name"
                    required
                    value={budget.dec}
                    onChange={handleInputChange}
                    name="dec"
                />%

              </div>
              <button type="submit" className="btn btn-success"> Zapisz </button>
            </form>
            </div>
        )}
      </div>
  );
};

export default AddBudget;