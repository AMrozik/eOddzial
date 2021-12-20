import React from 'react'
import './NavigationBar.css';
import {Nav} from 'react-bootstrap';


export const HeadPhysicianNavigation = () => {
  return (
      <React.Fragment>
          <Nav.Link className="link_item" href="/schedule">Schedule</Nav.Link>
          <Nav.Link className="link_item" href="/budget">Budget</Nav.Link>
          <Nav.Link className="link_item" href="/working_hours">Working hours</Nav.Link>
          <Nav.Link className="link_item" href="/patients">Patients</Nav.Link>
          <Nav.Link className="link_item" href="/operation_types">Operation types</Nav.Link>
          <Nav.Link className="link_item" href="/rooms">Rooms</Nav.Link>
<<<<<<< HEAD
=======
          <Nav.Link className="link_item" href="/add_room">Add Room</Nav.Link>
>>>>>>> 90db70cf8106d62f5e72c4f8845037e80487f438
          <Nav.Link className="link_item" href="/statistics">Statistics</Nav.Link>
      </React.Fragment>
  )
};
