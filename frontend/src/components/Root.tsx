import React from 'react';
import { AuthProvider } from './PersonalizeButton/useAuth';

const Root = ({ children }) => {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
};

export default Root;