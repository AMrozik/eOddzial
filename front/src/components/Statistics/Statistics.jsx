import React, {useState, useEffect, useMemo, useRef} from "react";
import StatisticsService from "../../services/StatisticsService";

function textify(nottext) {
    if (nottext) {
        return nottext['bud_mon'] + ', ' + nottext['bud_typy_int'];
    }
}

function textifyBudged(obj) {
    if (obj) {
        return ([
            <table className="table table-striped table-bordered">
            <tbody>
            <tr>
                <th><strong>Caly w skali wybranych lat:</strong></th>
                <td> {obj['bud_rok']} </td>
            </tr>
            <tr>
                <th><strong>Budzet na wybrane miesiace:</strong></th>
                <td> {obj['bud_mon']} </td>
            </tr>
            </tbody>
            </table>
        ])
    }
}

function textifyPatients(obj) {
    if (obj) {
        return ([
            <table className="table table-striped table-bordered">
            <tbody>
            <tr>
                <th><strong>Kobiety:</strong></th>
                <td> szt.{obj['kob_int']} proc.{obj['kob_proc']}%</td>
            </tr>
            <tr>
                <th><strong>Mezczyzni:</strong></th>
                <td> szt.{obj['men_int']} proc.{obj['men_proc']}%</td>
            </tr>
            <tr>
                <th><strong>Dzieci:</strong></th>
                <td> szt.{obj['dzi_int']} proc.{obj['dzi_proc']}%</td>
            </tr>
            <tr>
                <th><strong>Trudne:</strong></th>
                <td> szt.{obj['tru_int']} proc.{obj['tru_proc']}%</td>
            </tr>
            <tr>
                <th><strong>Minimalny wiek:</strong></th>
                <td> {obj['wiek_min_int']} </td>
            </tr>
            <tr>
                <th><strong>Maksymalny wiek:</strong></th>
                <td> {obj['wiek_max_int']} </td>
            </tr>
            <tr>
                <th><strong>Sredni wiek:</strong></th>
                <td> {obj['wiek_sred']} </td>
            </tr>
            </tbody>
            </table>
        ])
    }
}

function textifyProcedures(obj) {
    if (obj) {
        const keys = Object.keys(obj['bud_typy_int']);
        var rows = [];
        rows.push(<tr>
            <th>typ</th>
            <th>ilosc</th>
            <th>calkowity koszt</th>
            <th>procentowy koszt</th>
        </tr>)
        for (var i = 0; i < keys.length; i++) {
            rows.push(<tr>
                <td>{keys[i]}</td>
                <td>{obj['zab_typy_int'][keys[i]]}</td>
                <td>{obj['bud_typy_int'][keys[i]]}</td>
                <td>{obj['bud_typy_proc'][keys[i]]}%</td>
            </tr>)
        }
        return ([
            <table className="table table-striped table-bordered">
            <tbody>
            <tr>
                <th><strong>Ilosc zabiegow:</strong></th>
                <td> {obj['zab']} </td>
            </tr>
            <tr>
                <th><strong>Wykonane:</strong></th>
                <td> szt.{obj['wyk_int']} proc.{obj['wyk_proc']}%</td>
            </tr>
            <tr>
                <th><strong>Zaplanowane:</strong></th>
                <td> szt.{obj['zap_int']} proc.{obj['zap_proc']}%</td>
            </tr>
            <tr>
                <th><strong>Koszt wykonanych zabiegow:</strong></th>
                <td> {obj['wyk_koszt_int']}</td>
            </tr>
            <tr>
                <th><strong>Koszt wszystkich zabiegow:</strong></th>
                <td> {obj['zab_koszt_int']} </td>
            </tr>
            </tbody>
            </table>,

            <table className="table table-striped table-bordered">
            <tbody>{rows}</tbody>
            </table>
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
        <div className="col-md-12 list table_style">
            <h1> Statystyki </h1>
            <div className="stat_table">
                <p><strong>Budżet</strong></p>
                {textifyBudged(stats[0])}
            </div>
            <div className="stat_table">
                <p><strong>Pacjenci</strong></p>
                {textifyPatients(stats[0])}
            </div>
            <div className="stat_table">
                <p><strong>Zabiegi</strong></p>
                {textifyProcedures(stats[0])}
            </div>
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