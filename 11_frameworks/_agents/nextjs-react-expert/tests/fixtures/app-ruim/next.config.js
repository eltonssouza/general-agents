/** @type {import('next').NextConfig} */
module.exports = {
  target: 'serverless',
  images: { domains: ['example.com'] },
  serverRuntimeConfig: { secret: 'x' },
  experimental: {
    ppr: true,
    dynamicIO: true,
    turbopack: {},
    reactCompiler: true,
    serverComponentsExternalPackages: ['sharp'],
    instrumentationHook: true,
  },
  devIndicators: { buildActivity: false },
};
