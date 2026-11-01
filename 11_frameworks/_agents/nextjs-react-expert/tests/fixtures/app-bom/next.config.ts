import type { NextConfig } from 'next';
const nextConfig: NextConfig = { cacheComponents: true, reactCompiler: true,
  images: { remotePatterns: [{ hostname: 'example.com' }] } };
export default nextConfig;
