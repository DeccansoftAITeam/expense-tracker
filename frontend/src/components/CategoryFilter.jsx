import { CATEGORIES } from './ExpenseForm.jsx'

function CategoryFilter({ value, onChange }) {
  return (
    <label>
      Category{' '}
      <select aria-label="Filter by category" value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">All</option>
        {CATEGORIES.map((c) => (
          <option key={c} value={c}>
            {c}
          </option>
        ))}
      </select>
    </label>
  )
}

export default CategoryFilter
