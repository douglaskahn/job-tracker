// useSearch.js - A custom hook for search functionality that avoids page reloads

import { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import { getApiBase } from '../config';

/**
 * A custom hook that provides advanced search functionality
 * - Maintains local state for immediate feedback
 * - Debounces server requests to prevent excessive API calls
 * - Cancels outdated requests to prevent race conditions
 * - Properly handles loading states and error conditions
 * - Preserves search state between renders
 * - Maintains input focus during searches
 */
const useSearch = (options = {}) => {
  // Extract options with defaults
  const {
    initialSearchTerm = '',
    debounceTime = 400,
    pageSize = 50,
    isDemoMode = false,
    onSearchComplete = null,
    additionalParams = {}
  } = options;

  // Local state (immediately responsive to user input)
  const [searchTerm, setSearchTerm] = useState(initialSearchTerm);
  const searchInputRef = useRef(null);
  
  // Search processing state
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState({ data: [], total: 0 });
  const [error, setError] = useState(null);
  
  // Focus tracking state
  const [selectionStart, setSelectionStart] = useState(null);
  const [selectionEnd, setSelectionEnd] = useState(null);
  
  // Refs for tracking async operations
  const debounceTimerRef = useRef(null);
  const abortControllerRef = useRef(null);
  const lastExecutedSearchRef = useRef('');
  const searchRequestIdRef = useRef(0);
  
  // Cache for storing previous search results
  const searchCacheRef = useRef(new Map());
  
  /**
   * Execute the actual search request with proper cancellation
   */
  const executeSearch = useCallback(async (term) => {
    try {
      // Skip if this exact search was just executed
      if (term === lastExecutedSearchRef.current && term !== '') {
        return;
      }
      
      // Update the current search tracking
      lastExecutedSearchRef.current = term;
      setIsSearching(true);
      setError(null);
      
      // Check the cache first
      const cacheKey = `${term}:${isDemoMode}:${JSON.stringify(additionalParams)}`;
      if (searchCacheRef.current.has(cacheKey)) {
        const cachedResult = searchCacheRef.current.get(cacheKey);
        setSearchResults(cachedResult);
        
        if (onSearchComplete) {
          onSearchComplete(cachedResult);
        }
        
        setIsSearching(false);
        return;
      }
      
      // Cancel any in-flight request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      
      // Create a new abort controller for this request
      abortControllerRef.current = new AbortController();
      
      // Create an ID for this specific request to track it
      const requestId = ++searchRequestIdRef.current;
      
      // Build search parameters
      const params = {
        search: term || undefined,
        page: 1,
        page_size: pageSize,
        ...additionalParams
      };
      
      // Determine which endpoint to call
      const endpoint = isDemoMode ? '/demo/applications/' : '/applications/';
      const apiUrl = `${getApiBase()}${endpoint}`;
      
      // Make the request with cancellation support
      const response = await axios.get(apiUrl, {
        params,
        signal: abortControllerRef.current.signal
      });
      
      // Only process if this is still the current request
      if (requestId === searchRequestIdRef.current) {
        const result = response.data;
        
        // Store in cache
        searchCacheRef.current.set(cacheKey, result);
        
        // Limit cache size to prevent memory issues
        if (searchCacheRef.current.size > 20) {
          // Remove the oldest entry
          const firstKey = searchCacheRef.current.keys().next().value;
          searchCacheRef.current.delete(firstKey);
        }
        
        // Update UI
        setSearchResults(result);
        
        // Notify caller
        if (onSearchComplete) {
          onSearchComplete(result);
        }
      }
    } catch (err) {
      // Don't show error for cancelled requests
      if (!axios.isCancel(err)) {
        console.error('Search error:', err);
        setError(err.message || 'Error performing search');
      }
    } finally {
      setIsSearching(false);
    }
  }, [isDemoMode, pageSize, additionalParams, onSearchComplete]);
  
  /**
   * Handle search input changes while preserving focus
   */
  const handleSearchChange = useCallback((e) => {
    // Extract the value from the event or use the raw value
    let newValue;
    
    if (e && e.target && e.target.value !== undefined) {
      // It's an event object
      newValue = e.target.value;
      
      // Store current selection before state update
      setSelectionStart(e.target.selectionStart);
      setSelectionEnd(e.target.selectionEnd);
      searchInputRef.current = e.target;
    } else if (typeof e === 'string') {
      // It's already a string value
      newValue = e;
    } else if (e && typeof e === 'object') {
      // It's some other object, try to extract value
      console.warn('Received object instead of string or event for search:', e);
      if (e.value !== undefined) {
        newValue = e.value;
      } else if (e.query !== undefined) {
        newValue = e.query;
      } else if (e.toString && e.toString() !== '[object Object]') {
        newValue = e.toString();
      } else {
        newValue = '';
      }
    } else {
      // Default empty string
      newValue = '';
    }
    
    console.log('Search value processed:', newValue);
    
    // Update search term
    setSearchTerm(newValue);
    
    // Clear any pending debounced search
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    
    // Schedule new search
    debounceTimerRef.current = setTimeout(() => {
      executeSearch(newValue);
    }, debounceTime);
  }, [debounceTime, executeSearch]);

  // Restore focus after updates
  useEffect(() => {
    if (searchInputRef.current && selectionStart !== null && selectionEnd !== null) {
      searchInputRef.current.focus();
      searchInputRef.current.setSelectionRange(selectionStart, selectionEnd);
    }
  }, [searchResults, selectionStart, selectionEnd]);

  /**
   * Reset search completely
   */
  const resetSearch = useCallback(() => {
    // Cancel pending operations
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // Reset state
    setSearchTerm('');
    lastExecutedSearchRef.current = '';
    setIsSearching(false);
    setSelectionStart(null);
    setSelectionEnd(null);
    
    // Execute an empty search to refresh results
    executeSearch('');
  }, [executeSearch]);
  
  /**
   * Clean up resources when unmounting
   */
  useEffect(() => {
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
      
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  return {
    // Core state
    searchTerm,
    isSearching,
    searchResults,
    error,
    searchInputRef,
    
    // Actions
    handleSearchChange,
    resetSearch,
    setSearchTerm
  };
};

export default useSearch;
