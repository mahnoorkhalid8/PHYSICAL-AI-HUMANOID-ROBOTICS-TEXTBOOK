import React, { useState } from 'react';
import { useHistory } from '@docusaurus/router';
import './SignupForm.css';

interface FormData {
  email: string;
  password: string;
  name?: string;
  software_background: string;
  hardware_background: string;
}

const SignupForm: React.FC = () => {
  const history = useHistory();
  const [formData, setFormData] = useState<FormData>({
    email: '',
    password: '',
    name: '',
    software_background: '',
    hardware_background: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (!formData.software_background) {
      newErrors.software_background = 'Software background is required';
    } else if (formData.software_background.length < 2 || formData.software_background.length > 200) {
      newErrors.software_background = 'Software background must be between 2 and 200 characters';
    }

    if (!formData.hardware_background) {
      newErrors.hardware_background = 'Hardware background is required';
    } else if (formData.hardware_background.length < 2 || formData.hardware_background.length > 200) {
      newErrors.hardware_background = 'Hardware background must be between 2 and 200 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // In a real implementation, this would call the Better Auth signup API
      console.log('Signup data:', formData);

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      alert('Account created successfully!');

      // In a real implementation, after successful signup, we would:
      // 1. Store user session/token
      // 2. Update local auth state
      // 3. Redirect to book content

      // Store mock user data in localStorage to simulate successful authentication
      const mockUser = {
        id: `user_${Date.now()}`, // Generate a mock user ID
        email: formData.email,
        name: formData.name || undefined,
        software_background: formData.software_background,
        hardware_background: formData.hardware_background,
      };

      // Create a mock JWT token (properly formatted with header.payload.signature)
      // In a real implementation, this would come from the Better Auth API
      // Using btoa for base64 encoding (browser API)

      // Helper function to encode base64 URL-safe string
      const base64Encode = (str: string) => {
        return btoa(str)
          .replace(/\+/g, '-')
          .replace(/\//g, '_')
          .replace(/=/g, '');
      };

      const header = base64Encode(JSON.stringify({ alg: 'HS256', typ: 'JWT' }));
      const payload = base64Encode(JSON.stringify({
        sub: `user_${Date.now()}`,
        email: formData.email,
        exp: Math.floor(Date.now() / 1000) + (60 * 60 * 24), // 24 hours from now
        iat: Math.floor(Date.now() / 1000),
        software_background: formData.software_background,
        hardware_background: formData.hardware_background
      }));
      const signature = base64Encode('mock_signature_for_development'); // This is just for development

      const mockToken = `${header}.${payload}.${signature}`;

      // Store user and token in localStorage to match the format expected by useAuth
      localStorage.setItem('better-auth-user', JSON.stringify(mockUser));
      localStorage.setItem('better-auth-token', mockToken);

      // For now, redirect to the book intro page after successful signup
      history.push('/docs/intro');
    } catch (error) {
      console.error('Signup error:', error);
      alert('An error occurred during signup. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="signup-form-container">
      <div className="signup-form-card">
        <h2 className="signup-form-title">Create Account</h2>
        <p className="signup-form-subtitle">Join to access personalized content</p>

        <form onSubmit={handleSubmit} className="signup-form">
          <div className="form-group">
            <label htmlFor="name" className="form-label">Name (Optional)</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className={`form-input ${errors.name ? 'form-input-error' : ''}`}
              placeholder="Enter your name"
            />
            {errors.name && <span className="error-message">{errors.name}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="email" className="form-label">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={`form-input ${errors.email ? 'form-input-error' : ''}`}
              placeholder="Enter your email"
            />
            {errors.email && <span className="error-message">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              className={`form-input ${errors.password ? 'form-input-error' : ''}`}
              placeholder="Create a password"
            />
            {errors.password && <span className="error-message">{errors.password}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="software_background" className="form-label">
              Software Background <span className="required">*</span>
            </label>
            <select
              id="software_background"
              name="software_background"
              value={formData.software_background}
              onChange={handleChange}
              className={`form-input ${errors.software_background ? 'form-input-error' : ''}`}
            >
              <option value="">Select your software background</option>
              <option value="Beginner">Beginner (Learning)</option>
              <option value="Intermediate">Intermediate (Some experience)</option>
              <option value="Advanced">Advanced (Expert)</option>
              <option value="Expert">Expert (Professional)</option>
              <option value="Other">Other (Please specify)</option>
            </select>
            {formData.software_background === 'Other' && (
              <textarea
                name="software_background"
                value={formData.software_background}
                onChange={handleChange}
                className={`form-input ${errors.software_background ? 'form-input-error' : ''}`}
                placeholder="Please describe your software background"
                rows={3}
              />
            )}
            {errors.software_background && <span className="error-message">{errors.software_background}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="hardware_background" className="form-label">
              Hardware Background <span className="required">*</span>
            </label>
            <select
              id="hardware_background"
              name="hardware_background"
              value={formData.hardware_background}
              onChange={handleChange}
              className={`form-input ${errors.hardware_background ? 'form-input-error' : ''}`}
            >
              <option value="">Select your hardware background</option>
              <option value="Beginner">Beginner (Learning)</option>
              <option value="Intermediate">Intermediate (Some experience)</option>
              <option value="Advanced">Advanced (Some experience)</option>
              <option value="Expert">Expert (Professional)</option>
              <option value="Other">Other (Please specify)</option>
            </select>
            {formData.hardware_background === 'Other' && (
              <textarea
                name="hardware_background"
                value={formData.hardware_background}
                onChange={handleChange}
                className={`form-input ${errors.hardware_background ? 'form-input-error' : ''}`}
                placeholder="Please describe your hardware background"
                rows={3}
              />
            )}
            {errors.hardware_background && <span className="error-message">{errors.hardware_background}</span>}
          </div>

          <button
            type="submit"
            className={`signup-form-button ${isLoading ? 'button-loading' : ''}`}
            disabled={isLoading}
          >
            {isLoading ? 'Creating Account...' : 'Create Account'}
          </button>
        </form>

        <p className="signup-form-footer">
          Already have an account? <a href="/sign-in">Sign in</a>
        </p>
      </div>
    </div>
  );
};

export default SignupForm;