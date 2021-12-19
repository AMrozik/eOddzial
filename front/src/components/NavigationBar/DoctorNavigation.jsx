import React from 'react'
import './NavigationBar.css';
import {Nav} from 'react-bootstrap';


export const DoctorNavigation = () => {
  return (
      <React.Fragment>
        <Nav.Link className="link_item" href="/schedule">Schedule</Nav.Link>
        <Nav.Link className="link_item" href="/patients">Patients</Nav.Link>
      </React.Fragment>
  )
};
