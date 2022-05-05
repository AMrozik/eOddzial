import React, { useState, useEffect, useMemo, useRef } from "react";
import StatisticsService from "../../services/StatisticsService";
import { useTable } from "react-table";
import "../Rooms/Rooms.css"; //Maybe this css will be universal

function textify(nottext) {
 if(nottext) {
  return nottext['bud_mon'] + ', ' + nottext['bud_typy_int'];
 }
}

const Statistics = () => {
  const [stats, setStats] = useState([]);

// bud_mon: 10810000
// bud_rok: 12000000
// bud_typy_int: Object { 1aw: 100 }
// bud_typy_proc: Object { 1aw: 1 }
// dzi_int: 0
// dzi_proc: 0
// kob_int: 0
// kob_proc: 0
// men_int: 1
// men_proc: 1
// nie_wyk_int: 1
// nie_wyk_proc: 1
// tru_int: 0
// tru_proc: 0
// wiek_max_int: 2009
// wiek_min_int: 2009
// wiek_sred: 2009
// wyk_int: 1
// wyk_koszt_int: 100
// wyk_proc: 1
// zab: 1
// zab_typy_int: Object { 1aw: 1 }
// zab_typy_proc: Object { 1aw: 1 }
// zap_int: 0
// zap_proc: 0

//   const roomsRef = useRef();
//
//   roomsRef.current = rooms;

  useEffect(() => {
    retriveStats();
  }, []);

  const retriveStats = () => {
    StatisticsService.getAll()
        .then((response) => {
          console.log(response.data);
          setStats(response.data);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  return (
      <div>
        <p>Statistics</p>
        <p>{console.log(stats[0])}</p>
        <p>{textify(stats[0])}</p>
      </div>
        //<div className="col-md-12 list table_style">
        //  <table
        //      className="table table-striped table-bordered"
        //      {...getTableProps()}
        //  >
        //    <thead>
        //    {headerGroups.map((headerGroup) => (
        //        <tr {...headerGroup.getHeaderGroupProps()}>
        //          {headerGroup.headers.map((column) => (
        //              <th {...column.getHeaderProps()}>
        //                {column.render("Header")}
        //              </th>
        //          ))}
        //        </tr>
        //    ))}
        //    </thead>
        //    <tbody {...getTableBodyProps()}>
        //    {rows.map((row, i) => {
        //      prepareRow(row);
        //      return (
        //          <tr {...row.getRowProps()}>
        //            {row.cells.map((cell) => {
        //              return (
        //                  <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
        //              );
        //            })}
        //          </tr>
        //      );
        //    })}
        //    </tbody>
        //  </table>
        //</div>
  )//
}

export default Statistics;