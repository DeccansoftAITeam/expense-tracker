import { useState } from 'react'
import { toPaise } from '../money.js'

export const CATEGORIES = ['food', 'transport', 'bills', 'shopping', 'health', 'other']

function today() {
  return new Date().toISOString().slice(0, 10)
}

function ExpenseForm({ onAdd }) {
  const [description, setDescription] = useState('')
  const [amount, setAmount] = useState('')
  const [spentOn, setSpentOn] = useState(today())
  const [category, setCategory] = useState('other')
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    const amountPaise = toPaise(amount)
    if (amountPaise === null) {
      setError('Enter an amount like 250 or 250.50')
      return
    }
    try {
      await onAdd({ description, amount_paise: amountPaise, spent_on: spentOn, category })
      setDescription('')
      setAmount('')
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <form className="expense-form" onSubmit={handleSubmit}>
      <input
        aria-label="Description"
        placeholder="What did you spend on?"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <input
        aria-label="Amount"
        placeholder="Amount (₹)"
        inputMode="decimal"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
      />
      <input aria-label="Date" type="date" value={spentOn} onChange={(e) => setSpentOn(e.target.value)} />
      <select aria-label="Category" value={category} onChange={(e) => setCategory(e.target.value)}>
        {CATEGORIES.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>
      <button type="submit">Add</button>
      {error && <p className="error">{error}</p>}
    </form>
  )
}

export default ExpenseForm
