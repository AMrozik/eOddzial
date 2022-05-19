import React from 'react'
import './NavigationBar.css';
import {Nav} from 'react-bootstrap';


export const SecretaryNavigation = () => {
  return (
      <React.Fragment>
        <Nav.Link className="link_item" href="/statistics">Statystyki</Nav.Link>
      </React.Fragment>
  )
};