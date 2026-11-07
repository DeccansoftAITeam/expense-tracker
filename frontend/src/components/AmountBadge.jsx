import { formatRupees } from '../money.js'

export const LARGE_EXPENSE_PAISE = 500000 // ₹5,000

function AmountBadge({ paise }) {
  const large = paise >= LARGE_EXPENSE_PAISE
  return (
    <span className={large ? 'amount-badge large' : 'amount-badge'} title={large ? 'Large expense' : undefined}>
      {formatRupees(paise)}
    </span>
  )
}

export default AmountBadge
