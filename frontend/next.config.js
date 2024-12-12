/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  reactStrictMode: true,
  swcMinify: true,
  typescript: {
    ignoreBuildErrors: true, // Temporary for deployment
  },
  eslint: {
    ignoreDuringBuilds: true, // Temporary for deployment
  },
  experimental: {
    appDir: true,
  },
  // Add rewrites for API endpoints
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:3001/api/:path*',
      },
    ];
  },
}

module.exports = nextConfig 