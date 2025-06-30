/**
 * AppProviders.jsx
 * Wrapper component for all application context providers
 */

import React from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { ApplicationProvider } from './context/ApplicationContext';
import theme from './theme';

const AppProviders = ({ children }) => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <ApplicationProvider>
        {children}
      </ApplicationProvider>
    </ThemeProvider>
  );
};

export default AppProviders;
