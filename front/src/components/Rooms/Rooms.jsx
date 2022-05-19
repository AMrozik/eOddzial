import React, { useState, useEffect, useMemo, useRef } from "react";
import RoomService from "../../services/RoomService";
import { useTable } from "react-table";
import { Link, useNavigate } from "react-router-dom"
import "./Rooms.css";
import PrivateRoute from '../../PrivateRoute';

const Rooms = (props) => {
  const [rooms, setRooms] = useState([]);
  const roomsRef = useRef();
  const navigate = useNavigate();

  roomsRef.current = rooms;

  useEffect(() => {
    retriveRooms();
  }, []);

  const retriveRooms = () => {
    RoomService.getAll()
        .then((response) => {
          setRooms(response.data);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const refreshList = () => {
    retriveRooms();
  };

  const deletionAlert = (id) => {
    if(prompt("Wprowadz DELETE zeby potwierdzic usuniecie\nUWAGA!!! Usuniecie tego pokoju bedzie skutkowalo usunieciem powiazanych danych!",) === "DELETE"){
        deleteRoom(id)
    }
  }

  const deleteRoom = (id) => {
    RoomService.remove(id)
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
          Header: "Operation room",
          accessor: "room_number",
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
    data: rooms,
  });

  return (
        <div className="col-md-12 list table_style">
{/*          TODO: poprawic wyglad tego hrefa, moze calosc wziac w jeszcze jednego diva i wydzielic link z tabeli zeby latwiej go pozycjonowoac*/}
        <a href='/add_room'>dodaj</a>
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
{/*                            ANDRZEJU TUTAJ!!! DOTKNIJ TO PALCEM MIDASA*/}
                          <a href={'/room/'+row.original.id}> edytuj </a>
                          <button type="submit" className="btn btn-success" onClick={() => {deletionAlert(row.original.id)}}> usun </button>
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

export default Rooms;