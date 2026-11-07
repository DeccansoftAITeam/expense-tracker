import { useEffect, useState } from 'react'
import { createExpense, listExpenses } from './api.js'
import ExpenseForm from './components/ExpenseForm.jsx'
import ExpenseList from './components/ExpenseList.jsx'

function App() {
  const [expenses, setExpenses] = useState([])

  async function refresh() {
    setExpenses(await listExpenses())
  }

  useEffect(() => {
    refresh()
  }, [])

  async function handleAdd(expense) {
    await createExpense(expense)
    await refresh()
  }

  return (
    <main className="app">
      <h1>Expense Tracker</h1>
      <ExpenseForm onAdd={handleAdd} />
      <ExpenseList expenses={expenses} />
    </main>
  )
}

export default App
