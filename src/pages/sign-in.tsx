import React, { useState } from 'react';
import Layout from '@theme/Layout';
import { useHistory } from '@docusaurus/router';

function SignIn() {
  const history = useHistory();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      // In a real implementation, this would call the Better Auth sign-in API
      console.log('Sign-in attempt:', formData);

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Mock authentication - store user data in localStorage
      const mockUser = {
        id: `user_${Date.now()}`,
        email: formData.email,
        name: formData.email.split('@')[0], // Use part of email as name
        software_background: 'Intermediate', // Default or retrieved from stored data
        hardware_background: 'Intermediate'  // Default or retrieved from stored data
      };

      const mockToken = `mock_token_${Date.now()}`;

      // Store user and token in localStorage to match the format expected by useAuth
      localStorage.setItem('better-auth-user', JSON.stringify(mockUser));
      localStorage.setItem('better-auth-token', mockToken);

      // In a real app, we would receive the user and token from the auth API
      // and update the auth context accordingly

      // Redirect to book after successful sign-in
      history.push('/docs/intro');
    } catch (err) {
      console.error('Sign-in error:', err);
      setError('Invalid email or password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
        <div className="login-form-container">
          <div className="login-form-card">
            <h2 className="login-form-title">Sign In</h2>
            <p className="login-form-subtitle">Access your personalized content</p>

            <form onSubmit={handleSubmit} className="login-form">
              <div className="form-group">
                <label htmlFor="email" className="form-label">Email</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="Enter your email"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="password" className="form-label">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="Enter your password"
                  required
                />
              </div>

              {error && (
                <div className="error-message" style={{ color: '#e74c3c', marginBottom: '1rem', textAlign: 'center' }}>
                  {error}
                </div>
              )}

              <button
                type="submit"
                className={`login-form-button ${isLoading ? 'button-loading' : ''}`}
                disabled={isLoading}
              >
                {isLoading ? 'Signing In...' : 'Sign In'}
              </button>
            </form>

            <p className="login-form-footer">
              Don't have an account? <a href="/signup">Sign up</a>
            </p>
          </div>
        </div>

        <style jsx>{`
          .login-form-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 60vh;
          }

          .login-form-card {
            background: white;
            border-radius: 8px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
          }

          .login-form-title {
            margin: 0 0 0.5rem 0;
            font-size: 1.5rem;
            font-weight: 600;
            text-align: center;
          }

          .login-form-subtitle {
            margin: 0 0 1.5rem 0;
            color: #666;
            text-align: center;
            font-size: 0.9rem;
          }

          .form-group {
            margin-bottom: 1rem;
          }

          .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #333;
          }

          .form-input {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
          }

          .form-input:focus {
            outline: none;
            border-color: #007cba;
            box-shadow: 0 0 0 2px rgba(0, 124, 186, 0.2);
          }

          .login-form-button {
            width: 100%;
            padding: 0.75rem;
            background-color: #007cba;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
          }

          .login-form-button:hover {
            background-color: #005a87;
          }

          .login-form-button:disabled {
            background: #bdc3c7;
            cursor: not-allowed;
          }

          .login-form-footer {
            margin-top: 1.5rem;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
          }

          .login-form-footer a {
            color: #007cba;
            text-decoration: none;
          }

          .login-form-footer a:hover {
            text-decoration: underline;
          }
        `}</style>
      </div>
    </Layout>
  );
}

export default SignIn;