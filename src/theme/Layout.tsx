import React from 'react';
import { AuthProvider } from '@site/src/components/PersonalizeButton/useAuth';
import OriginalLayout from '@theme-original/Layout';

const Layout = (props) => {
  return (
    <AuthProvider>
      <OriginalLayout {...props}>{props.children}</OriginalLayout>
    </AuthProvider>
  );
};

export default Layout;