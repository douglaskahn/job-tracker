import React from 'react';
import { FormControlLabel, Switch, Box, Tooltip, Typography, Badge } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

const DemoToggle = ({ checked, onChange }) => {
  console.log("DemoToggle rendered with checked:", checked);
  
  return (
    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, border: checked ? '2px solid #FF9800' : 'none', padding: checked ? 1 : 0, borderRadius: 1, bgcolor: checked ? 'rgba(255, 152, 0, 0.1)' : 'transparent' }}>
      <FormControlLabel
        control={<Switch checked={checked} onChange={(e) => {
          console.log("DemoToggle switch changed to:", e.target.checked);
          onChange(e);
        }} color="warning" />}
        label={
          <Typography variant="body1" sx={{ fontWeight: checked ? 'bold' : 'normal', color: checked ? '#FF9800' : 'inherit' }}>
            Demo Mode {checked && <Badge color="warning" variant="dot" sx={{ ml: 1 }}/>}
          </Typography>
        }
      />
      <Tooltip title="Toggle between real data and demo data. Demo data includes 50 synthetic job applications with dates from March to June 2025.">
        <InfoIcon fontSize="small" color="action" sx={{ ml: 1, cursor: 'help' }} />
      </Tooltip>
    </Box>
  );
};

export default DemoToggle;
