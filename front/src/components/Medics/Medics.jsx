import React, {useState, useEffect, useMemo, useRef} from "react";
import MedicsService from "../../services/MedicsService";
import {useTable} from "react-table";

const Medics = (props) => {
    const [medics, setMedics] = useState([]);
    const medicsRef = useRef();

    medicsRef.current = medics;

    useEffect(() => {
        retriveMedics();
    }, []);

    const retriveMedics = () => {
        MedicsService.getAll()
            .then((response) => {
                setMedics(response.data);
            })
            .catch((e) => {
                console.log(e);
            });
    };

    const refreshList = () => {
        retriveMedics();
    };

    const deletionAlert = (id) => {
        if (prompt("Wprowadz DELETE zeby potwierdzic usuniecie\nUWAGA!!! Usuniecie tego elementu bedzie skutkowalo usunieciem powiazanych danych!",) === "DELETE") {
            deleteMedics(id)
        }
    }

    const deleteMedics = (id) => {
        MedicsService.remove(id)
            .then(response => {
                window.location.reload();
            })
            .catch(e => {
                console.log(e);
            });
    };

    const columns = useMemo(
        () => [
            {
                Header: "Medics",
                accessor: "name",
            },
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
        data: medics,
    });

    return (
        <div className="col-md-12 list table_style">
            {/*          TODO: poprawic wyglad tego hrefa, moze calosc wziac w jeszcze jednego diva i wydzielic link z tabeli zeby latwiej go pozycjonowoac*/}

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
                                <button type="submit" className="btn btn-warning table_button">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                                         className="bi bi-pause-circle" viewBox="0 0 16 16">
                                        <path
                                            d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                        <path
                                            d="M5 6.25a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5zm3.5 0a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5z"/>
                                    </svg>
                                    <a href='/medics_breaks'> przerwy</a>
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
                                        <button type="submit" className="btn btn-warning table_button">
                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                                 fill="currentColor" className="bi bi-pause-circle" viewBox="0 0 16 16">
                                                <path
                                                    d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                                <path
                                                    d="M5 6.25a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5zm3.5 0a1.25 1.25 0 1 1 2.5 0v3.5a1.25 1.25 0 1 1-2.5 0v-3.5z"/>
                                            </svg>
                                            <a href={'/add_medic_break/' + row.original.id}> dodaj przerwe </a>
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

export default Medics;