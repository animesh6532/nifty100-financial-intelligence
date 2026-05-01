export const formatters = {
  currency: (value) => new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
  }).format(value),
  
  percentage: (value) => `${(value * 100).toFixed(2)}%`,
  
  number: (value) => new Intl.NumberFormat('en-IN').format(value),
}
