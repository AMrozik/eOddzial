import React, { useState, useEffect, useMemo, useRef } from "react";
import PatientsService from "../../services/PatientsService";
import { useTable } from "react-table";
import { Link, useNavigate } from "react-router-dom"
import "./Patients.css";
import PrivateRoute from '../../PrivateRoute';

const Patients = (props) => {
  const [patients, setPatients] = useState([]);
  const patientsRef = useRef();
  const navigate = useNavigate();

  patientsRef.current = patients;

  useEffect(() => {
    retrivePatients();
  }, []);

  const retrivePatients = () => {
    PatientsService.getAll()
        .then((response) => {
          setPatients(response.data);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const refreshList = () => {
    retrivePatients();
  };

  const deletionAlert = (id) => {
    if(prompt("Wprowadz DELETE zeby potwierdzic usuniecie\nUWAGA!!! Usuniecie tego pokoju bedzie skutkowalo usunieciem powiazanych danych!",) === "DELETE"){
        deletePatients(id)
    }
  }

  const deletePatients = (id) => {
    PatientsService.remove(id)
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
          Header: "Patients",
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
    data: patients,
  });

  return (
        <div className="col-md-12 list table_style">
{/*          TODO: poprawic wyglad tego hrefa, moze calosc wziac w jeszcze jednego diva i wydzielic link z tabeli zeby latwiej go pozycjonowoac*/}
        <a href='/create_patient'>dodaj</a>
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
                          <a href={'/patient/'+row.original.id}> edytuj </a>
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

export default Patients;