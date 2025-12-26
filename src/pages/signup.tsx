import React from 'react';
import Layout from '@theme/Layout';
import SignupForm from '@site/src/components/SignupForm';

function Signup() {
  return (
    <Layout title="Sign Up" description="Create an account to access personalized content">
      <div style={{ padding: '2rem', maxWidth: '600px', margin: '0 auto' }}>
        <SignupForm />
      </div>
    </Layout>
  );
}

export default Signup;