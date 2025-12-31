// Script to set up test authentication data in localStorage
// This simulates a logged-in user with background information

// Test user data
const testUser = {
  id: "test-user-123",
  email: "test@example.com",
  name: "Test User",
  software_background: "Intermediate Python developer with robotics experience",
  hardware_background: "Basic understanding of electronic circuits"
};

// Test JWT token (this works with our mock JWKS server)
const testToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6InRlc3Qta2V5LWlkIiwidHlwIjoiSldUIn0.eyJzdWIiOiJ0ZXN0LXVzZXItMTIzIiwiZW1haWwiOiJ0ZXN0QGV4YW1wbGUuY29tIiwibmFtZSI6IlRlc3QgVXNlciIsInVzZXJfbWV0YWRhdGEiOnsic29mdHdhcmVfYmFja2dyb3VuZCI6IkludGVybWVkaWF0ZSBQeXRob24gZGV2ZWxvcGVyIHdpdGggcm9ib3RpY3MgZXhwZXJpZW5jZSIsImhhcmR3YXJlX2JhY2tncm91bmQiOiJCYXNpYyB1bmRlcnN0YW5kaW5nIG9mIGVsZWN0cm9uaWMgY2lyY3VpdHMifSwiaWF0IjoxNzY2OTg4MTQwLCJleHAiOjE3NjcwNzQ1NDAsIm5iZiI6MTc2Njk4ODE0MCwiaXNzIjoidGVzdC1hdXRoLXNlcnZlciIsImF1ZCI6InRlc3QtYXBwIiwia2lkIjoidGVzdC1rZXktaWQifQ.jW77rpcXhVVs_yLzVtQJB4nzvKst0f64WSliXXbI67MFXlw5ggUnAraoNBPHyeVuc1BAntBZgOPUv3Gn7hK5KTYCC5dLBjP5ax_vkMvaONbIvO6_FbKZEWhQDk9BDWtcObcb4P-oWMkxmcL-0I9uoi9vJLvCarEGqFXw1dU1ryYzk9R6ii8E-ez-bHMeM5NEMt48_YJqujntz7B9RYTxkWo9W1t7ara4lw2uKYX-B33_RJbK9t7VZtZKAEwjuGJrU1OEAk58YytGk9nTt7IEFbXY-dSTJmE4AcoUW1YUxDVfYaxFBTLFnZetr5tX8ouct9CecaCmuWeN4WQW7yiObQ";

// Store the user and token in localStorage
localStorage.setItem('better-auth-user', JSON.stringify(testUser));
localStorage.setItem('better-auth-token', testToken);

console.log('Test authentication data has been set up in localStorage');
console.log('User:', testUser);
console.log('Token is stored (first 20 chars):', testToken.substring(0, 20) + '...');

// Also provide a function to update the token if needed
function setupAuth() {
  localStorage.setItem('better-auth-user', JSON.stringify(testUser));
  localStorage.setItem('better-auth-token', testToken);
  console.log('Authentication data has been set up in localStorage');
}

// Function to clear auth data
function clearAuth() {
  localStorage.removeItem('better-auth-user');
  localStorage.removeItem('better-auth-token');
  console.log('Authentication data has been cleared from localStorage');
}

// Function to check auth status
function checkAuth() {
  const user = localStorage.getItem('better-auth-user');
  const token = localStorage.getItem('better-auth-token');

  if (user && token) {
    console.log('✅ Authentication is set up');
    console.log('User:', JSON.parse(user));
    console.log('Token length:', token.length);
  } else {
    console.log('❌ No authentication data found');
  }
}