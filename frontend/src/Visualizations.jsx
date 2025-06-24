import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
// You must install chart.js and react-chartjs-2 for these imports to work
import { Bar, Pie, Line } from 'react-chartjs-2';

const Visualizations = ({ data }) => (
  <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
    <Card sx={{ minWidth: 300, flex: 1 }}>
      <CardContent>
        <Typography variant="h6">Applications Over Time</Typography>
        <Line data={data.overTime} />
      </CardContent>
    </Card>
    <Card sx={{ minWidth: 300, flex: 1 }}>
      <CardContent>
        <Typography variant="h6">Status Distribution</Typography>
        <Pie data={data.statusDistribution} />
      </CardContent>
    </Card>
    <Card sx={{ minWidth: 300, flex: 1 }}>
      <CardContent>
        <Typography variant="h6">Calendar View</Typography>
        <Bar data={data.calendar} />
      </CardContent>
    </Card>
  </div>
);

export default Visualizations;
