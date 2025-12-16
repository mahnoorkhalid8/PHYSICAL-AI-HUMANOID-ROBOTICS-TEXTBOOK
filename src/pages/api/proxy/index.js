export default async function handler(req, res) {
  try {
    // Get the original URL and extract the path after /api/
    const { pathname } = new URL(req.url, `https://${req.headers.host}`);
    const backendPath = pathname.replace(/^\/api\/proxy/, '/api'); // Convert /api/proxy to /api/

    // Get the backend URL from environment variables or use a default
    const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'; // Replace with your actual backend URL when deployed

    // Build the target URL
    const targetUrl = `${backendUrl}${backendPath}`;

    // Prepare the request options
    const options = {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    // Add body if present
    if (req.body && Object.keys(req.body).length > 0) {
      options.body = JSON.stringify(req.body);
    }

    // Forward the request to the backend
    const response = await fetch(targetUrl, options);

    // Get the response data
    const data = await response.json();

    // Return the response with the same status as the backend
    return res.status(response.status).json(data);
  } catch (error) {
    console.error('Proxy error:', error);
    return res.status(500).json({
      error: 'Proxy error',
      message: 'Failed to connect to the backend service'
    });
  }
}

export const config = {
  api: {
    bodyParser: true,
  },
};