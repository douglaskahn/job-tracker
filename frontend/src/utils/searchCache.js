// searchCache.js - A utility for caching and managing search requests

const cache = new Map();
let pendingRequests = new Map();
const CACHE_TTL = 60000; // 1 minute cache TTL

/**
 * Creates a cache key from search parameters
 */
export const createCacheKey = (params) => {
  const sortedParams = Object.keys(params)
    .sort()
    .filter(key => params[key] !== undefined)
    .map(key => `${key}:${params[key]}`)
    .join('|');
  
  return sortedParams;
};

/**
 * Retrieves results from cache if available and fresh
 */
export const getFromCache = (cacheKey) => {
  if (!cache.has(cacheKey)) return null;
  
  const { data, timestamp } = cache.get(cacheKey);
  const now = Date.now();
  
  // Check if cache is still valid
  if (now - timestamp > CACHE_TTL) {
    cache.delete(cacheKey);
    return null;
  }
  
  return data;
};

/**
 * Stores results in cache
 */
export const storeInCache = (cacheKey, data) => {
  cache.set(cacheKey, {
    data,
    timestamp: Date.now()
  });
};

/**
 * Clears entire cache or specific keys
 */
export const clearCache = (specificKeys = null) => {
  if (specificKeys) {
    if (Array.isArray(specificKeys)) {
      specificKeys.forEach(key => cache.delete(key));
    } else {
      cache.delete(specificKeys);
    }
  } else {
    cache.clear();
  }
};

/**
 * Registers a pending request
 */
export const registerPendingRequest = (cacheKey, promise) => {
  pendingRequests.set(cacheKey, promise);
  return promise.finally(() => {
    pendingRequests.delete(cacheKey);
  });
};

/**
 * Gets a pending request if one exists
 */
export const getPendingRequest = (cacheKey) => {
  return pendingRequests.get(cacheKey);
};

/**
 * Aborts all pending requests that match a particular search prefix
 */
export const abortRelatedRequests = (searchPrefix) => {
  for (const [key] of pendingRequests) {
    if (key.includes(`search:${searchPrefix}`)) {
      pendingRequests.delete(key);
    }
  }
};
