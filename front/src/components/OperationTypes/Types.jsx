import React, { useState, useEffect, useMemo, useRef } from "react";
import TypesService from "../../services/TypesService";
import { useTable } from "react-table";
import { Link, useNavigate } from "react-router-dom"
import "./Types.css";
import PrivateRoute from '../../PrivateRoute';

const Types = (props) => {
  const [types, setTypes] = useState([]);
  const typesRef = useRef();
  const navigate = useNavigate();

  typesRef.current = types;

  useEffect(() => {
    retriveTypes();
  }, []);

  const retriveTypes = () => {
    TypesService.getAll()
        .then((response) => {
          setTypes(response.data);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const refreshList = () => {
    retriveTypes();
  };

  const deletionAlert = (id) => {
    if(prompt("Wprowadz DELETE zeby potwierdzic usuniecie\nUWAGA!!! Usuniecie tego pokoju bedzie skutkowalo usunieciem powiazanych danych!",) === "DELETE"){
        deleteTypes(id)
    }
  }

  const deleteTypes = (id) => {
    TypesService.remove(id)
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
          Header: "Type",
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
    data: types,
  });

  return (
        <div className="col-md-12 list table_style">
            <a href='/add_type'>dodaj</a>
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
                          <a href={'/type/'+row.original.id}> edytuj </a>
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

export default Types;