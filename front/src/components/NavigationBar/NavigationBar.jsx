import React, {useContext} from 'react'
import {Route, Routes} from 'react-router-dom'
import AuthContext from '../../AuthContext'
import './NavigationBar.css';
import {Nav, Navbar} from 'react-bootstrap';
import {HeadPhysicianNavigation} from "./HeadPhysicianNavigation";
import {DoctorNavigation} from "./DoctorNavigation";
import {PlanistNavigation} from "./PlanistNavigation";
import {SecretaryNavigation} from "./SecretaryNavigation";
import PrivateRoute from '../../PrivateRoute';
import Login from '../Login/Login';
import Logout from '../Login/Logout';
import Operation from "../Operations/Operation"
import OperationDateSearch from "../Operations/OperationDateSearch";
import AddOperation from "../Operations/AddOperation"
import EditOperation from "../Operations/EditOperation"
import Statistics from "../Statistics/Statistics";
import Patients from "../Patients/Patients";
import EditPatient from "../Patients/EditPatient";
import AddPatients from "../Patients/AddPatients";
import Medics from "../Medics/Medics";
import MedicsBreaks from "../Medics/Breaks/MedicsBreaks";
import EditMedicBreak from "../Medics/Breaks/EditMedicBreak";
import AddMedicBreak from "../Medics/Breaks/AddMedicBreak";
import Rooms from "../Rooms/Rooms";
import EditRoom from "../Rooms/EditRoom";
import AddRoom from "../Rooms/AddRoom";
import RoomsBreaks from "../Rooms/Breaks/RoomsBreaks";
import EditRoomBreak from "../Rooms/Breaks/EditRoomBreak";
import AddRoomBreak from "../Rooms/Breaks/AddRoomBreak";
import Types from "../OperationTypes/Types";
import EditType from "../OperationTypes/EditType";
import AddType from "../OperationTypes/AddType";
import Budgets from "../BudgetYears/Budgets";
import EditBudget from "../BudgetYears/EditBudget";
import AddBudget from "../BudgetYears/AddBudget";
import WardData from "../WardData/WardData";
import AddWardData from "../WardData/AddWardData";


