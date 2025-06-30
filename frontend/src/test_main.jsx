import React from 'react';
import ReactDOM from 'react-dom/client';

const TestApp = () => {
  return (
    <div>
      <h1>Test App</h1>
      <p>This is a test to see if the basic React setup works.</p>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <TestApp />
  </React.StrictMode>
);
