/**
 * test_config.js
 * 
 * Simple test to verify the configuration system is working correctly.
 * Run with: node frontend/test_config.js
 */

// Import the configuration (using ES modules)
import config, { initConfig } from './src/config.js';

async function testConfig() {
  console.log('\n===== Testing Configuration System =====\n');
  
  // Test direct config access
  console.log('Direct config access:');
  console.log('API Base URL:', config.apiBase);
  console.log('Default page size:', config.pageSize);
  console.log('Environment:', config.isProduction ? 'Production' : 'Development');
  
  // Test async initialization
  console.log('\nTesting async initialization:');
  try {
    const initializedConfig = await initConfig();
    console.log('Config initialized successfully!');
    console.log('API Base URL after init:', initializedConfig.apiBase);
  } catch (error) {
    console.error('Error initializing config:', error);
  }
  
  console.log('\n===== Configuration Test Complete =====');
  console.log('All configuration properties:');
  console.log(JSON.stringify(config, null, 2));
}

// Run the test
testConfig();
