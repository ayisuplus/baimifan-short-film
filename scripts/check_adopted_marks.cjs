// Protect existing user decisions when adding project-backed initial choices.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const code=fs.readFileSync(__dirname+'/storyboard-marks.js','utf8');
const fn=code.slice(code.indexOf('function readMarks(){'),code.indexOf('function save(change){'));
const frozen={CY001:'track-a',CY024K0:'track-b'};
function check(raw,expected,ok=true){
 const ctx={localStorage:{getItem:()=>raw},key:'test',adoptedMarks:frozen,marks:{sentinel:'preserved'},storageError:''};
 vm.createContext(ctx);vm.runInContext(fn+'; result=readMarks();',ctx);
 assert.equal(ctx.result,ok);assert.deepEqual(JSON.parse(JSON.stringify(ctx.marks)),expected);
}
check(null,frozen);check('{}',{});check('{"CY001":"changed"}',{CY001:'changed'});
check('{"historical":"unknown"}',{historical:'unknown'});
check('{bad',{sentinel:'preserved'},false);check('[]',{sentinel:'preserved'},false);
console.log('PASS: missing record uses frozen choices; existing empty/partial/unknown preserved; invalid records not overwritten.');
