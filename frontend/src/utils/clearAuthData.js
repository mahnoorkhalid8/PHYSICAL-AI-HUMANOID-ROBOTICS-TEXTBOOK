// Clear any existing authentication data on app load to ensure clean state
if (typeof window !== 'undefined' && window.localStorage) {
  // Clear authentication data that might have been set by test components
  if (localStorage.getItem('better-auth-token') || localStorage.getItem('better-auth-user')) {
    console.log('Clearing existing authentication data from localStorage');
    localStorage.removeItem('better-auth-token');
    localStorage.removeItem('better-auth-user');
  }
}