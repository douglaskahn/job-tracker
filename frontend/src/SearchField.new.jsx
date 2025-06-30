import React, { useState, useEffect } from 'react';
import { TextField, CircularProgress } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

/**
 * A search field component that maintains focus while typing and works with
 * the useSearch hook to provide a smooth search experience.
 */
const SearchField = ({ 
  value, 
  onChange, 
  placeholder = "Search...", 
  autoFocus = false,
  isDebouncing = false
}) => {
  const [localValue, setLocalValue] = useState(value || '');
  
  // Update local value when prop value changes (but only if different)
  useEffect(() => {
    if (value !== localValue) {
      setLocalValue(value || '');
    }
  }, [value, localValue]);

  // Handle changes and maintain focus
  const handleChange = (e) => {
    const newValue = e.target.value;
    setLocalValue(newValue);
    if (onChange) {
      onChange(e);
    }
  };

  return (
    <TextField
      fullWidth
      value={localValue}
      onChange={handleChange}
      placeholder={placeholder}
      autoFocus={autoFocus}
      InputProps={{
        startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
        endAdornment: isDebouncing && (
          <CircularProgress 
            size={20}
            sx={{ 
              position: 'absolute',
              right: 8,
              color: 'primary.main'
            }}
          />
        ),
      }}
      sx={{
        '& .MuiInputBase-root': {
          pr: isDebouncing ? 4 : 1, // Add padding when showing loading indicator
        },
      }}
    />
  );
};

export default SearchField;
