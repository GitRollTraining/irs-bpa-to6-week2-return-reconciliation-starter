import {useEffect, useRef, useState} from 'react'

async function api(path, options) {
  const response = await fetch(`/api${path}`, options)
  const body = await response.json()
  if (!response.ok) throw new Error(typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail))
  return body
}
export default function App() {
  const [batches, setBatches] = useState([]), [batch, setBatch] = useState(null)
  const [inspections, setInspections] = useState([]), [report, setReport] = useState(null)
  const [name, setName] = useState(''), [expected, setExpected] = useState('')
  const [files, setFiles] = useState([]), [filter, setFilter] = useState('all'), [detail, setDetail] = useState(null)
  const [error, setError] = useState(''), [busy, setBusy] = useState(false)
  const selection = useRef(0)
  useEffect(() => { api('/batches').then(setBatches).catch(e => setError(e.message)) }, [])
  async function run(action) {
    setBusy(true); setError('')
    try { await action() } catch(e) { setError(e.message) } finally { setBusy(false) }
  }
  async function chooseBatch(value) {
    const version = ++selection.current
    setBatch(value); setReport(null); setDetail(null); setInspections([]); setFiles([]); setFilter('all')
    await run(async () => {
      const rows = await api(`/batches/${value.batch_id}/inspections`)
      if (selection.current === version) setInspections(rows)
    })
  }
  async function chooseInspection(id) {
    const version = ++selection.current
    setReport(null); setDetail(null); setFilter('all')
    await run(async () => {
      const value = await api(`/batches/${batch.batch_id}/inspections/${id}`)
      if (selection.current === version) setReport(value)
    })
  }
  function register(event) {
    event.preventDefault()
    run(async () => {
      const identities = expected.split('\n').filter(x => x.trim()).map(line => {
        const [return_id, year, extra] = line.trim().split(',').map(x => x.trim())
        if (!year || extra !== undefined) throw new Error('Use one ID,year pair per line')
        return {return_id, year}
      })
      const value = await api('/batches', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({name, expected:identities})})
      setBatches(await api('/batches')); setName(''); setExpected(''); await chooseBatch(value)
    })
  }
  function upload(event) {
    event.preventDefault()
    const version = ++selection.current
    run(async () => {
      const data = new FormData(); for (const file of files) data.append('files', file)
      const value = await api(`/batches/${batch.batch_id}/inspections`, {method:'POST',body:data})
      const rows = await api(`/batches/${batch.batch_id}/inspections`)
      if (selection.current === version) {setReport(value); setInspections(rows); setDetail(null); setFilter('all')}
    })
  }
  return <main>
    <h1>Return Batch Reconciliation Desk</h1>
    <p>Training transport reconciliation; not tax validation. Synthetic data only.</p>
    {busy && <p role="status">Loading…</p>}{error && <p role="alert">{error}</p>}
    <section><h2>Register batch</h2><form onSubmit={register}>
      <label>Batch name<input required maxLength={100} value={name} onChange={e => setName(e.target.value)}/></label>
      <label>Expected identities (ID,year per line)<textarea required value={expected} onChange={e => setExpected(e.target.value)}/></label>
      <button disabled={busy}>Register batch</button>
    </form></section>
    <section><h2>Registered batches</h2>{!batches.length && <p>No batches yet.</p>}
      {batches.map(b => <button key={b.batch_id} disabled={busy} onClick={() => chooseBatch(b)}>{b.name} · {b.batch_id.slice(0,8)}</button>)}
    </section>
    {batch && <section><h2>Batch: {batch.name}</h2><p>Batch ID: {batch.batch_id}</p>
      <p>Expected: {batch.expected.map(x => `${x.return_id}/${x.year}`).join(', ')}</p>
      <form onSubmit={upload}><label>Complete delivery XML files<input key={batch.batch_id} type="file" multiple required onChange={e => setFiles([...e.target.files])}/></label><button disabled={busy || !files.length}>Inspect delivery</button></form>
      <h3>Inspections</h3>{!inspections.length && <p>No inspections yet.</p>}
      {inspections.map(i => <button key={i.inspection_id} disabled={busy} onClick={() => chooseInspection(i.inspection_id)}>{i.inspection_id} · {i.ready ? 'Ready' : 'Blocked'}</button>)}
    </section>}
    {report && <section><h2>{report.ready ? 'Ready for handoff' : 'Blocked handoff'}</h2><p>Inspection: {report.inspection_id}</p>
      <p data-testid="counts">{Object.entries(report.counts).map(([k,v]) => `${k}: ${v}`).join(' · ')}</p>
      <p>Missing means no usable identified file was found, not proof of what an unreadable file contains.</p>
      <p>Missing: {report.missing.map(x => `${x.return_id}/${x.year}`).join(', ') || 'None'}</p>
      <a href={`/api/batches/${report.batch_id}/inspections/${report.inspection_id}`} download>Download JSON report</a>
      <label>Filter outcome<select value={filter} onChange={e => {setFilter(e.target.value);setDetail(null)}}>{['all','matched','duplicate','unexpected','invalid'].map(x => <option key={x}>{x}</option>)}</select></label>
      <ul>{report.files.filter(f => filter === 'all' || f.outcome === filter).map(f => <li key={f.file_id}><button onClick={() => setDetail(f)}>{f.filename} — {f.outcome}</button></li>)}</ul>
      {detail && <article><h3>File details: {detail.filename}</h3><p>File ID: {detail.file_id}</p>
        {detail.record && <><p>Identity: {detail.record.return_id}/{detail.record.year}</p><p>Filer: {detail.record.filer_name}</p><p>Contact: {detail.record.contact === null ? '(absent)' : detail.record.contact === '' ? '(explicitly empty)' : detail.record.contact}</p><ol>{detail.record.income.map((entry,i) => <li key={i}>{entry.label}: {entry.amount}</li>)}</ol></>}
        {detail.issues.map((issue,i) => <pre key={i}>{JSON.stringify(issue,null,2)}</pre>)}
      </article>}
    </section>}
  </main>
}
