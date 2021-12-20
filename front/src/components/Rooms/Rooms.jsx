import React, { useState, useEffect, useMemo, useRef } from "react";
import RoomServicw from "../../services/RoomService";
import { useTable } from "react-table";
import "./Rooms.css";

const Rooms = (props) => {
  const [rooms, setRooms] = useState([]);
  const roomsRef = useRef();

  roomsRef.current = rooms;

  useEffect(() => {
    retriveRooms();
  }, []);

  const retriveRooms = () => {
    RoomServicw.getAll()
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
    RoomServicw.removeAll()
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

    RoomServicw.remove(id)
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