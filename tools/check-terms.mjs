import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {fileURLToPath,pathToFileURL} from 'node:url';
import path from 'node:path';
import {createHash} from 'node:crypto';

// Optional sibling app checkout root; no network, publishing or DayLeaf changes.
const site=fileURLToPath(new URL('../',import.meta.url));
const apps=path.resolve(process.argv[2]||path.join(site,'..'));
const decode=s=>s.replaceAll('&quot;','"').replaceAll('&#x27;',"'").replaceAll('&#39;',"'").replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&');
for(const [folder,slug] of [['FQ-Lite','firmquill-lite'],['FQ-Full-Suite','firmquill-full-suite'],['CurbQuill','curbquill'],['MileQuill-Lite','milequill-lite'],['PocketQuill','pocketquill'],['Launcher','filebirch'],['ScreenQuill','screenquill']]){
 let text,version;
 if(folder==='FQ-Full-Suite'){
  const doc=await import(pathToFileURL(path.join(apps,folder,'web/legal/terms.mjs')));text=doc.termsText;version=doc.termsVersion;
 }else if(folder==='Launcher'||folder==='ScreenQuill'){
  text=await readFile(path.join(apps,folder,folder==='Launcher'?'tos.md':'SopRecorder/terms.md'),'utf8');version=/Version ([\d.]+)/.exec(text)[1];
 }else{
  const doc=JSON.parse(await readFile(path.join(apps,folder,'terms.json'),'utf8'));text=doc.text;version=doc.version;
 }
 text=text.replace(/\r\n?/g,'\n');
 const html=await readFile(path.join(site,'terms',slug,'index.html'),'utf8');
 const article=/<article data-terms-version="([^"]+)">\s*([\s\S]*?)<\/article>/.exec(html);assert.ok(article,folder+' article');assert.equal(article[1],version);
 const actual=[...article[2].matchAll(/<(h1|h2|p)>([\s\S]*?)<\/\1>/g)].map(m=>decode(m[2])).join('\n\n');
 assert.equal(actual,text.trim().replace(/^#{1,2} /gm,''),folder+' legal text differs');
 if(folder==='Launcher'||folder==='ScreenQuill'){
  const digest=createHash('sha256').update(text).digest('hex');assert.ok(html.includes('content="'+digest+'"'),folder+' canonical metadata');assert.ok(html.includes('name="terms-status" content="approved"'));
 }
 console.log(folder+' · identical agreement and version '+version);
}
