import React, { useState, useEffect, useMemo, useRef } from "react";
import StatisticsService from "../../services/StatisticsService";
import "../Rooms/Rooms.css";

function textify(nottext) {
 if(nottext) {
  return nottext['bud_mon'] + ', ' + nottext['bud_typy_int'];
 }
}

function textifyBudged(obj){
    if(obj){
        return ([
            <p><strong>Caly w skali wybranych lat:</strong> {obj['bud_rok']} </p>,
            <p><strong>Budzet na wybrane miesiace:</strong> {obj['bud_mon']} </p>,
        ])
    }
}

function textifyPatients(obj){
    if(obj){
        return ([
            <p><strong>Kobiety:</strong> szt.{obj['kob_int']} proc.{obj['kob_proc']}%</p>,
            <p><strong>Mezczyzni:</strong> szt.{obj['men_int']} proc.{obj['men_proc']}%</p>,
            <p><strong>Dzieci:</strong> szt.{obj['dzi_int']} proc.{obj['dzi_proc']}%</p>,
            <p><strong>Trudne:</strong> szt.{obj['tru_int']} proc.{obj['tru_proc']}%</p>,
            <p><strong>Minimalny wiek:</strong> {obj['wiek_min_int']}</p>,
            <p><strong>Maksymalny wiek:</strong> {obj['wiek_max_int']}</p>,
            <p><strong>Sredni wiek:</strong> {obj['wiek_sred']}</p>
        ])
    }
}

function textifyProcedures(obj){
    if(obj){
        const keys = Object.keys(obj['bud_typy_int']);
        var rows = [];
        rows.push(<tr><th>typ</th><th>ilosc</th><th>calkowity koszt</th><th>procentowy koszt</th></tr>)
        for(var i = 0; i<keys.length; i++){
            rows.push(<tr><td>{keys[i]}</td><td>{obj['zab_typy_int'][keys[i]]}</td><td>{obj['bud_typy_int'][keys[i]]}</td><td>{obj['bud_typy_proc'][keys[i]]}%</td></tr>)
        }
        return ([
            <p><strong>Ilosc zabiegow:</strong> {obj['zab']}</p>,
            <p><strong>Wykonane:</strong> szt.{obj['wyk_int']} proc.{obj['wyk_proc']}%</p>,
            <p><strong>Zaplanowane:</strong> szt.{obj['zap_int']} proc.{obj['zap_proc']}%</p>,
            <p><strong>Koszt wykonanych zabiegow:</strong> {obj['wyk_koszt_int']} </p>,
            <p><strong>Koszt wszystkich zabiegow:</strong> {obj['zab_koszt_int']} </p>,
            <tbody>{rows}</tbody>
        ])
    }
}

const Statistics = () => {
  const [stats, setStats] = useState([]);

// Budzet
// bud_mon: 10810000
// bud_rok: 12000000

// Pacjenci
// dzi_int: 0
// dzi_proc: 0
// kob_int: 0
// kob_proc: 0
// men_int: 1
// men_proc: 1
// tru_int: 0
// tru_proc: 0
// wiek_max_int: 2009
// wiek_min_int: 2009
// wiek_sred: 2009

// Zabiegi
// zab: 1
// wyk_int: 1
// wyk_proc: 1
// wyk_koszt_int: 100
// zab_typy_int: Object { 1aw: 1 }
// zab_typy_proc: Object { 1aw: 1 }
// bud_typy_int: Object { 1aw: 100 }
// bud_typy_proc: Object { 1aw: 1 }
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
          setStats(response.data);
        })
        .catch((e) => {
          console.log(e);
        });
  };

  return (
      <div>
        <h1>Statistics</h1>
        <h2>Budzet</h2>
        {textifyBudged(stats[0])}
        <h2>Pacjenci</h2>
        {textifyPatients(stats[0])}
        <h2>Zabiegi</h2>
        {textifyProcedures(stats[0])}
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