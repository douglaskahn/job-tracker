import React from 'react';
import Visualizations from '../Visualizations';

const VisualizationsPage = ({ data }) => (
  <div>
    <h2>Visualizations</h2>
    <Visualizations data={data} />
  </div>
);

export default VisualizationsPage;
