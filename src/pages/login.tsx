import React, { useEffect } from 'react';
import { Redirect } from '@docusaurus/router';

function Login() {
  useEffect(() => {
    // Redirect to the new sign-in page
    window.location.href = '/sign-in';
  }, []);

  return <Redirect to="/sign-in" />;
}

export default Login;