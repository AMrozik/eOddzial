import React from 'react';

import Scheduler, {Resource} from 'devextreme-react/scheduler';

import {data, isSevereData, operationTypeData, operatorData, patientData, roomData} from './data.js';

const currentDate = new Date(2021, 3, 29);
const views = ['day', 'week', 'workWeek', 'month'];

class OperationScheduler extends React.Component {
  render() {
    return (
        <Scheduler
            timeZone="America/Los_Angeles"
            dataSource={data}
            views={views}
            defaultCurrentView="week"
            defaultCurrentDate={currentDate}
            height={600}
            startDayHour={9}
        >
          <Resource
              dataSource={patientData}
              fieldExpr="patientDataId"
              label="Patient"
              allowMultiple={false}
          />
          <Resource
              dataSource={operationTypeData}
              fieldExpr="operationTypeDataId"
              label="Operation type"
              allowMultiple={false}
          />
          <Resource
              dataSource={operatorData}
              fieldExpr="operatorDataId"
              label="Operator"
              allowMultiple={false}
          />
          <Resource
              dataSource={roomData}
              fieldExpr="roomDataId"
              label="Room"
              allowMultiple={false}
          />
        </Scheduler>
    );
  }

}

export default OperationScheduler;