import { describe, expect, it } from 'vitest'
import { formatRupees, toPaise } from './money.js'

describe('money (E1: integer paise)', () => {
  it('formats paise with Indian grouping', () => {
    expect(formatRupees(10000000)).toBe('₹1,00,000.00')
  })

  it('converts rupee text to paise without floats', () => {
    expect(toPaise('250.5')).toBe(25050)
    expect(toPaise('0.07')).toBe(7)
    expect(toPaise('19.99')).toBe(1999)
  })

  it('rejects text that is not an amount', () => {
    expect(toPaise('abc')).toBeNull()
    expect(toPaise('1.234')).toBeNull()
  })
})
