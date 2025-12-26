import React from 'react';
import { useLocation } from '@docusaurus/router';
import AuthGuard from '@site/src/components/AuthGuard';
import OriginalDocPage from '@theme-original/DocPage';

const ProtectedDocPage = (props) => {
  const location = useLocation();

  // Protect all doc pages that are part of the book content
  const isBookContent = location.pathname.startsWith('/docs/');

  if (isBookContent) {
    return (
      <AuthGuard redirectTo="/sign-in">
        <OriginalDocPage {...props} />
      </AuthGuard>
    );
  }

  // For non-book content pages, show without auth
  return <OriginalDocPage {...props} />;
};

export default ProtectedDocPage;