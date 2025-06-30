import React from 'react';
import { Box } from '@mui/material';

// A simple component that adds minimal space at the bottom of the application
const BottomSpacer = ({ height = 40 }) => {
  return (
    <Box 
      sx={{ 
        height: `${height}px`, 
        width: '100%', 
        marginTop: '10px', 
        position: 'relative',
      }}
      aria-hidden="true"
      data-testid="bottom-spacer"
    />
  );
};

export default BottomSpacer;
