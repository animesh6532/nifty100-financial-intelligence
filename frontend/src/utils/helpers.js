export const helpers = {
  getInitials: (name) => name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase(),
}
