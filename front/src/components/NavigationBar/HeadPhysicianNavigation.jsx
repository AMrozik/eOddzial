import React from 'react'
import './NavigationBar.css';
import {Nav} from 'react-bootstrap';


export const HeadPhysicianNavigation = () => {
  return (
      <React.Fragment>
          <Nav.Link className="link_item" href="/schedule">Plan</Nav.Link>
          <Nav.Link className="link_item" href="/statistics">Statystyki</Nav.Link>
          <Nav.Link className="link_item" href="/patients">Pacjenci</Nav.Link>
          <Nav.Link className="link_item" href="/medics">Lekarze</Nav.Link>
          <Nav.Link className="link_item" href="/rooms">Pokoje</Nav.Link>
          <Nav.Link className="link_item" href="/operation_types">Typy operacji</Nav.Link>
          <Nav.Link className="link_item" href="/wardData">Konfiguracja</Nav.Link>
      </React.Fragment>
  )
};
