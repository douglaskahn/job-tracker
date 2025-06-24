import React from 'react';
import { createRoot } from 'react-dom/client';
import { Button, Box, Typography } from '@mui/material';
import axios from 'axios';

// Simple test component to verify demo API calls
const TestDemoAPI = () => {
  const [demoData, setDemoData] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);

  const fetchDemoData = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log("Fetching demo data from http://localhost:8005/demo/applications/");
      const response = await axios.get('http://localhost:8005/demo/applications/');
      console.log("Demo data response:", response.data);
      setDemoData(response.data);
    } catch (err) {
      console.error("Error fetching demo data:", err);
      setError(err.message || "Failed to fetch demo data");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>Demo API Test</Typography>
      <Button 
        variant="contained" 
        color="primary" 
        onClick={fetchDemoData}
        disabled={loading}
        sx={{ mb: 2 }}
      >
        {loading ? 'Loading...' : 'Fetch Demo Data'}
      </Button>

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          Error: {error}
        </Typography>
      )}

      {demoData && (
        <Box>
          <Typography variant="h6" gutterBottom>
            Received {demoData.length} demo records
          </Typography>
          <Box sx={{ maxHeight: '400px', overflow: 'auto', border: '1px solid #ccc', p: 2 }}>
            <pre>{JSON.stringify(demoData.slice(0, 5), null, 2)}</pre>
          </Box>
        </Box>
      )}
    </Box>
  );
};

// Find or create a root element
const rootElement = document.getElementById('demo-test-root') || (() => {
  const el = document.createElement('div');
  el.id = 'demo-test-root';
  document.body.appendChild(el);
  return el;
})();

// Render the test component
createRoot(rootElement).render(<TestDemoAPI />);
