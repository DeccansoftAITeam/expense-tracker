import { formatRupees } from '../money.js'

function ExpenseList({ expenses, onArchive }) {
  if (expenses.length === 0) {
    return <p className="empty">No expenses yet</p>
  }
  return (
    <table className="expense-list">
      <thead>
        <tr>
          <th>Date</th>
          <th>Description</th>
          <th>Category</th>
          <th className="amount">Amount</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {expenses.map((expense) => (
          <tr key={expense.id} className={expense.archived ? 'archived' : ''}>
            <td>{expense.spent_on}</td>
            <td>{expense.description}</td>
            <td>{expense.category}</td>
            <td className="amount">{formatRupees(expense.amount_paise)}</td>
            <td>
              <button type="button" onClick={() => onArchive(expense.id, !expense.archived)}>
                {expense.archived ? 'Restore' : 'Archive'}
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default ExpenseList
