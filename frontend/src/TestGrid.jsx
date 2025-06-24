import * as React from 'react';
import { DataGrid } from '@mui/x-data-grid';
const columns = [
  { field: 'id', headerName: 'ID', width: 90 },
  { field: 'name', headerName: 'Name', width: 150 },
];
const rows = [
  { id: 1, name: 'Alice' },
  { id: 2, name: 'Bob' },
];
export default function TestGrid() {
  return (
    <div style={{ width: 400 }}>
      <DataGrid rows={rows} columns={columns} />
    </div>
  );
}