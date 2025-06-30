import React, { useState, useMemo } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Box, Chip, Button, Tooltip, TextField, IconButton, Menu, MenuItem, Checkbox, ListItemText, FormControl, InputLabel, Select, FormControlLabel, Switch } from '@mui/material';
import ViewColumnIcon from '@mui/icons-material/ViewColumn';
import SearchIcon from '@mui/icons-material/Search';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { saveAs } from 'file-saver';
import config from './config';

const statusColors = {
  'Not Yet Applied': 'default',
  'Applied': 'warning',
  'Interviewing': 'orange',
  'Offer': 'success',
  'Rejected': 'error',
  'No Longer Listed': 'default',
  'Decided not to apply': 'secondary',
  'Declined Offer': 'default',
  'Accepted': 'primary',
  'Applied / No Longer Listed': 'default',
};

// Render function for resume file links
const renderResumeLink = (params) => {
  if (!params.value) return <span style={{ color: '#aaa' }}>N/A</span>;
  
  return (
    <a href={`${config.api.baseURL}/uploads/${params.value}`} target="_blank" rel="noopener noreferrer" style={{ color: '#1976d2', textDecoration: 'underline' }}>
      See Resume
    </a>
  );
};

// Render function for cover letter links
const renderCoverLetterLink = (params) => {
  if (!params.value) return <span style={{ color: '#aaa' }}>N/A</span>;
  
  return (
    <a href={`${config.api.baseURL}/uploads/${params.value}`} target="_blank" rel="noopener noreferrer" style={{ color: '#1976d2', textDecoration: 'underline' }}>
      See Cover Letter
    </a>
  );
};

const columns = [
  { field: 'company', headerName: 'Company', width: 160 },
  { field: 'role', headerName: 'Role', width: 160 },
  { field: 'status', headerName: 'Status', width: 120, renderCell: (params) => (
    <Chip label={params.value} color={statusColors[params.value] || 'default'} size="small" />
  ) },
  { field: 'url', headerName: 'Job Posting', width: 140, renderCell: (params) =>
    params.value ? (
      <a href={params.value} target="_blank" rel="noopener noreferrer" style={{ color: '#1976d2', textDecoration: 'underline' }}>
        See Job Posting
      </a>
    ) : (
      <span style={{ color: '#aaa' }}>N/A</span>
    ),
    sortable: false,
    filterable: false,
  },
  { field: 'application_date', headerName: 'Date Applied', width: 120 },
  { field: 'met_with', headerName: 'Met With', width: 140 },
  { field: 'notes', headerName: 'Notes', width: 180 },
  { field: 'resume_file', headerName: 'Resume', width: 120, renderCell: renderResumeLink },
  { field: 'cover_letter_file', headerName: 'Cover Letter', width: 120, renderCell: renderCoverLetterLink },
  { field: 'pros', headerName: 'Pros', width: 120 },
  { field: 'cons', headerName: 'Cons', width: 120 },
  { field: 'salary', headerName: 'Salary', width: 100 },
  { field: 'follow_up_required', headerName: 'Follow Up', width: 100, renderCell: (params) => (
    params.value ? <span style={{ color: 'orange', fontWeight: 'bold' }} title="Follow Up Required">●</span> : null
  ), sortable: true, filterable: true },
  {
    field: 'view',
    headerName: '',
    width: 50,
    renderCell: (params) => (
      <Tooltip title="View Details">
        <IconButton
          size="small"
          onClick={(e) => {
            e.stopPropagation();
            if (params.row && params.row.onView) params.row.onView(params.row);
          }}
          sx={{
            '&:hover': {
              backgroundColor: 'action.hover',
            }
          }}
        >
          <VisibilityIcon fontSize="small" />
        </IconButton>
      </Tooltip>
    ),
    sortable: false,
    filterable: false,
    disableColumnMenu: true,
    align: 'center',
  },
];

const editableFields = [
  'company', 'role', 'status', 'url', 'application_date', 'met_with', 'notes',
  'resume_file', 'cover_letter_file', 'pros', 'cons', 'salary', 'follow_up_required'
];

