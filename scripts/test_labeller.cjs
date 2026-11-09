// Behaviour harness, not browser/rendering evidence. No engine execution on v1.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
function setup() {
  const html = fs.readFileSync(path.join(root, 'evals/labeller.html'), 'utf8');
  class Element {
    constructor(tag='div') {
      this.tagName=tag.toUpperCase();this.children=[];this.events={};this.value='';this.checked=false;this.style={};
      const classes=new Set();
      this.classList={add:c=>classes.add(c),remove:c=>classes.delete(c),contains:c=>classes.has(c),toggle:(c,on)=>on?classes.add(c):classes.delete(c)};
    }
    append(...children){this.children.push(...children)}
    replaceChildren(...children){this.children=children}
    addEventListener(k,fn){this.events[k]=fn}
    focus(){}
    click(){this.events.click?.({target:this,preventDefault(){}})}
    querySelectorAll(selector){
      const all=this.children.flatMap(c=>typeof c==='object'?[c,...c.querySelectorAll('*')]:[]);
      if(selector==='*')return all;
      return all.filter(c=>c.tagName==='INPUT' && (!selector.includes(':checked') || c.checked));
    }
    querySelector(selector){return this.querySelectorAll(selector)[0] || null}
  }
  const elements={};
  for(const m of html.matchAll(/<([\w]+)[^>]*\bid="([^"]+)"[^>]*>/g))elements[m[2]]=new Element(m[1]);
  const form=elements.form;form.elements={};
  for(const name of ['state','handover','caseType','eligible']){
    const values=[...html.matchAll(new RegExp(`name="${name}" value="([^"]+)"`,'g'))].map(m=>m[1]);
    form.elements[name]=values.map(value=>Object.assign(new Element('input'),{value}));
  }
  form.elements.action=new Element('textarea');form.elements.notes=new Element('textarea');
  form.querySelector=selector=>{
    const name=selector.match(/name=(\w+)/)?.[1];
    return form.elements[name]?.find(input=>input.checked) || null;
  };
  const storage=new Map();let exported;
  const context=vm.createContext({
    document:{body:new Element(),getElementById:id=>elements[id],createElement:tag=>new Element(tag),addEventListener(){}},
    window:{addEventListener(){},scrollTo(){}},location:{search:'?quick=1'},URLSearchParams,Blob,
    URL:{createObjectURL:blob=>{exported=blob;return 'blob:test'},revokeObjectURL(){}},
    localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},
    fetch:async()=>({ok:true,text:async()=>fs.readFileSync(path.join(root,'evals/proposals_v1_Lenny.csv'),'utf8')}),
  });
  const run=code=>vm.runInContext(code,context);
  run(html.split('<script>')[1].split('</script>')[0]);
  elements.member.value='Lenny';
  context.csv=fs.readFileSync(path.join(root,'evals/eval_set_v1.csv'),'utf8');
  run('begin(csv)');
  return {run,elements,exported:()=>exported,storage};
}
test('navigation, export and restoring do not accept unreviewed proposals',async()=>{
  const h=setup();await h.run('loadProposals()');
  assert.equal(h.elements.count.textContent,'0/44 labelled');
  h.run('go(1)');h.run('exportCSV()');
  assert.equal(h.elements.count.textContent,'0/44 labelled');
  assert(!(await h.exported().text()).includes('AI-proposed, accepted'));
  h.run('acceptAndNext()');
  assert.equal(h.elements.count.textContent,'1/44 labelled');
  assert.equal(h.run('labels.V002.origin'),'AI-proposed, accepted');
  h.elements.form.elements.notes.value='Corrected by tester';h.run('acceptAndNext()');
  assert.equal(h.run('labels.V003.origin'),'AI-proposed, corrected');
  h.run('restore();render()');assert.equal(h.elements.count.textContent,'2/44 labelled');
  h.run('exportCSV()');const csv=await h.exported().text();
  assert(csv.includes('AI-proposed, accepted by Lenny'));
  assert(csv.includes('AI-proposed, corrected by Lenny'));
});
test('shared cases remain blank; incomplete acceptance does not advance',async()=>{
  const h=setup();await h.run('loadProposals()');h.run('go(40)');
  assert.equal(h.run('cases[index].id'),'V197');assert.equal(h.run('proposals.V197'),undefined);
  assert.equal(h.elements.form.elements.action.value,'');h.run('acceptAndNext()');
  assert.equal(h.run('cases[index].id'),'V197');assert.equal(h.run('Object.keys(labels).length'),0);
});
