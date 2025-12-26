import React from 'react';
import { AuthProvider } from '@site/src/components/PersonalizeButton/useAuth';

// Root component to wrap the entire app with providers
const Root: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
};

export default Root;