const JobTable = ({
  rows, onRowClick, onView, onShowAll, onClearFilters, search, setSearch, visibleColumns, setVisibleColumns, page, setPage,
  statusFilter, setStatusFilter, followUpFilter, setFollowUpFilter
}) => {
  // Debug logging for rows
  console.log("JobTable received rows:", rows, "length:", rows?.length);
  console.log("Data type check:", Array.isArray(rows) ? "Is array" : "Not an array", typeof rows);
  
  // Sort by most recent (application_date, created_at, or fallback to order_number desc)
  const sortedRows = useMemo(() => {
    // Safety check: ensure rows is an array
    if (!Array.isArray(rows)) {
      console.error("Rows is not an array:", rows);
      return [];
    }
    
    return [...rows].sort((a, b) => {
      // Convert all values to comparable numbers, higher = more recent
      const multiplier = 1000000; // To maintain integer precision with order numbers
      
      const getSortValue = (row) => {
        // Special handling for imported records (all have same created_at)
        if (row.created_at === "2025-06-20T02:58:17" && 
            row.order_number !== undefined && row.order_number !== null) {
          // Make higher order numbers sort first
          return Number(row.order_number) * multiplier;
        }
        
        // For new records
        if (row.created_at) {
          const date = new Date(row.created_at);
          return date.getTime();
        }
        
        // Fallback to application_date if available
        if (row.application_date) {
          const date = new Date(row.application_date);
          return date.getTime();
        }
        
        // Final fallback to id
        return Number(row.id);
      };
      
      const aVal = getSortValue(a);
      const bVal = getSortValue(b);
      
      return bVal - aVal;
    });
  }, [rows]);

  // Pagination state
  const pageSize = 10;
  const pageCount = Math.ceil(sortedRows.length / pageSize);

  // Show/hide columns state
  const [anchorEl, setAnchorEl] = useState(null);
  const handleColumnMenuOpen = (e) => setAnchorEl(e.currentTarget);
  const handleColumnMenuClose = () => setAnchorEl(null);
  const handleToggleColumn = (field) => {
    setVisibleColumns((prev) =>
      prev.includes(field) ? prev.filter(f => f !== field) : [...prev, field]
    );
  };

  // State for sorting with default sort order
  const [sortModel, setSortModel] = useState([
    { field: config.defaultSortField, sort: config.defaultSortDirection }
  ]);

  // Filtered and sorted rows
  const filteredRows = useMemo(() => {
    console.log(`JobTable processing ${sortedRows.length} applications`);
    
    let filtered = sortedRows;
    if (statusFilter) {
      filtered = filtered.filter(row => row.status === statusFilter);
    }
    if (followUpFilter === 'yes') {
      filtered = filtered.filter(row => row.follow_up_required);
    }
    if (!search) return filtered;
    return filtered.filter(row =>
      Object.values(row).some(val =>
        val && val.toString().toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [sortedRows, search, statusFilter, followUpFilter]);

  // Apply custom sorting if sort model is defined
  const sortedFilteredRows = useMemo(() => {
    if (!sortModel.length) return filteredRows;
    
    return [...filteredRows].sort((a, b) => {
      const { field, sort } = sortModel[0];
      const aValue = a[field];
      const bValue = b[field];
      
      // Handle undefined or null values
      if (aValue == null && bValue == null) return 0;
      if (aValue == null) return sort === 'asc' ? -1 : 1;
      if (bValue == null) return sort === 'asc' ? 1 : -1;
      
      // Compare values based on sort direction
      if (aValue < bValue) return sort === 'asc' ? -1 : 1;
      if (aValue > bValue) return sort === 'asc' ? 1 : -1;
      return 0;
    });
  }, [filteredRows, sortModel]);

  // Memoize columns and filtered columns for DataGrid stability
  const memoizedColumns = useMemo(() => columns, []);
  const filteredColumns = useMemo(
    () => memoizedColumns.filter(col => visibleColumns.includes(col.field)),
    [memoizedColumns, visibleColumns]
  );

  // Modify the filteredRows to include the onView callback for each row
  const filteredRowsWithView = useMemo(() => 
    sortedFilteredRows.map(row => ({ ...row, onView })),
    [sortedFilteredRows, onView]
  );

  // Unique status values for filter dropdown
  const statusOptions = useMemo(() => {
    const set = new Set();
    rows.forEach(row => row.status && set.add(row.status));
    return Array.from(set);
  }, [rows]);

  // CSV export utility
  function exportToCSV(rows, columns) {
    const visibleCols = columns.filter(col => col.field !== 'view');
    const header = visibleCols.map(col => col.headerName || col.field).join(',');
    const csvRows = rows.map(row =>
      visibleCols.map(col => {
        let val = row[col.field];
        if (val === undefined || val === null) return '';
        // Escape quotes and commas
        return '"' + String(val).replace(/"/g, '""') + '"';
      }).join(',')
    );
    const csv = [header, ...csvRows].join('\n');
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, 'applications_export.csv');
  }

  return (
    <Box maxWidth="lg" mx="auto" sx={{ width: '100%' }}>
      {/* Top controls: search, show/hide columns, clear */}
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, gap: 2, flexWrap: 'wrap', width: '100%' }}>
        {/* Status filter */}
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={statusFilter}
            label="Status"
            onChange={e => setStatusFilter(e.target.value)}
          >
            <MenuItem value="">All</MenuItem>
            {statusOptions.map(status => (
              <MenuItem key={status} value={status}>{status}</MenuItem>
            ))}
          </Select>
        </FormControl>
        {/* Follow-up filter */}
        <FormControlLabel
          control={
            <Switch
              checked={followUpFilter === 'yes'}
              onChange={e => setFollowUpFilter(e.target.checked ? 'yes' : '')}
              color="warning"
            />
          }
          label="Follow Up Only"
        />
        {/* Search field */}
        <TextField
          size="small"
          variant="outlined"
          placeholder="Search applications..."
          value={search}
          onChange={e => { setSearch(e.target.value); setPage(0); }}
          InputProps={{ startAdornment: <SearchIcon sx={{ mr: 1 }} /> }}
          sx={{ minWidth: 240 }}
        />
        {/* Columns menu */}
        <IconButton onClick={handleColumnMenuOpen} aria-label="Show/hide columns">
          <ViewColumnIcon />
        </IconButton>
        <Menu anchorEl={anchorEl} open={Boolean(anchorEl)} onClose={handleColumnMenuClose}>
          {editableFields.map(field => {
            const col = columns.find(c => c.field === field);
            if (!col) return null;
            return (
              <MenuItem key={col.field} onClick={() => handleToggleColumn(col.field)}>
                <Checkbox checked={visibleColumns.includes(col.field)} />
                <ListItemText primary={col.headerName || col.field} />
              </MenuItem>
            );
          })}
        </Menu>
        {/* Clear filters button */}
        <Tooltip title="Clear all filters and reset view">
          <span><Button onClick={onClearFilters} color="secondary" variant="outlined">Clear</Button></span>
        </Tooltip>
        {/* Export CSV button */}
        <Button variant="outlined" onClick={() => exportToCSV(sortedFilteredRows, filteredColumns)}>
          Export CSV
        </Button>
      </Box>
      {/* DataGrid in horizontally scrollable container */}
      <Box sx={{ overflowX: 'auto' }}>
        <Box sx={{ minWidth: '1000px' }}>
          <DataGrid
            rows={filteredRowsWithView.slice(page * pageSize, (page + 1) * pageSize)}
            columns={filteredColumns}
            pageSize={pageSize}
            rowsPerPageOptions={[]}
            pagination={false}
            hideFooter
            disableSelectionOnClick
            onRowClick={(params) => onView(params.row)}
            sortModel={sortModel}
            onSortModelChange={(model) => setSortModel(model)}
            getRowClassName={(params) => `status-${params.row.status?.toLowerCase().replace(/\s+/g, '-')}`}
            sx={{
              '& .MuiDataGrid-columnHeaders': { position: 'sticky', top: 0, background: '#fff', zIndex: 1 },
              '& .MuiDataGrid-row': {
                cursor: 'pointer',
              },
              '& .MuiDataGrid-row:hover': { backgroundColor: '#f5f7fa' },
              '& .MuiDataGrid-cell': { borderBottom: '1px solid #e0e0e0' },
              fontSize: 15,
              height: 650,
            }}
          />
        </Box>
      </Box>
      {/* Bottom controls: Pagination, Show All */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 2 }}>
        <Box>
          <Tooltip title="Go to first page"><span><Button onClick={() => setPage(0)} disabled={page === 0}>First</Button></span></Tooltip>
          <Tooltip title="Previous page"><span><Button onClick={() => setPage((p) => Math.max(0, p - 1))} disabled={page === 0}>Prev</Button></span></Tooltip>
          <Tooltip title="Next page"><span><Button onClick={() => setPage((p) => Math.min(pageCount - 1, p + 1))} disabled={page >= pageCount - 1}>Next</Button></span></Tooltip>
          <Tooltip title="Go to last page"><span><Button onClick={() => setPage(pageCount - 1)} disabled={page >= pageCount - 1}>Last</Button></span></Tooltip>
          <span style={{ marginLeft: 16 }}>Page {page + 1} of {pageCount}</span>
        </Box>
        <Button variant="contained" color="primary" onClick={onShowAll} sx={{ ml: 2 }}>
          Show All
        </Button>
      </Box>
      {/* NOTE: Dynamic row height for long-form fields is a possible future UX enhancement. See requirements doc. */}
    </Box>
  );
};

export default JobTable;
