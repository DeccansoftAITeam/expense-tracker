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

export function listExpenses() {
  return request('/expenses')
}

export function createExpense(expense) {
  return request('/expenses', { method: 'POST', body: JSON.stringify(expense) })
}
