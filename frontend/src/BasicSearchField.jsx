import React, { useState, useEffect, useRef, useCallback } from 'react';
import { TextField, CircularProgress } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';

/**
 * A search field component designed for maximum stability.
 * It maintains focus during searches and handles event passing carefully.
 */
const BasicSearchField = ({ 
  value, 
  onChange, 
  placeholder = "Search...", 
  autoFocus = false,
  isDebouncing = false
}) => {
  const [localValue, setLocalValue] = useState(value || '');
  const inputRef = useRef(null);
  const selectionRef = useRef({ start: null, end: null });
  
  // Update local value when prop value changes (but only if different)
  useEffect(() => {
    if (value !== localValue) {
      setLocalValue(value || '');
    }
  }, [value, localValue]);

  // Preserve selection and focus
  const saveFocusState = useCallback(() => {
    if (document.activeElement === inputRef.current) {
      selectionRef.current = {
        start: inputRef.current.selectionStart,
        end: inputRef.current.selectionEnd,
        hasFocus: true
      };
    } else {
      selectionRef.current.hasFocus = false;
    }
  }, []);

  // Restore focus state after render
  useEffect(() => {
    if (selectionRef.current.hasFocus && inputRef.current) {
      inputRef.current.focus();
      if (selectionRef.current.start !== null && selectionRef.current.end !== null) {
        inputRef.current.setSelectionRange(selectionRef.current.start, selectionRef.current.end);
      }
    }
  });

  // Handle changes and pass the full event object
  const handleChange = useCallback((e) => {
    saveFocusState();
    const newValue = e.target.value;
    setLocalValue(newValue);
    if (onChange) {
      onChange(e); // Pass the entire event object to maintain focus
    }
  }, [onChange, saveFocusState]);

  return (
    <TextField
      fullWidth
      value={localValue}
      onChange={handleChange}
      placeholder={placeholder}
      autoFocus={autoFocus}
      inputRef={inputRef}
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

export default React.memo(BasicSearchField);
