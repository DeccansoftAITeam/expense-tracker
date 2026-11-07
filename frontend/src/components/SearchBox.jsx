function SearchBox({ value, onChange }) {
  return (
    <input
      type="search"
      aria-label="Search descriptions"
      placeholder="Search descriptions"
      value={value}
      onChange={(e) => onChange(e.target.value)}
    />
  )
}

export function matchesSearch(expense, text) {
  const needle = text.trim().toLowerCase()
  return needle === '' || expense.description.toLowerCase().includes(needle)
}

export default SearchBox