export const NavigationBar = () => {
  let {user, logoutUser} = useContext(AuthContext)
  let NavigationLinks;
  let SignInOutNavigation;



  if (user && user.is_ordynator) {
    NavigationLinks = <HeadPhysicianNavigation/>
  } else if (user && user.is_medic) {
    NavigationLinks = <DoctorNavigation/>
  } else if (user && user.is_planist) {
    NavigationLinks = <PlanistNavigation/>
  } else if (user && user.is_secretary) {
    NavigationLinks = <SecretaryNavigation/>
  }
  if (user) {
    SignInOutNavigation = <Nav.Link className="link_item" onClick={logoutUser} href="/logout">Wyloguj</Nav.Link>
  } else {
    SignInOutNavigation = <Nav.Link className="link_item" href="/login">Zaloguj</Nav.Link>
  }

  return (
      <div className="content">
            <Navbar bg="dark" variant="dark" expand="lg" sticky="top" className="navbar">
              <Navbar.Toggle aria-controls="basic-navbar-nav"/>
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">

                  <div className="float_container">

                  {NavigationLinks}

                  {SignInOutNavigation}
                  </div>

                </Nav>
              </Navbar.Collapse>
            </Navbar>
            <br/>
            <Routes>
              <Route path="/operations" exact element={<PrivateRoute/>}>
                <Route path="/operations" exact element={<Operation/>}/>
              </Route>
              <Route path="/statistics" exact element={<PrivateRoute/>}>
                <Route path="/statistics" exact element={<Statistics/>}/>
              </Route>
              <Route path="/patients" exact element={<PrivateRoute/>}>
                <Route path="/patients" exact element={<Patients/>}/>
              </Route>
              <Route path="/medics" exact element={<PrivateRoute/>}>
                <Route path="/medics" exact element={<Medics/>}/>
              </Route>
              <Route path="/rooms" exact element={<PrivateRoute/>}>
                <Route path="/rooms" exact element={<Rooms/>}/>
              </Route>
              <Route path="/operation_types" exact element={<PrivateRoute/>}>
                <Route path="/operation_types" exact element={<Types/>}/>
              </Route>
              <Route path="/budget_years" exact element={<PrivateRoute/>}>
                <Route path="/budget_years" exact element={<Budgets/>}/>
              </Route>
              <Route path="/wardData" exact element={<PrivateRoute/>}>
                <Route path="/wardData" exact element={<WardData/>}/>
              </Route>

              <Route path="/operation_date_search/:date" exact element={<PrivateRoute/>}>
                <Route path="/operation_date_search/:date" exact element={<OperationDateSearch/>}/>
              </Route>
              <Route path="/add_operation/:date" exact element={<PrivateRoute/>}>
                <Route path="/add_operation/:date" exact element={<AddOperation/>}/>
              </Route>
              <Route path="/operations/:id" exact element={<PrivateRoute/>}>
                <Route path="/operations/:id" exact element={<EditOperation/>}/>
              </Route>
              <Route path="/operation/" exact element={<PrivateRoute/>}>
                <Route path="/operation/" exact element={<Operation/>}/>
              </Route>

              <Route path="/add_room" exact element={<PrivateRoute/>}>
                <Route path="/add_room" exact element={<AddRoom/>}/>
              </Route>
              <Route path="/room/:id" exact element={<PrivateRoute/>}>
                <Route path="/room/:id" exact element={<EditRoom/>}/>
              </Route>
              <Route path="/rooms_breaks" exact element={<PrivateRoute/>}>
                <Route path="/rooms_breaks" exact element={<RoomsBreaks/>}/>
              </Route>
              <Route path="/add_room_break/:id" exact element={<PrivateRoute/>}>
                <Route path="/add_room_break/:id" exact element={<AddRoomBreak/>}/>
              </Route>
              <Route path="/room_break/:id" exact element={<PrivateRoute/>}>
                <Route path="/room_break/:id" exact element={<EditRoomBreak/>}/>
              </Route>

              <Route path="/medics_breaks" exact element={<PrivateRoute/>}>
                <Route path="/medics_breaks" exact element={<MedicsBreaks/>}/>
              </Route>
              <Route path="/add_medic_break/:id" exact element={<PrivateRoute/>}>
                <Route path="/add_medic_break/:id" exact element={<AddMedicBreak/>}/>
              </Route>
              <Route path="/medic_break/:id" exact element={<PrivateRoute/>}>
                <Route path="/medic_break/:id" exact element={<EditMedicBreak/>}/>
              </Route>

              <Route path="/add_patient" exact element={<PrivateRoute/>}>
                <Route path="/add_patient" exact element={<AddPatients/>}/>
              </Route>
              <Route path="/patient/:id" exact element={<PrivateRoute/>}>
                <Route path="/patient/:id" exact element={<EditPatient/>}/>
              </Route>

              <Route path="/add_type" exact element={<PrivateRoute/>}>
                <Route path="/add_type" exact element={<AddType/>}/>
              </Route>
              <Route path="/type/:id" exact element={<PrivateRoute/>}>
                <Route path="/type/:id" exact element={<EditType/>}/>
              </Route>

              <Route path="/add_budget_year" exact element={<PrivateRoute/>}>
                <Route path="/add_budget_year" exact element={<AddBudget/>}/>
              </Route>
              <Route path="/budget_year/:year" exact element={<PrivateRoute/>}>
                <Route path="/budget_year/:year" exact element={<EditBudget/>}/>
              </Route>

              <Route path="/add_ward_data" exact element={<PrivateRoute/>}>
                <Route path="/add_ward_data" exact element={<AddWardData/>}/>
              </Route>

              <Route path="/login" element={<Login/>}/>
              <Route path="/logout" element={<Logout/>}/>
            </Routes>
      </div>
  )
};
