import React, {useState, useEffect, useMemo, useRef} from "react";
import RoomService from "../../services/RoomService";
import {useTable} from "react-table";
import "./OperationTypes.css";
import {Button} from "react-bootstrap/Button";

const OperationTypes = (props) => {
  const [rooms, setRooms] = useState([]);
  const roomsRef = useRef();

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

  const openRoom = (rowIndex) => {
    const id = roomsRef.current[rowIndex].id;

    props.history.push("/rooms/" + id);
  };

  const deleteRoom = (rowIndex) => {
    const id = roomsRef.current[rowIndex].id;

    RoomService.remove(id)
        .then((response) => {
          props.history.push("/rooms");

          let newRooms = [...roomsRef.current];
          newRooms.splice(rowIndex, 1);

          setRooms(newRooms);
          refreshList();
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const addRoom = () => {
    alert("")
  };

  const columns = useMemo(
      () => [
        {
          Header: "Operation room name",
          accessor: "name",
        },
        {
          Header: "Status",
          accessor: "active",
          Cell: (props) => {
            return props.value ? "Active" : "Inactive";
          },
        },
        {
          Header: "Actions",
          accessor: "actions",
          Cell: (props) => {
            const rowIdx = props.row.id;
            return (
                <div>
                <span onClick={() => openRoom(rowIdx)}>
                  <i className="far fa-edit action mr-2 action_icon"/>
                </span>

                  <span onClick={() => deleteRoom(rowIdx)}>
                  <i className="fas fa-trash action action_icon"/>
                </span>

                  <span onClick={() => addRoom()}>
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
    data: rooms,
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