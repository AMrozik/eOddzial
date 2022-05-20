import React from 'react';
import './Footer.css';

export const Footer = () => {
  return (
      <div className="footer">
        &copy; {new Date().getFullYear()} <a href="https://www.nfz.gov.pl/dla-swiadczeniodawcy/slowniki/pliki-icd-9-pl/" className="repo_link"> Ogłoszenie rządu dotyczące dostępnych operacji w szpitalach </a>
      </div>
  )
};