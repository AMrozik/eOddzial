import React from 'react';
import Query from 'devextreme/data/query';
import { operationsData } from './data.js';

function getOperationsById(id) {
  return Query(operationsData).filter(['id', id]).toArray()[0];
}

export default function Appointment(model) {
  const { targetedAppointmentData } = model.data;

  const operationsData = getOperationsById(targetedAppointmentData.operationsId) || {};

  return (
    <div className="showtime-preview">
      <div> {operationsData.text}</div>
      <div>
        Medic: {operationsData.medic}
      </div>
      <div>
        Patient: {operationsData.patient}
      </div>
      <div>
        Room: {operationsData.room}
      </div>
    </div>
  );
}