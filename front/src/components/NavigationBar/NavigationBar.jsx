import React, {useContext} from 'react'
import {Route, Routes} from 'react-router-dom'
import AuthContext from '../../AuthContext'
import './NavigationBar.css';
import {Nav, Navbar} from 'react-bootstrap';
import Login from '../Login/Login';
import Logout from '../Login/Logout';
import PrivateRoute from '../../PrivateRoute';
import {HeadPhysicianNavigation} from "./HeadPhysicianNavigation";
import OperationScheduler from "../OperationScheduler/OperationScheduler";
import Budget from "../Budget/Budget";
import WorkingHours from "../WorkingHours/WorkingHours";
import Patients from "../Patients/Patients";
import OperationTypes from "../OperationTypes/OperationTypes";
import Rooms from "../Rooms/Rooms";
import Statistics from "../Statistics/Statistics";
import {DoctorNavigation} from "./DoctorNavigation";
import {PlanistNavigation} from "./PlanistNavigation";
import {SecretaryNavigation} from "./SecretaryNavigation";
import AddRoom from "../Rooms/AddRoom";
import EditRoom from "../Rooms/EditRoom";
import Room from "../Rooms/Room";
import AddPatient from "../Patients/AddPatient";


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
    SignInOutNavigation = <Nav.Link className="link_item" onClick={logoutUser} href="/logout">Sign out</Nav.Link>
  } else {
    SignInOutNavigation = <Nav.Link className="link_item" href="/login"/>
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
              <Route path="/budget" exact element={<PrivateRoute/>}>
                <Route path="/budget" exact element={<Budget/>}/>
              </Route>
              <Route path="/working_hours" exact element={<PrivateRoute/>}>
                <Route path="/working_hours" exact element={<WorkingHours/>}/>
              </Route>
              <Route path="/patients" exact element={<PrivateRoute/>}>
                <Route path="/patients" exact element={<Patients/>}/>
              </Route>
              <Route path="/add_patient" exact element={<PrivateRoute/>}>
                <Route path="/add_patient" exact element={<AddPatient/>}/>
              </Route>
              <Route path="/operation_types" exact element={<PrivateRoute/>}>
                <Route path="/operation_types" exact element={<OperationTypes/>}/>
              </Route>
              <Route path="/rooms" exact element={<PrivateRoute/>}>
                <Route path="/rooms" exact element={<Rooms/>}/>
              </Route>
              <Route path="/add_room" exact element={<PrivateRoute/>}>
                <Route path="/add_room" exact element={<AddRoom/>}/>
              </Route>
              <Route path="/edit_room" exact element={<PrivateRoute/>}>
                <Route path="/edit_room" exact element={<EditRoom/>}/>
              </Route>
              <Route path="/room/" exact element={<PrivateRoute/>}>
                <Route path="/room/" exact element={<Room/>}/>
              </Route>
              <Route path="/statistics" exact element={<PrivateRoute/>}>
                <Route path="/statistics" exact element={<Statistics/>}/>
              </Route>
              <Route path="/login" element={<Login/>}/>
              <Route path="/logout" element={<Logout/>}/>
            </Routes>
          </div>
        </div>
      </div>
  )
};
