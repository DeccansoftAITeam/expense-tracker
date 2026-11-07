import { useEffect, useState } from 'react'
import { getSummary } from '../api.js'
import { formatRupees } from '../money.js'

function thisMonth() {
  return new Date().toISOString().slice(0, 7)
}

function MonthlySummary({ refreshKey }) {
  const [month, setMonth] = useState(thisMonth())
  const [summary, setSummary] = useState(null)

  useEffect(() => {
    getSummary(month).then(setSummary).catch(() => setSummary(null))
  }, [month, refreshKey])

  return (
    <section className="summary">
      <h2>
        Monthly summary{' '}
        <input aria-label="Month" type="month" value={month} onChange={(e) => setMonth(e.target.value)} />
      </h2>
      {summary && (
        <table className="expense-list">
          <tbody>
            {Object.entries(summary.by_category).map(([category, paise]) => (
              <tr key={category}>
                <td>{category}</td>
                <td className="amount">{formatRupees(paise)}</td>
              </tr>
            ))}
            <tr className="total">
              <td>Total</td>
              <td className="amount">{formatRupees(summary.total_paise)}</td>
            </tr>
          </tbody>
        </table>
      )}
    </section>
  )
}

export default MonthlySummary
