import React from 'react';
import { useAuth } from '@site/src/components/PersonalizeButton/useAuth';
import { Redirect } from '@docusaurus/router';
import Layout from '@theme/Layout';

interface AuthGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  redirectTo?: string;
}

const AuthGuard: React.FC<AuthGuardProps> = ({
  children,
  fallback = null,
  redirectTo = '/sign-in'
}) => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    // Show loading state while checking authentication
    return (
      <Layout title="Loading" description="Checking authentication status...">
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          minHeight: '60vh',
          padding: '2rem'
        }}>
          <div>Loading...</div>
        </div>
      </Layout>
    );
  }

  if (!isAuthenticated) {
    // Redirect to sign-in if not authenticated
    return <Redirect to={redirectTo} />;
  }

  // User is authenticated, show the protected content
  return <>{children}</>;
};

export default AuthGuard;