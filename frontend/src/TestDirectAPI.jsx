import React from 'react';
import { createRoot } from 'react-dom/client';
import { Button, Box, Typography } from '@mui/material';
import axios from 'axios';

// Test component that makes direct API calls
const TestDirectAPI = () => {
  const [result, setResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  const testDemoEndpoint = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log("Testing direct call to demo endpoint");
      const response = await axios.get('http://localhost:8005/demo/applications/');
      console.log("Direct demo API response:", response.data);
      setResult({
        endpoint: '/demo/applications/',
        count: response.data.length,
        sample: response.data.slice(0, 5)
      });
    } catch (err) {
      console.error("Error with direct API call:", err);
      setError(err.message || "Failed to fetch from demo endpoint");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3, position: 'fixed', top: 0, right: 0, width: '40%', bgcolor: '#f5f5f5', boxShadow: 3, zIndex: 9999, maxHeight: '80vh', overflow: 'auto' }}>
      <Typography variant="h5" gutterBottom>Direct API Test</Typography>
      <Button 
        variant="contained" 
        color="primary" 
        onClick={testDemoEndpoint}
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? 'Loading...' : 'Test Demo Endpoint Directly'}
      </Button>

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error: {error}
        </Typography>
      )}

      {result && (
        <Box>
          <Typography variant="h6" gutterBottom>
            Result from {result.endpoint}
          </Typography>
          <Typography>
            Received {result.count} records
          </Typography>
          <Box sx={{ maxHeight: '300px', overflow: 'auto', border: '1px solid #ccc', p: 2, mt: 2 }}>
            <pre>{JSON.stringify(result.sample, null, 2)}</pre>
          </Box>
        </Box>
      )}
    </Box>
  );
};

// Create and insert the component
const rootElement = document.createElement('div');
document.body.appendChild(rootElement);
createRoot(rootElement).render(<TestDirectAPI />);
