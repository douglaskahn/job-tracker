import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  IconButton,
  TextField,
  InputAdornment,
  Typography,
  Tooltip,
  Menu,
  MenuItem,
  Checkbox,
  ListItemText,
  Alert,
} from '@mui/material';
import {
  Close as CloseIcon,
  Search as SearchIcon,
  ViewColumn as ViewColumnIcon,
  CloudDownload as CloudDownloadIcon,
  Visibility as VisibilityIcon,
  Edit as EditIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import { DataGrid, GridActionsCellItem } from '@mui/x-data-grid';
import { saveAs } from 'file-saver';

const ShowAllModal = ({
  open,
  onClose,
  rows,
  columns,
  onView,
  visibleColumns,
  setVisibleColumns,
  onEdit,
  onDelete
}) => {
  const [error, setError] = useState('');
  const [columnMenuAnchor, setColumnMenuAnchor] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortModel, setSortModel] = useState([]);
  const [loading, setLoading] = useState(false);
  const [columnVisibilityModel, setColumnVisibilityModel] = useState(
    visibleColumns.reduce((acc, col) => ({ ...acc, [col]: true }), {})
  );

  // Enhanced filtering with type checking
  const filteredRows = React.useMemo(() => rows.filter(row =>
    Object.entries(row).some(([key, value]) => {
      if (!visibleColumns.includes(key)) return false;
      if (value == null) return false;
      const stringValue = value.toString().toLowerCase();
      const search = searchTerm.toLowerCase();
      return stringValue.includes(search);
    })
  ), [rows, searchTerm, visibleColumns]);

  // Handle data export with error handling
  const handleExport = () => {
    setLoading(true);
    setError('');
    try {
      const visibleCols = columns.filter(col => columnVisibilityModel[col.field]);
      const header = visibleCols.map(col => `"${col.headerName || col.field}"`).join(',');
      const csvRows = filteredRows.map(row =>
        visibleCols.map(col => {
          const value = row[col.field];
          if (value == null) return '""';
          if (col.field === 'status') return `"${value}"`;
          if (typeof value === 'boolean') return value ? '"Yes"' : '"No"';
          return `"${value.toString().replace(/"/g, '""')}"`;
        }).join(',')
      );
      const csv = [header, ...csvRows].join('\n');
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8' });
      saveAs(blob, `job_applications_${new Date().toISOString().split('T')[0]}.csv`);
    } catch (error) {
      setError('Failed to export data. Please try again.');
      console.error('Export error:', error);
    } finally {
      setLoading(false);
    }
  };

  // Enhanced columns with actions
  const enhancedColumns = React.useMemo(() => [
    ...columns.map(col => ({
      ...col,
      flex: 1,
      minWidth: 120,
      sortable: true,
      filterable: true,
      hideable: true,
      renderCell: (params) => {
        const value = params.value;
        if (value == null) return '';
        if (typeof value === 'boolean') return value ? 'Yes' : 'No';
        return value.toString();
      }
    })),
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 120,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<VisibilityIcon />}
          label="View"
          onClick={() => onView(params.row)}
        />,
        <GridActionsCellItem
          icon={<EditIcon />}
          label="Edit"
          onClick={() => onView(params.row)}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Delete"
          onClick={() => onDelete(params.row.id)}
        />,
      ]
    }
  ], [columns, onView, onDelete]);

  // Column menu handlers
  const handleColumnMenuOpen = (event) => {
    setColumnMenuAnchor(event.currentTarget);
  };

  const handleColumnMenuClose = () => {
    setColumnMenuAnchor(null);
  };

  const handleColumnToggle = (field) => {
    setColumnVisibilityModel(prev => {
      const newModel = {
        ...prev,
        [field]: !prev[field]
      };
      const visibleCols = Object.entries(newModel)
        .filter(([_, visible]) => visible)
        .map(([field]) => field);
      setVisibleColumns(visibleCols);
      return newModel;
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="xl"
      fullWidth
      PaperProps={{
        sx: {
          height: '90vh',
          maxHeight: '90vh'
        }
      }}
    >
      <DialogTitle sx={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        p: 2
      }}>
        <Typography variant="h6">All Applications</Typography>
        <Box sx={{ display: 'flex', gap: 1 }}>
          <TextField
            size="small"
            placeholder="Search all fields..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              )
            }}
          />
          <Tooltip title="Export to CSV">
            <IconButton 
              onClick={handleExport}
              disabled={loading}
              color="primary"
            >
              <CloudDownloadIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Column Visibility">
            <IconButton 
              color="primary"
              aria-label="show/hide columns"
              onClick={handleColumnMenuOpen}
            >
              <ViewColumnIcon />
            </IconButton>
          </Tooltip>
          <IconButton onClick={onClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>

      <DialogContent sx={{ p: 2 }}>
        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}
        <Box sx={{ height: '100%', width: '100%' }}>
          <DataGrid
            rows={filteredRows}
            columns={enhancedColumns}
            disableRowSelectionOnClick
            sortModel={sortModel}
            onSortModelChange={setSortModel}
            columnVisibilityModel={columnVisibilityModel}
            onColumnVisibilityModelChange={(model) => {
              setColumnVisibilityModel(model);
              const visibleCols = Object.entries(model)
                .filter(([_, visible]) => visible)
                .map(([field]) => field);
              setVisibleColumns(visibleCols);
            }}
            density="comfortable"
            autoHeight={false}
            getRowHeight={() => 'auto'}
            sx={{
              '& .MuiDataGrid-cell': {
                whiteSpace: 'normal',
                lineHeight: 'normal',
                p: 1,
                minHeight: '52px !important',
                maxHeight: 'none !important',
                '&:focus': {
                  outline: 'none'
                }
              },
              '& .MuiDataGrid-row': {
                minHeight: '52px !important',
                maxHeight: 'none !important'
              }
            }}
            components={{
              Toolbar: null // We have our own toolbar in DialogTitle
            }}
            loading={loading}
          />
        </Box>
      </DialogContent>

      <Menu
        anchorEl={columnMenuAnchor}
        open={Boolean(columnMenuAnchor)}
        onClose={handleColumnMenuClose}
      >
        {columns.map((column) => (
          <MenuItem 
            key={column.field}
            onClick={() => handleColumnToggle(column.field)}
            dense
          >
            <Checkbox
              checked={columnVisibilityModel[column.field] || false}
              size="small"
            />
            <ListItemText primary={column.headerName || column.field} />
          </MenuItem>
        ))}
      </Menu>
    </Dialog>
  );
};

export default ShowAllModal;
