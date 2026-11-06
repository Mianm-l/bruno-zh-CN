const asar = require('C:/Users/61981/.gemini/antigravity/scratch/node_modules/asar');
const path = require('path');

const srcDir = 'C:/Users/61981/.gemini/antigravity/scratch/bruno_app';
const destAsar = 'C:/Users/61981/.gemini/antigravity/scratch/app_zh.asar';

console.log('Starting packing asar...');
console.time('pack');
asar.createPackage(srcDir, destAsar).then(() => {
  console.timeEnd('pack');
  console.log('Packing complete! Output:', destAsar);
}).catch(err => {
  console.error('Error packing:', err);
  process.exit(1);
});
