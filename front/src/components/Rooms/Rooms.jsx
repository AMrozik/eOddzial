import React, {useState, useEffect, useMemo, useRef} from "react";
import RoomService from "../../services/RoomService";
import {useTable} from "react-table";
import "./Rooms.css";
import AddRoom from "./AddRoom";
import {Button} from "react-bootstrap/Button";

const Rooms = (props) => {
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

  const removeAllTutorials = () => {
    RoomService.removeAll()
        .then((response) => {
          console.log(response.data);
          refreshList();
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const openTutorial = (rowIndex) => {
    const id = roomsRef.current[rowIndex].id;

    props.history.push("/rooms/" + id);
  };

  const deleteTutorial = (rowIndex) => {
    const id = roomsRef.current[rowIndex].id;

    RoomService.remove(id)
        .then((response) => {
          props.history.push("/rooms");

          let newTutorials = [...roomsRef.current];
          newTutorials.splice(rowIndex, 1);

          setRooms(newTutorials);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  const addTutorial = () => {
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
                <span onClick={() => openTutorial(rowIdx)}>
                  <i className="far fa-edit action mr-2 action_icon"/>
                </span>

                <span onClick={() => deleteTutorial(rowIdx)}>
                  <i className="fas fa-trash action action_icon"/>
                </span>

                <span onClick={() => addTutorial()}>
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

export default Rooms;