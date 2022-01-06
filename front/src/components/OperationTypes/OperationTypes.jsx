import React, {useState, useEffect, useMemo, useRef} from "react";
import OperationTypeService from "../../services/OperationTypeService";
import {useTable} from "react-table";
import "./OperationTypes.css";
import {Button} from "react-bootstrap/Button";

const OperationTypes = (props) => {
  const [operationTypes, setOperationTypes] = useState([]);
  const operationTypesRef = useRef();

  operationTypesRef.current = operationTypes;

  useEffect(() => {
    retrieveOperationTypes();
  }, []);

  const retrieveOperationTypes = () => {
    OperationTypeService.getAll()
        .then((response) => {
          setOperationTypes(response.data);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const refreshList = () => {
    retrieveOperationTypes();
  };

  const openOperationType = (rowIndex) => {
    const id = operationTypesRef.current[rowIndex].id;

    props.history.push("/operation_type/" + id);
  };

  const deleteOperationType = (rowIndex) => {
    const id = operationTypesRef.current[rowIndex].id;

    OperationTypeService.remove(id)
        .then((response) => {
          props.history.push("/operation_type");

          let newOperationTypes = [...operationTypesRef.current];
          newOperationTypes.splice(rowIndex, 1);

          setOperationTypes(newOperationTypes);
          refreshList();
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const addOperationType = () => {
    alert("")
  };

  const columns = useMemo(
      () => [
        {
          Header: "Name",
          accessor: "name",
        },
        {
          Header: "ICD 9",
          accessor: "ICD_code",
        },
        {
          Header: "Cost",
          accessor: "cost",
        },
        {
          Header: "Duration",
          accessor: "duration",
        },
        {
          Header: "Difficulty",
          accessor: "is_difficult",
          Cell: (props) => {
            return props.value ? "Severe" : "Normal";
          },
        },
        {
          Header: "Actions",
          accessor: "actions",
          Cell: (props) => {
            const rowIdx = props.row.id;
            return (
                <div>
                <span onClick={() => openOperationType(rowIdx)}>
                  <i className="far fa-edit action mr-2 action_icon"/>
                </span>

                  <span onClick={() => deleteOperationType(rowIdx)}>
                  <i className="fas fa-trash action action_icon"/>
                </span>

                  <span onClick={() => addOperationType()}>
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
    data: operationTypes,
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

export default OperationTypes;