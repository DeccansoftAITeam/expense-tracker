import { expect, test } from '@playwright/test'

// Each test uses a unique description, so old rows in the database do not matter.
const unique = (text) => `${text} ${Date.now()}-${Math.floor(Math.random() * 1000)}`

async function addExpense(page, { description, amount, category = 'other' }) {
  await page.getByLabel('Description', { exact: true }).fill(description)
  await page.getByLabel('Amount', { exact: true }).fill(amount)
  await page.getByLabel('Category', { exact: true }).selectOption(category)
  await page.getByRole('button', { name: 'Add' }).click()
  await expect(page.getByRole('cell', { name: description })).toBeVisible()
}

test.beforeEach(async ({ page }) => {
  await page.goto('/')
})

test('shows the app title and heading', async ({ page }) => {
  await expect(page).toHaveTitle('Expense Tracker')
  await expect(page.getByRole('heading', { name: 'Expense Tracker' })).toBeVisible()
})

test('adds an expense and shows the amount in rupees', async ({ page }) => {
  const description = unique('Lunch')
  await addExpense(page, { description, amount: '250.50', category: 'food' })
  const row = page.getByRole('row').filter({ hasText: description })
  await expect(row).toContainText('₹250.50')
  await expect(row).toContainText('food')
})

test('rejects an amount that is not a number', async ({ page }) => {
  await page.getByLabel('Description', { exact: true }).fill(unique('Bad'))
  await page.getByLabel('Amount', { exact: true }).fill('abc')
  await page.getByRole('button', { name: 'Add' }).click()
  await expect(page.getByText('Enter an amount like 250 or 250.50')).toBeVisible()
})

test('filters by category', async ({ page }) => {
  const food = unique('Dosa')
  const bus = unique('Bus pass')
  await addExpense(page, { description: food, amount: '80', category: 'food' })
  await addExpense(page, { description: bus, amount: '500', category: 'transport' })
  await page.getByLabel('Filter by category').selectOption('transport')
  await expect(page.getByRole('cell', { name: bus })).toBeVisible()
  await expect(page.getByRole('cell', { name: food })).toHaveCount(0)
})

test('search ignores case', async ({ page }) => {
  const description = unique('Coconut Water')
  await addExpense(page, { description, amount: '40' })
  await page.getByLabel('Search descriptions').fill('coconut water')
  await expect(page.getByRole('cell', { name: description })).toBeVisible()
})

test('archive hides an expense and "Show archived" brings it back', async ({ page }) => {
  const description = unique('Mistake')
  await addExpense(page, { description, amount: '10' })
  await page.getByRole('row').filter({ hasText: description }).getByRole('button', { name: 'Archive' }).click()
  await expect(page.getByRole('cell', { name: description })).toHaveCount(0)
  await page.getByLabel('Show archived').check()
  await expect(page.getByRole('cell', { name: description })).toBeVisible()
})

test('expenses persist after a page reload', async ({ page }) => {
  const description = unique('Electricity')
  await addExpense(page, { description, amount: '1200', category: 'bills' })
  await page.reload()
  await expect(page.getByRole('cell', { name: description })).toBeVisible()
})
