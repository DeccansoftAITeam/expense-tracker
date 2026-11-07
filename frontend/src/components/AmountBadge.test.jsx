import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, describe, expect, it } from 'vitest'
import AmountBadge from './AmountBadge.jsx'

afterEach(cleanup)

describe('AmountBadge', () => {
  it('shows paise as rupees with 2 decimals', () => {
    render(<AmountBadge paise={25050} />)
    expect(screen.getByText('₹250.50')).toBeTruthy()
  })

  it('marks ₹5,000 and more as large', () => {
    render(<AmountBadge paise={500000} />)
    expect(screen.getByText('₹5,000.00').className).toContain('large')
  })

  it('does not mark ₹4,999.99 as large', () => {
    render(<AmountBadge paise={499999} />)
    expect(screen.getByText('₹4,999.99').className).not.toContain('large')
  })
})
