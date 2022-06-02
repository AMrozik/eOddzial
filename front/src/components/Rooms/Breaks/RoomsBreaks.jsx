import React, {useState, useEffect, useMemo, useRef} from "react";
import RoomsBreaksService from "../../../services/RoomsBreaksService";
import RoomsService from "../../../services/RoomsService";
import {useTable} from "react-table";

const RoomsBreaks = (props) => {
    const [roomsBreaks, setRoomsBreaks] = useState([]);
    const roomsBreaksRef = useRef();

    roomsBreaksRef.current = roomsBreaks;

    useEffect(() => {
        retriveRoomsBreaks();
    }, []);

    const retriveRoomsBreaks = () => {
        RoomsBreaksService.getAll()
            .then((response) => {
                let temp = response.data;
                RoomsService.getAll().then((resp) => {
                    let temp2 = [];
                    temp2 = resp.data;
                    for (var i = 0; i < temp.length; i++) {
                        for (var j = 0; j < temp2.length; j++) {
                            if (temp2[j].id == temp[i]["room"]) {
                                temp[i]["room_number"] = temp2[j]["room_number"];
                            }
                        }
                        var temp_date_start = new Date(temp[i]["date_start"]);
                        temp[i]["date_start"] = temp_date_start.toLocaleString();
                        var temp_date_end = new Date(temp[i]["date_end"]);
                        temp[i]["date_end"] = temp_date_end.toLocaleString();
                    }
                    setRoomsBreaks(temp);
                });
            })
            .catch((e) => {
                console.log(e);
            });
    };

    const refreshList = () => {
        retriveRoomsBreaks();
    };

    const deletionAlert = (id) => {
        if (prompt("Wprowadz DELETE zeby potwierdzic usuniecie\nUWAGA!!! Usuniecie tego elementu bedzie skutkowalo usunieciem powiazanych danych!",) === "DELETE") {
            deleteRoomBreak(id)
        }
    }

    const deleteRoomBreak = (id) => {
        RoomsBreaksService.remove(id)
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
                Header: "Number pokoj",
                accessor: "room_number",
            },
            {
                Header: "Start",
                accessor: "date_start",
            },
            {
                Header: "Koniec",
                accessor: "date_end",
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
        data: roomsBreaks,
    });

    return (
        <div className="col-md-12 list table_style">
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
                                    </td>
                                );
                            })}
                            <td>
                                {/* ANDRZEJU TUTAJ!!! DOTKNIJ TO PALCEM MIDASA */}


                                <button type="submit" className="btn btn-danger table_button" onClick={() => {
                                    deletionAlert(row.original.id)
                                }}>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                         fill="currentColor" className="bi bi-dash-circle" viewBox="0 0 16 16">
                                        <path
                                            d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                        <path d="M4 8a.5.5 0 0 1 .5-.5h7a.5.5 0 0 1 0 1h-7A.5.5 0 0 1 4 8z"/>
                                    </svg> usuń
                                </button>


                                <button type="submit" className="btn btn-success table_button">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                         fill="currentColor" className="bi bi-plus-circle" viewBox="0 0 16 16">
                                        <path
                                            d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                                        <path
                                            d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                                    </svg>
                                    <a href={'/room_break/' + row.original.id}> edytuj </a>
                                </button>
                            </td>
                        </tr>
                    );
                })}
                </tbody>
            </table>
        </div>
    );
};

export default RoomsBreaks;