/**
 * test_context_structure.js
 * 
 * A simple test to verify the structure of our ApplicationContext
 * This test doesn't render any components but checks that our context exports
 * the expected functions and structure.
 * 
 * Run with: node frontend/test_context_structure.js
 */

// Import the context module
const ApplicationContext = require('./src/context/ApplicationContext');

function testContextStructure() {
  console.log('\n===== Testing ApplicationContext Structure =====\n');
  
  // Check that the module exports what we expect
  console.log('Module exports:');
  const exportedItems = Object.keys(ApplicationContext);
  console.log(exportedItems);
  
  // Check for required exports
  const requiredExports = ['default', 'useApplicationContext', 'ApplicationProvider'];
  const missingExports = requiredExports.filter(item => !exportedItems.includes(item));
  
  if (missingExports.length === 0) {
    console.log('\n✅ All required exports present!');
  } else {
    console.log('\n❌ Missing exports:', missingExports);
  }
  
  // Check structure of ApplicationProvider if present
  if (ApplicationContext.ApplicationProvider) {
    console.log('\nApplicationProvider exists');
  } else {
    console.log('\n❌ ApplicationProvider not found');
  }
  
  // Check structure of useApplicationContext if present
  if (ApplicationContext.useApplicationContext) {
    console.log('useApplicationContext exists');
  } else {
    console.log('❌ useApplicationContext not found');
  }
  
  console.log('\n===== Context Structure Test Complete =====');
}

// Run the test
try {
  testContextStructure();
} catch (error) {
  console.error('Error testing context structure:', error);
}
