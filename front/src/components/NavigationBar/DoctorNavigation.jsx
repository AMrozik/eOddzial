import React from 'react'
import './NavigationBar.css';
import {Nav} from 'react-bootstrap';


export const DoctorNavigation = () => {
  return (
      <React.Fragment>
        <Nav.Link className="link_item" href="/operations">Operacje</Nav.Link>
        <Nav.Link className="link_item" href="/patients">Pacjenci</Nav.Link>
      </React.Fragment>
  )
};
