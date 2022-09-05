import React, {useState, useEffect, useMemo, useRef} from "react";
import OperationService from "../../services/OperationService";
import HintingAlgService from "../../services/HintingAlgService";
import TypesService from "../../services/TypesService";
import MedicsService from "../../services/MedicsService";
import PatientsService from "../../services/PatientsService";
import RoomsService from "../../services/RoomsService";
import {useTable} from "react-table";
import {useNavigate} from "react-router-dom"

const Operation = (props) => {
    const [operation, setOperation] = useState([]);
    const [visibleOperation, setVisibleOperation] = useState([]);
    const operationRef = useRef();
    const navigate = useNavigate();
    const today = new Date();

    operationRef.current = operation;

    useEffect(() => {
        retriveOperation();
    }, []);

    const retriveOperation = () => {
        OperationService.getAll()
            .then((response) => {
                setOperation(response.data);
                setVisibleOperation(response.data);
            })
            .catch((e) => {
                console.log(e);
            });
    };

    const refreshList = () => {
        retriveOperation();
    };

    const deletionAlert = (id) => {
        if (prompt("Wprowadz DELETE zeby potwierdzic usuniecie\nUWAGA!!! Usuniecie tego elementu bedzie skutkowalo usunieciem powiazanych danych!",) === "DELETE") {
            deleteOperation(id)
        }
    }

const deleteOperation = (id) => {
        OperationService.remove(id)
            .then(response => {
                window.location.reload();
            })
            .catch(e => {
                console.log(e);
            });
    };

    let inputSearchHandler = (element) => {
        var lowerCase = element.target.value.toLowerCase();
        setVisibleOperation(operation.filter((element) => {return element.date.toLowerCase().includes(lowerCase)}));
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
                Header: "Operacja",
                accessor: operation => 'data operacji: ' + operation.date + ' godzina: ' + operation.start
            }
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
        data: visibleOperation,
    });

    return (
        <div className="col-md-12 list table_style">

            <label>Wyszukaj operacje po dacie</label>
            <input class="form-group searchbar" placeholder="Wyszukaj operacje" type="date" onChange={inputSearchHandler}/>

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
                                <a href={'/operation_date_search/'+today.getFullYear()+'-'+(parseInt(today.getMonth())+1)}>
                                    <button type="submit" className="btn btn-success table_button">
                                        {buttonSVG()} Dodaj
                                    </button>
                                </a>
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
                                        <a href={'/operations/' + row.original.id}>
                                            <button type="submit" className="btn btn-success table_button">
                                                {buttonSVG()} Edytuj
                                            </button>
                                        </a>
                                        <button type="submit" className="btn btn-danger table_button" onClick={() => {
                                            deletionAlert(row.original.id)
                                        }}>
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                 fill="currentColor" className="bi bi-dash-circle" viewBox="0 0 16 16">
                                                <path
                                                    d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                                <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                                            </svg> Usun
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

export default Operation;
