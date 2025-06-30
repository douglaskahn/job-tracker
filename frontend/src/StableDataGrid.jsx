import React, { memo, useRef } from 'react';
import { DataGrid } from '@mui/x-data-grid';

/**
 * A stabilized DataGrid component that prevents unnecessary re-renders
 * and preserves focus state to avoid flashing when filters change.
 */
const StableDataGrid = memo((props) => {
  // Store DOM element reference to preserve focus and state
  const gridRef = useRef(null);
  
  return (
    <div 
      ref={gridRef}
      style={{ 
        height: props.sx?.height || 580,
        position: 'relative' 
      }}
      className="stable-data-grid-container"
    >
      <DataGrid 
        {...props} 
        slotProps={{
          // Configure slots to better handle filter changes
          baseButton: {
            // Prevent button clicks from causing page refreshes
            disableRipple: true,
          },
          // Add additional configuration for other slots if needed
        }}
      />
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison to avoid unnecessary re-renders
  
  // Function to compare row arrays by ID for quick checks
  const compareRowArrays = (prevRows, nextRows) => {
    if (prevRows === nextRows) return true; // Same reference
    if (!prevRows || !nextRows) return prevRows === nextRows;
    if (prevRows.length !== nextRows.length) return false;
    
    // Check if the IDs match
    const prevIds = prevRows.map(r => r.id).join(',');
    const nextIds = nextRows.map(r => r.id).join(',');
    return prevIds === nextIds;
  };
  
  // First check critical properties that would require a re-render
  const columnsEqual = 
    prevProps.columns === nextProps.columns || 
    (prevProps.columns?.length === nextProps.columns?.length &&
     JSON.stringify(prevProps.columns) === JSON.stringify(nextProps.columns));
     
  const rowsEqual = compareRowArrays(prevProps.rows, nextProps.rows);
  const pageEqual = prevProps.page === nextProps.page;
  const pageSizeEqual = prevProps.pageSize === nextProps.pageSize;
  
  // If any of these changed, we need to re-render
  if (!columnsEqual || !rowsEqual || !pageEqual || !pageSizeEqual) {
    return false;
  }
  
  // Otherwise, consider it stable
  return true;
});

export default StableDataGrid;
