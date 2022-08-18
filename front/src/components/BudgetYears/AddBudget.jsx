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
                <div>
                    <label htmlFor="name" >Styczen:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.jan}
                        onChange={handleInputChange}
                        name="jan"
                        align="left"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Luty:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.feb}
                        onChange={handleInputChange}
                        name="feb"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Marzec:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.mar}
                        onChange={handleInputChange}
                        name="mar"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Kwiecien:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.apr}
                        onChange={handleInputChange}
                        name="apr"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Maj:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.may}
                        onChange={handleInputChange}
                        name="may"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Czerwiec:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.jun}
                        onChange={handleInputChange}
                        name="jun"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Lipiec:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.jul}
                        onChange={handleInputChange}
                        name="jul"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Sierpien:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.aug}
                        onChange={handleInputChange}
                        name="aug"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Wrzesien:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.sep}
                        onChange={handleInputChange}
                        name="sep"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Pazdziernik:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.oct}
                        onChange={handleInputChange}
                        name="oct"
                        style={{"width": "40%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div>
                    <label htmlFor="name" >Listopad:</label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.nov}
                        onChange={handleInputChange}
                        name="nov"
                        style={{"width": "50%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>
                <div >
                    <label htmlFor="name">Grodzien: </label>
                    <input
                        type="number"
                        className="form-control"
                        id="name"
                        required
                        value={budget.dec}
                        onChange={handleInputChange}
                        name="dec"
                        style={{"width": "45%", "display":"inline"}}
                    />
                    <label style={{"margin-left": "4px"}} htmlFor="name">%</label>
                </div>

              </div>
              <button type="submit" className="btn btn-success"> Zapisz </button>
            </form>
            </div>
        )}
      </div>
  );
};

export default AddBudget;