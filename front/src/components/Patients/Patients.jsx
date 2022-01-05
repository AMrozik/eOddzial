import React, {useState, useEffect, useMemo, useRef} from "react";
import PatientService from "../../services/PatientService";
import {useTable} from "react-table";
import "./Patients.css";
import {Button} from "react-bootstrap/Button";

const Patients = (props) => {
  const [patients, setPatients] = useState([]);
  const patientsRef = useRef();

  patientsRef.current = patients;

  useEffect(() => {
    retrievePatients();
  }, []);

  const retrievePatients = () => {
    PatientService.getAll()
        .then((response) => {
          setPatients(response.data);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const openPatient = (rowIndex) => {
    const id = patientsRef.current[rowIndex].id;

    props.history.push("/patient/" + id);
  };

  const deletePatient = (rowIndex) => {
    const id = patientsRef.current[rowIndex].id;

    PatientService.remove(id)
        .then((response) => {
          props.history.push("/patients");

          let newPatients = [...patientsRef.current];
          newPatients.splice(rowIndex, 1);

          setPatients(newPatients);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const addPatient = () => {
    alert("")
  };

  const columns = useMemo(
      () => [
        {
          Header: "Patient name",
          accessor: "name",
        },
        {
          Header: "PESEL",
          accessor: "PESEL",
        },
        {
          Header: "Age",
          accessor: "age",
        },
        {
          Header: "Actions",
          accessor: "actions",
          Cell: (props) => {
            const rowIdx = props.row.id;
            return (
                <div>
                <span onClick={() => openPatient(rowIdx)}>
                  <i className="far fa-edit action mr-2 action_icon"/>
                </span>

                  <span onClick={() => deletePatient(rowIdx)}>
                  <i className="fas fa-trash action action_icon"/>
                </span>

                  <span onClick={() => addPatient()}>
                  <i className="fas fa-plus-circle action action_icon"/>
                </span>
                </div>
            );
          },
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
    data: patients,
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
                        <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
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