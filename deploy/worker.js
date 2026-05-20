export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    // SPA fallback: serve index.html for non-file routes
    const response = await env.ASSETS.fetch(request);
    if (response.status === 404 && !url.pathname.includes('.')) {
      return env.ASSETS.fetch(new Request(new URL('/', request.url)));
    }
    return response;
  }
};
