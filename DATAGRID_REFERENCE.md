# DataGrid Component Reference

This document provides standardized implementation patterns for the Material UI DataGrid component in the Job Tracker application.

## Table of Contents
1. [Basic Configuration](#basic-configuration)
2. [External Controls](#external-controls)
3. [Custom Toolbar](#custom-toolbar)
4. [Custom Footer](#custom-footer)
5. [Column Definitions](#column-definitions)
6. [Document Icons](#document-icons)
7. [Styling Patterns](#styling-patterns)
8. [Performance Optimizations](#performance-optimizations)

## Basic Configuration

The standard configuration for our DataGrids:

```jsx
import { DataGrid } from '@mui/x-data-grid';

function BasicJobGrid({ rows }) {
  return (
    <DataGrid
      rows={rows}
      columns={columns}
      initialState={{
        pagination: {
          paginationModel: { page: 0, pageSize: 10 },
        },
        sorting: {
          sortModel: [{ field: 'created_at', sort: 'desc' }],
        },
      }}
      pageSizeOptions={[5, 10, 25]}
      checkboxSelection={false}
      disableRowSelectionOnClick
      autoHeight
    />
  );
}
```

## External Controls

Simple pattern for integrating external controls with the DataGrid:

```jsx
import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';

export default function JobGridWithExternalControls() {
  const [status, setStatus] = React.useState('');
  
  // Simple filter based on status
  const filteredRows = React.useMemo(() => {
    if (!status) return rows;
    return rows.filter(row => row.status === status);
  }, [rows, status]);
  
  const handleReset = () => {
    setStatus('');
  };
  
  return (
    <Box sx={{ width: '100%' }}>
      {/* Simple external controls */}
      <Box sx={{ mb: 2, display: 'flex', gap: 2, alignItems: 'center' }}>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={status}
            label="Status"
            onChange={(e) => setStatus(e.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            <MenuItem value="Applied">Applied</MenuItem>
            <MenuItem value="Interviewing">Interviewing</MenuItem>
            {/* Other status options */}
          </Select>
        </FormControl>
        
        <Box sx={{ flexGrow: 1 }} />
        
        <Button
          variant="outlined"
          onClick={handleReset}
        >
          Reset Filters
        </Button>
      </Box>
      
      {/* DataGrid with filtered data */}
      <DataGrid
        rows={filteredRows}
        columns={columns}
        // Other props as needed
      />
    </Box>
  );
}
```

## Custom Toolbar

Implementing a custom toolbar with search functionality:

```jsx
import * as React from 'react';
import {
  DataGrid,
  GridToolbarContainer,
  GridToolbarColumnsButton,
  GridToolbarFilterButton,
  GridToolbarExportButton,
} from '@mui/x-data-grid';
import { TextField, IconButton, Box } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';

function CustomToolbar(props) {
  return (
    <GridToolbarContainer>
      <GridToolbarColumnsButton />
      <GridToolbarFilterButton />
      <GridToolbarExportButton />
      
      <Box sx={{ flexGrow: 1 }} />
      
      <TextField
        variant="outlined"
        size="small"
        placeholder="Search..."
        value={props.value}
        onChange={props.onChange}
        InputProps={{
          startAdornment: <SearchIcon fontSize="small" sx={{ mr: 1 }} />,
          endAdornment: props.value && (
            <IconButton
              size="small"
              onClick={() => props.onChange({ target: { value: '' } })}
            >
              <ClearIcon fontSize="small" />
            </IconButton>
          )
        }}
      />
    </GridToolbarContainer>
  );
}

export default function JobGridWithSearch() {
  const [searchText, setSearchText] = React.useState('');
  
  const handleSearchChange = (event) => {
    setSearchText(event.target.value);
  };
  
  const filteredRows = React.useMemo(() => {
    if (!searchText) return rows;
    
    return rows.filter(row => 
      Object.entries(row).some(([key, value]) => {
        if (typeof value !== 'string') return false;
        return value.toLowerCase().includes(searchText.toLowerCase());
      })
    );
  }, [rows, searchText]);
  
  return (
    <DataGrid
      rows={filteredRows}
      columns={columns}
      slots={{
        toolbar: CustomToolbar,
      }}
      slotProps={{
        toolbar: {
          value: searchText,
          onChange: handleSearchChange,
        },
      }}
    />
  );
}
```

## Custom Footer

Custom footer with status indicator:

```jsx
import * as React from 'react';
import Box from '@mui/material/Box';
import { DataGrid } from '@mui/x-data-grid';
import FiberManualRecordIcon from '@mui/icons-material/FiberManualRecord';

function CustomFooterComponent(props) {
  return (
    <Box sx={{ p: 1, display: 'flex', justifyContent: 'space-between' }}>
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <FiberManualRecordIcon
          fontSize="small"
          sx={{
            mr: 1,
            color: props.status === 'connected' ? '#4caf50' : '#d9182e',
          }}
        />
        Status: {props.status}
      </Box>
      
      <Box>
        Total Records: {props.rowCount}
      </Box>
    </Box>
  );
}

export default function JobGridWithCustomFooter() {
  const [status, setStatus] = React.useState('connected');
  
  return (
    <Box sx={{ width: '100%', height: 400 }}>
      <DataGrid
        rows={rows}
        columns={columns}
        slots={{
          footer: CustomFooterComponent,
        }}
        slotProps={{
          footer: { 
            status,
            rowCount: rows.length
          },
        }}
      />
    </Box>
  );
}
```

## Column Definitions

Standard column definitions for our application:

```jsx
import { 
  VisibilityIcon, 
  EditIcon, 
  DeleteIcon, 
  NotificationImportantIcon,
  PictureAsPdfIcon,
  ArticleIcon,
  DescriptionIcon
} from '@mui/icons-material';
const columns = [
  // Basic text column
  { 
    field: 'company', 
    headerName: 'Company', 
    width: 180,
    flex: 1 
  },
  
  // Status column with chip
  { 
    field: 'status', 
    headerName: 'Status', 
    width: 140,
    renderCell: (params) => (
      <Chip 
        label={params.value} 
        color={getStatusColor(params.value)} 
        size="small" 
      />
    ),
  },
  
  // Date column with formatting
  { 
    field: 'application_date', 
    headerName: 'Date Applied', 
    width: 120,
    valueFormatter: (params) => {
      if (!params.value) return '';
      return new Date(params.value).toLocaleDateString();
    },
  },
  
  // URL column with link
  { 
    field: 'url', 
    headerName: 'Job Posting', 
    width: 120,
    renderCell: (params) => 
      params.value ? (
        <Link href={params.value} target="_blank" rel="noopener">
          View Job
        </Link>
      ) : (
        <span style={{ color: '#aaa' }}>N/A</span>
      ),
  },
  
  // Document links with icons
  { 
    field: 'resume_path', 
    headerName: 'Resume', 
    width: 100,
    renderCell: (params) => {
      if (!params.value) return <span style={{ color: '#aaa' }}>N/A</span>;
      
      const fileExtension = params.value.split('.').pop().toLowerCase();
      
      // Choose icon based on file extension
      let icon = <DescriptionIcon fontSize="small" />;  // Default document icon
      if (fileExtension === 'pdf') {
        icon = <PictureAsPdfIcon fontSize="small" color="error" />;
      } else if (['doc', 'docx'].includes(fileExtension)) {
        icon = <ArticleIcon fontSize="small" color="primary" />;
      }
      
      return (
        <Tooltip title={`Open ${fileExtension.toUpperCase()} file`}>
          <IconButton
            size="small"
            onClick={() => window.open(params.value, '_blank')}
          >
            {icon}
          </IconButton>
        </Tooltip>
      );
    },
  },
  
  // Boolean column with icon
  { 
    field: 'follow_up_required', 
    headerName: 'Follow Up', 
    width: 120,
    type: 'boolean',
    renderCell: (params) => 
      params.value ? (
        <Tooltip title="Follow-up required">
          <NotificationImportantIcon color="warning" />
        </Tooltip>
      ) : null,
  },
  
  // Actions column
  { 
    field: 'actions', 
    headerName: 'Actions', 
    width: 120,
    sortable: false,
    renderCell: (params) => (
      <Box sx={{ display: 'flex', gap: 1 }}>
        <IconButton 
          size="small" 
          onClick={() => handleView(params.row)}
          color="primary"
        >
          <VisibilityIcon fontSize="small" />
        </IconButton>
        <IconButton 
          size="small" 
          onClick={() => handleEdit(params.row)}
          color="primary"
        >
          <EditIcon fontSize="small" />
        </IconButton>
        <IconButton 
          size="small" 
          onClick={() => handleDelete(params.row)}
          color="error"
        >
          <DeleteIcon fontSize="small" />
        </IconButton>
      </Box>
    ),
  },
];
```

## Styling Patterns

### Button Styling Standards

```jsx
// Primary action buttons
<Button 
  variant="contained" 
  color="primary"
  startIcon={<AddIcon />}
>
  Add Application
</Button>

// Secondary actions
<Button 
  variant="outlined" 
  color="primary"
>
  Show Details
</Button>

// Danger actions
<Button 
  variant="contained" 
  color="error"
  startIcon={<DeleteIcon />}
>
  Delete
</Button>

// Text buttons for less prominent actions
<Button 
  variant="text" 
  color="primary"
>
  Cancel
</Button>
```

### Row Styling Based on Status

```jsx
<DataGrid
  rows={rows}
  columns={columns}
  getRowClassName={(params) => {
    if (params.row.follow_up_required) return 'follow-up-row';
    switch (params.row.status) {
      case 'Offer': return 'offer-row';
      case 'Rejected': return 'rejected-row';
      default: return '';
    }
  }}
  sx={{
    '& .follow-up-row': {
      borderLeft: '4px solid orange',
      bgcolor: 'rgba(255, 193, 7, 0.08)',
    },
    '& .offer-row': {
      borderLeft: '4px solid green',
      bgcolor: 'rgba(76, 175, 80, 0.08)',
    },
    '& .rejected-row': {
      borderLeft: '4px solid red',
      bgcolor: 'rgba(244, 67, 54, 0.08)',
    },
  }}
/>
```

## Performance Optimizations

### Memo Wrapped DataGrid
Use memoization when the DataGrid is in a component with frequent parent re-renders, but the grid data changes infrequently:

```jsx
import React, { memo } from 'react';
import { DataGrid } from '@mui/x-data-grid';

// Memoized DataGrid component to prevent unnecessary re-renders
const StableDataGrid = memo((props) => {
  return <DataGrid {...props} />;
}, (prevProps, nextProps) => {
  // Custom comparison to decide when to re-render
  if (prevProps.rows !== nextProps.rows) return false;
  if (prevProps.loading !== nextProps.loading) return false;
  
  // For columns, we need deep comparison
  if (JSON.stringify(prevProps.columns) !== JSON.stringify(nextProps.columns)) {
    return false;
  }
  
  // Consider it equal otherwise (won't re-render)
  return true;
});

export default StableDataGrid;
```

### Virtualized Rows for Large Datasets
For tables with hundreds or thousands of rows, use these virtualization settings:

```jsx
<DataGrid
  rows={rows}
  columns={columns}
  pagination
  paginationMode="client"
  pageSizeOptions={[10, 25, 50, 100]}
  rowCount={rows.length}
  // Enable virtualization for better performance with large datasets
  rowBuffer={10}
  rowThreshold={100}
/>
```

**When to use which approach:**
- Use **memoization** when: The parent component re-renders frequently but grid data changes infrequently
- Use **virtualization** when: Dealing with large datasets (100+ rows) to reduce DOM elements
- Use **both techniques** for optimal performance in complex applications with large datasets

This reference document will evolve as we implement and optimize the DataGrid components throughout the application.

## Vite-Specific Considerations

When using DataGrid with Vite, keep these additional considerations in mind:

### 1. Import Optimization

Vite's ESM-based development server provides fast imports, but it's important to use proper import patterns for MUI components:

```jsx
// Prefer specific imports over barrel imports
// Good - specific imports
import { DataGrid } from '@mui/x-data-grid';
import Button from '@mui/material/Button';

// Avoid - barrel imports can increase bundle size with Vite
// import { Button, TextField, Box } from '@mui/material';
```

### 2. CSS Injection Order

With Vite, you may need to ensure proper CSS injection order for MUI:

```jsx
// In main.jsx or index.jsx
import { StyledEngineProvider } from '@mui/material/styles';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <StyledEngineProvider injectFirst>
      <App />
    </StyledEngineProvider>
  </React.StrictMode>
);
```

### 3. Environment Variables

When referencing environment variables in components that use DataGrid, use Vite's pattern:

```jsx
// Correct pattern for Vite environment variables
const apiUrl = import.meta.env.VITE_API_URL;

// Don't use process.env (React's pattern)
// const apiUrl = process.env.REACT_APP_API_URL;
```

### 4. Fast Refresh Compatibility

When using memoized components with Vite's Fast Refresh (HMR), follow these practices for better debugging and development:

```jsx
// Add display name to help with debugging
StableDataGrid.displayName = 'StableDataGrid';

// Use named function instead of anonymous for better HMR compatibility
function StableDataGridWrapper(props) {
  return <StableDataGrid {...props} />;
}

// Export the wrapper for better Hot Module Replacement
export default StableDataGridWrapper;
```

This approach ensures that your memoized DataGrid components will work well with Vite's Fast Refresh while maintaining the performance benefits of memoization.

## Document Icons

For consistency in document representation, use these standard icons for different file types:

```jsx
import { 
  PictureAsPdfIcon, 
  ArticleIcon, 
  DescriptionIcon,
  AttachFileIcon 
} from '@mui/icons-material';

// File icon mapping
const getFileIcon = (filename) => {
  if (!filename) return null;
  
  const extension = filename.split('.').pop().toLowerCase();
  
  switch (extension) {
    case 'pdf':
      return <PictureAsPdfIcon fontSize="small" color="error" />;
    case 'doc':
    case 'docx':
      return <ArticleIcon fontSize="small" color="primary" />;
    case 'xls':
    case 'xlsx':
      return <TableChartIcon fontSize="small" color="success" />;
    case 'txt':
      return <TextSnippetIcon fontSize="small" />;
    default:
      return <DescriptionIcon fontSize="small" />;
  }
};

// Usage example in a component
function DocumentLink({ path, label }) {
  const icon = getFileIcon(path);
  
  return path ? (
    <Button
      startIcon={icon}
      size="small"
      onClick={() => window.open(path, '_blank')}
    >
      {label || 'View Document'}
    </Button>
  ) : (
    <span style={{ color: '#aaa' }}>No document</span>
  );
}

// Usage in DataGrid column
{
  field: 'cover_letter',
  headerName: 'Cover Letter',
  width: 130,
  renderCell: (params) => (
    <IconButton
      size="small"
      disabled={!params.value}
      onClick={() => params.value && window.open(params.value, '_blank')}
      color={params.value?.endsWith('.pdf') ? 'error' : 'primary'}
    >
      {getFileIcon(params.value)}
    </IconButton>
  )
}
```
