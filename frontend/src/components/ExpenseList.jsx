import { formatRupees } from '../money.js'

function ExpenseList({ expenses }) {
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
        </tr>
      </thead>
      <tbody>
        {expenses.map((expense) => (
          <tr key={expense.id}>
            <td>{expense.spent_on}</td>
            <td>{expense.description}</td>
            <td>{expense.category}</td>
            <td className="amount">{formatRupees(expense.amount_paise)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}

export default ExpenseList
