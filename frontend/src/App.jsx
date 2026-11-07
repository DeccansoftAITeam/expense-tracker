import { useCallback, useEffect, useState } from 'react'
import { createExpense, listExpenses, setArchived } from './api.js'
import CategoryFilter from './components/CategoryFilter.jsx'
import ExpenseForm from './components/ExpenseForm.jsx'
import ExpenseList from './components/ExpenseList.jsx'
import MonthlySummary from './components/MonthlySummary.jsx'

function App() {
  const [expenses, setExpenses] = useState([])
  const [showArchived, setShowArchived] = useState(false)
  const [category, setCategory] = useState('')
  const [version, setVersion] = useState(0)

  const refresh = useCallback(async () => {
    setExpenses(await listExpenses({ includeArchived: showArchived, category }))
    setVersion((v) => v + 1)
  }, [showArchived, category])

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
        <CategoryFilter value={category} onChange={setCategory} />
        <label>
          <input type="checkbox" checked={showArchived} onChange={(e) => setShowArchived(e.target.checked)} /> Show
          archived
        </label>
      </div>
      <ExpenseList expenses={expenses} onArchive={handleArchive} />
      <MonthlySummary refreshKey={version} />
    </main>
  )
}

export default App
