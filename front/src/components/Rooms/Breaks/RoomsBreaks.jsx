import React, { useState, useEffect, useMemo, useRef } from "react";
import RoomsBreaksService from "../../../services/RoomsBreaksService";
import RoomsService from "../../../services/RoomsService";
import { useTable } from "react-table";
import { Link, useNavigate } from "react-router-dom"
import "./RoomsBreaks.css";
import PrivateRoute from '../../../PrivateRoute';

const RoomsBreaks = (props) => {
  const [roomsBreaks, setRoomsBreaks] = useState([]);
  const roomsBreaksRef = useRef();
  const navigate = useNavigate();

  roomsBreaksRef.current = roomsBreaks;

  useEffect(() => {
    retriveRoomsBreaks();
  }, []);

  const retriveRoomsBreaks = () => {
    RoomsBreaksService.getAll()
        .then((response) => {
          let temp = response.data;
          RoomsService.getAll().then((resp)=>{
            let temp2 = [];
            temp2 = resp.data;
            for(var i=0; i<temp.length; i++){
                for(var j=0; j<temp2.length; j++){
                    if(temp2[j].id == temp[i]["room"]){
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
    if(prompt("Wprowadz DELETE zeby potwierdzic usuniecie\nUWAGA!!! Usuniecie tego pokoju bedzie skutkowalo usunieciem powiazanych danych!",) === "DELETE"){
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
          Header: "Operation room",
          accessor: "room_number",
        },
        {
          Header: "Start",
          accessor: "date_start",
        },
        {
          Header: "End",
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
{/*                   ANDRZEJU TUTAJ!!! DOTKNIJ TO PALCEM MIDASA*/}
                      <a href={'/room_break/'+row.original.id}> edytuj </a>
                      <button type="submit" className="btn btn-success" onClick={() => {deletionAlert(row.original.id)}}> usun </button>
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