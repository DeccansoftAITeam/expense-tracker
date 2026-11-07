export const API_URL = 'http://localhost:8000'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!response.ok) {
    const body = await response.json().catch(() => ({}))
    throw new Error(body.detail ? JSON.stringify(body.detail) : `HTTP ${response.status}`)
  }
  return response.json()
}

export function listExpenses({ includeArchived = false } = {}) {
  const params = new URLSearchParams()
  if (includeArchived) params.set('include_archived', 'true')
  const query = params.toString()
  return request(`/expenses${query ? `?${query}` : ''}`)
}

export function createExpense(expense) {
  return request('/expenses', { method: 'POST', body: JSON.stringify(expense) })
}

export function setArchived(id, archived) {
  return request(`/expenses/${id}`, { method: 'PATCH', body: JSON.stringify({ archived }) })
}
