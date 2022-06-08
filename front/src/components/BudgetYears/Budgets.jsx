import React, {useState, useEffect, useMemo, useRef} from "react";
import BudgetYearsService from "../../services/BudgetYearsService";
import {useTable} from "react-table";

const Budgets = (props) => {
    const [budgets, setBudgets] = useState([]);
    const [visibleBudgets, setVisibleBudgets] = useState([]);
    const budgetsRef = useRef();

    budgetsRef.current = budgets;

    useEffect(() => {
        retriveBudgets();
    }, []);

    const retriveBudgets = () => {
        BudgetYearsService.getAll()
            .then((response) => {
                setBudgets(response.data);
                setVisibleBudgets(response.data);
            })
            .catch((e) => {
                console.log(e);
            });
    };

    // const refreshList = () => {
    //     retriveBudgets();
    // };

    const deletionAlert = (id) => {
        if (prompt("Wprowadz DELETE zeby potwierdzic usuniecie\nUWAGA!!! Usuniecie tego elementu bedzie skutkowalo usunieciem powiazanych danych!",) === "DELETE") {
            deleteBudgets(id)
        }
    }

    const deleteBudgets = (id) => {
        BudgetYearsService.remove(id)
            .then(response => {
                window.location.reload();
            })
            .catch(e => {
                console.log(e);
            });
    };

    let inputSearchHandler = (element) => {
        var lowerCase = element.target.value.toLowerCase();
        setVisibleBudgets(budgets.filter((element) => {return element.year.toString().toLowerCase().includes(lowerCase)}));
    };

    const buttonSVG = () => {
        return ([
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                 className="bi bi-plus-circle" viewBox="0 0 16 16">
                <path
                    d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                <path
                    d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
            </svg>
        ])
    }

    const columns = useMemo(
        () => [
            {
                Header: "Rok",
                accessor: "year",
            },
//             {
//                 Header: "Wartosc",
//                 accessor: "given_budget",
//             },
        ],
        []
    );

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
    } = useTable({
        columns,
        data: visibleBudgets,
    });

    return (
        <div className="col-md-12 list table_style">
            <input
                id="outlined-basic"
                type="text"
                onChange={inputSearchHandler}
                variant="outlined"
                label="Search"
            />
            <table
                className="table table-striped table-bordered"
                {...getTableProps()}
            >
                <thead>
                {headerGroups.map((headerGroup) => (
                    <tr {...headerGroup.getHeaderGroupProps()}>
                        {headerGroup.headers.map((column) => (
                            <th {...column.getHeaderProps()}>
                                {column.render("Header")}


                                <button type="submit" className="btn btn-success table_button">
                                    {buttonSVG()}
                                    <a href='/add_budget_year'> dodaj</a>
                                </button>

                            </th>
                        ))}
                    </tr>
                ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                {rows.map((row, i) => {
                    prepareRow(row);
                    return (
                        <tr {...row.getRowProps()}>
                            {row.cells.map((cell) => {
                                return (
                                    <td {...cell.getCellProps()}>
                                        {cell.render("Cell")}
                                        {/*                            ANDRZEJU TUTAJ!!! DOTKNIJ TO PALCEM MIDASA*/}


                                        <button type="submit" className="btn btn-success table_button">
                                            {buttonSVG()}
                                            <a href={'/budget_year/' + row.original.year}> edytuj </a>
                                        </button>


                                        <button type="submit" className="btn btn-danger table_button" onClick={() => {
                                            deletionAlert(row.original.year)
                                        }}>
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                 fill="currentColor" className="bi bi-dash-circle" viewBox="0 0 16 16">
                                                <path
                                                    d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                                <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                                            </svg> usuń
                                        </button>

                                    </td>
                                );
                            })}
                        </tr>
                    );
                })}
                </tbody>
            </table>
        </div>
    );
};

export default Budgets;