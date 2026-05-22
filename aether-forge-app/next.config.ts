import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Force React 19 concurrent features to keep infinite canvas computations non-blocking
  experimental: {
    optimizePackageImports: ["lucide-react"],
  },
};

export default nextConfig;