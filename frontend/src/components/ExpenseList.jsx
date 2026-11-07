import AmountBadge from './AmountBadge.jsx'

function ExpenseList({ expenses, onArchive, onRepeat }) {
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
          <th>Paid by</th>
          <th className="amount">Amount</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {expenses.map((expense) => (
          <tr key={expense.id} className={expense.archived ? 'archived' : ''}>
            <td>{expense.spent_on}</td>
            <td>
              {expense.description}
              {expense.repeat === 'monthly' && <span className="tag">monthly</span>}
            </td>
            <td>{expense.category}</td>
            <td>{expense.payment_method}</td>
            <td className="amount">
              <AmountBadge paise={expense.amount_paise} />
            </td>
            <td className="actions">
              {expense.repeat === 'monthly' && expense.next_id === null && !expense.archived && (
                <button type="button" onClick={() => onRepeat(expense.id)}>
                  Repeat next month
                </button>
              )}
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
