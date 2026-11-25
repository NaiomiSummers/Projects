import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

for (const folder of ['FQ-Lite','FQ-Full-Suite','CurbQuill','Day-Leaf','MileQuill-Lite','PocketQuill']) {
  const dir = folder === 'FQ-Full-Suite' ? folder + '/web/legal' : folder;
  const full = folder === 'FQ-Full-Suite';
  const doc = full ? await import('../../' + dir + '/terms.mjs')
    : JSON.parse(await readFile(new URL('../../' + dir + '/terms.json',import.meta.url),'utf8'));
  const {appId} = doc;
  const termsVersion = full ? doc.termsVersion : doc.version;
  const termsText = full ? doc.termsText : doc.text;
  const page = await readFile(new URL('../terms/' + appId + '/index.html', import.meta.url),'utf8');
  const article = /<article data-terms-version="([^"]+)">\s*([\s\S]*?)<\/article>/.exec(page);
  assert.ok(article, folder + ' public agreement missing');
  assert.equal(article[1], termsVersion, folder + ' version differs');
  const paragraphs = [...article[2].matchAll(/<(h1|h2|p)>([\s\S]*?)<\/\1>/g)];
  const decode = s => s.replaceAll('&quot;','"').replaceAll('&#x27;',"'").replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&amp;','&');
  assert.equal(paragraphs.map(match=>decode(match[2])).join('\n\n'), termsText.trim(), folder + ' terms differ');
  console.log(folder + ' · identical agreement and version ' + termsVersion);
}

