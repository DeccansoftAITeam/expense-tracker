import { useCallback, useEffect, useState } from 'react'
import { createExpense, listExpenses, setArchived } from './api.js'
import ExpenseForm from './components/ExpenseForm.jsx'
import ExpenseList from './components/ExpenseList.jsx'

function App() {
  const [expenses, setExpenses] = useState([])
  const [showArchived, setShowArchived] = useState(false)

  const refresh = useCallback(async () => {
    setExpenses(await listExpenses({ includeArchived: showArchived }))
  }, [showArchived])

  useEffect(() => {
    refresh()
  }, [refresh])

  async function handleAdd(expense) {
    await createExpense(expense)
    await refresh()
  }

  async function handleArchive(id, archived) {
    await setArchived(id, archived)
    await refresh()
  }

  return (
    <main className="app">
      <h1>Expense Tracker</h1>
      <ExpenseForm onAdd={handleAdd} />
      <div className="toolbar">
        <label>
          <input type="checkbox" checked={showArchived} onChange={(e) => setShowArchived(e.target.checked)} /> Show
          archived
        </label>
      </div>
      <ExpenseList expenses={expenses} onArchive={handleArchive} />
    </main>
  )
}

export default App
