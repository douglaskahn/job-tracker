import React from 'react';
import { Typography, Box } from '@mui/material';

const Dashboard = () => (
  <Box p={3}>
    <Typography variant="h4" gutterBottom>
      Job Application Tracker Dashboard
    </Typography>
    <Typography>
      Welcome! Use the sidebar to navigate between applications, visualizations, and settings.
    </Typography>
  </Box>
);

export default Dashboard;
