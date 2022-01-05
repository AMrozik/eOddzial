import React from 'react';

import Scheduler, {Resource} from 'devextreme-react/scheduler';

import { data, isSevereData } from './data.js';

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
              dataSource={isSevereData}
              fieldExpr="isSevereDataId"
              label="isSevere"
              allowMultiple={false}
          />
        </Scheduler>
    );
  }

}

export default OperationScheduler;