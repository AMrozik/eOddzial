import React from 'react';
import Scheduler, { Editing, Resource } from 'devextreme-react/scheduler';
import Query from 'devextreme/data/query';

import Appointment from './Appointment.js';
import { data, operationsData} from './data.js';

const currentDate = new Date(2022, 8, 14);
const views = ['day', 'week', 'workWeek', 'month'];
const groups = ['Id'];

class OperationScheduler extends React.Component {
  constructor(props) {
    super(props);
    this.onAppointmentFormOpening = this.onAppointmentFormOpening.bind(this);
  }

  render() {
    return (
      <Scheduler
        timeZone="Poland/Warsaw"
        dataSource={data}
        views={views}
        defaultCurrentView="day"
        defaultCurrentDate={currentDate}
        groups={groups}
        height={600}
        firstDayOfWeek={0}
        startDayHour={6}
        endDayHour={24}
        showAllDayPanel={false}
        crossScrollingEnabled={true}
        appointmentComponent={Appointment}
        onAppointmentFormOpening={this.onAppointmentFormOpening}
      >
        <Editing allowAdding={true} />
        <Resource
          dataSource={operationsData}
          fieldExpr="operationsId"
          useColorAsDefault={true}
        />
      </Scheduler>
    );
  }

  onAppointmentFormOpening(e) {
    const { form } = e;
    let operationsInfo = getOperationsById(e.appointmentData.operationsId) || {};
    let { startDate } = e.appointmentData;

    form.option('items', [{
      label: {
        text: 'Operation',
      },
      editorType: 'dxTextBox',
      dataField: 'operationsId',
      editorOptions: {
        value: operationsInfo.text,

      },
    }, {
      label: {
        text: 'Medic',
      },
      name: 'medic',
      editorType: 'dxTextBox',
      editorOptions: {
        value: operationsInfo.medic,
      },
    },{
      label: {
        text: 'Patient',
      },
      name: 'patient',
      editorType: 'dxTextBox',
      editorOptions: {
        value: operationsInfo.patient,
      },
    },{
      label: {
        text: 'Room',
      },
      name: 'room',
      editorType: 'dxTextBox',
      editorOptions: {
        value: operationsInfo.room,
      },
    }, {
      dataField: 'startDate',
      editorType: 'dxDateBox',
      editorOptions: {
        width: '100%',
        type: 'datetime',
        onValueChanged(args) {
          startDate = args.value;
          form.updateData('endDate', new Date(startDate.getTime() + 60 * 1000 * operationsInfo.duration));
        },
      },
    }
    ]);
  }
}

function getOperationsById(id) {
  return Query(operationsData).filter(['id', id]).toArray()[0];
}

 export default OperationScheduler;