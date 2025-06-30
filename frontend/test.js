// test.js - A simple script to test our changes
const fs = require('fs');
const path = require('path');

console.log('===== Testing Job Tracker Refactoring Phase 1 =====\n');

// Check for required files
const requiredFiles = [
  'src/config.js',
  'src/context/ApplicationContext.js',
  'src/hooks/useApplicationData.js',
  'src/AppProviders.js',
  'src/api.js.new'
];

console.log('Checking for required files:');
let allFilesExist = true;

for (const file of requiredFiles) {
  const filePath = path.join(__dirname, file);
  const exists = fs.existsSync(filePath);
  console.log(`${exists ? '✅' : '❌'} ${file}`);
  
  if (!exists) {
    allFilesExist = false;
  }
}

console.log(`\nOverall file check: ${allFilesExist ? '✅ All files present' : '❌ Some files are missing'}`);
console.log('\n===== Test Complete =====');
