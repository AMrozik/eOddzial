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
import OperationScheduler from "../OperationScheduler/OperationScheduler";
import Statistics from "../Statistics/Statistics";
import Patients from "../Patients/Patients";
import EditPatient from "../Patients/Patient";
import AddPatients from "../Patients/AddPatients";
import Medics from "../Medics/Medics";
import Rooms from "../Rooms/Rooms";
import EditRoom from "../Rooms/Room";
import AddRoom from "../Rooms/AddRoom";
import OperationTypes from "../OperationTypes/OperationTypes";
import WardData from "../WardData/WardData";


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
      <div className="navigation_style">
        <div className="row">
          <div className="col-md-12">
            <Navbar bg="dark" variant="dark" expand="lg" sticky="top">
              <Navbar.Toggle aria-controls="basic-navbar-nav"/>
              <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">

                  {NavigationLinks}

                  {SignInOutNavigation}

                </Nav>
              </Navbar.Collapse>
            </Navbar>
            <br/>
            <Routes>
              <Route path="/schedule" exact element={<PrivateRoute/>}>
                <Route path="/schedule" exact element={<OperationScheduler/>}/>
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
                <Route path="/operation_types" exact element={<OperationTypes/>}/>
              </Route>
              <Route path="/wardData" exact element={<PrivateRoute/>}>
                <Route path="/wardData" exact element={<WardData/>}/>
              </Route>

{/*                Routing is weird in this project */}
              <Route path="/add_room" exact element={<PrivateRoute/>}>
                <Route path="/add_room" exact element={<AddRoom/>}/>
              </Route>
              <Route path="/room/:id" exact element={<PrivateRoute/>}>
                <Route path="/room/:id" exact element={<EditRoom/>}/>
              </Route>

              <Route path="/create_patient" exact element={<PrivateRoute/>}>
                <Route path="/create_patient" exact element={<AddPatients/>}/>
              </Route>
              <Route path="/patient/:id" exact element={<PrivateRoute/>}>
                <Route path="/patient/:id" exact element={<EditPatient/>}/>
              </Route>

              <Route path="/login" element={<Login/>}/>
              <Route path="/logout" element={<Logout/>}/>
            </Routes>
          </div>
        </div>
      </div>
  )
};
