import React from 'react';
import './Footer.css';

export const Footer = () => {
  return (
      <div className="footer">
        &copy; {new Date().getFullYear()} <a href="https://www.nfz.gov.pl/dla-swiadczeniodawcy/slowniki/pliki-icd-9-pl/" className="repo_link"> Government announcement regarding available operations in hospitals </a>
      </div>
  )
};