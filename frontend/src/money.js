// Rule E1: money is integer paise. Never use floats for amounts.

const rupeeFormat = new Intl.NumberFormat('en-IN')

export function formatRupees(paise) {
  const sign = paise < 0 ? '-' : ''
  const abs = Math.abs(paise)
  const rupees = Math.floor(abs / 100)
  const rest = String(abs % 100).padStart(2, '0')
  return `${sign}₹${rupeeFormat.format(rupees)}.${rest}`
}

// "250.5" -> 25050. Returns null when the text is not a valid amount.
export function toPaise(text) {
  const match = /^(\d+)(?:\.(\d{1,2}))?$/.exec(String(text).trim())
  if (!match) return null
  const rupees = Number(match[1])
  const paise = Number((match[2] || '').padEnd(2, '0'))
  return rupees * 100 + paise
}
