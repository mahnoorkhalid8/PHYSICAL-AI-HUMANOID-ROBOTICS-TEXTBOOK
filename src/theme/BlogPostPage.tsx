import React from 'react';
import OriginalBlogPostPage from '@theme-original/BlogPostPage';

// Blog posts remain public to allow users to preview content
// Only book content (docs) requires authentication
const ProtectedBlogPostPage = (props) => {
  return <OriginalBlogPostPage {...props} />;
};

export default ProtectedBlogPostPage;