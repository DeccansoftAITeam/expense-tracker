import { useEffect, useState } from 'react'
import { getBudgets, getSummary } from '../api.js'
import { formatRupees } from '../money.js'

function thisMonth() {
  return new Date().toISOString().slice(0, 7)
}

function MonthlySummary({ refreshKey }) {
  const [month, setMonth] = useState(thisMonth())
  const [summary, setSummary] = useState(null)
  const [budgets, setBudgets] = useState({})

  useEffect(() => {
    getSummary(month).then(setSummary).catch(() => setSummary(null))
    getBudgets(month)
      .then((list) => setBudgets(Object.fromEntries(list.map((b) => [b.category, b]))))
      .catch(() => setBudgets({}))
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
            {Object.entries(summary.by_category).map(([category, paise]) => {
              const budget = budgets[category]
              return (
                <tr key={category} className={budget?.over ? 'over-budget' : ''}>
                  <td>
                    {category}
                    {budget?.over && <span className="tag warning">over budget</span>}
                  </td>
                  <td className="budget">{budget ? `of ${formatRupees(budget.limit_paise)}` : ''}</td>
                  <td className="amount">{formatRupees(paise)}</td>
                </tr>
              )
            })}
            <tr className="total">
              <td>Total</td>
              <td></td>
              <td className="amount">{formatRupees(summary.total_paise)}</td>
            </tr>
          </tbody>
        </table>
      )}
    </section>
  )
}

export default MonthlySummary
