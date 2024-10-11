/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        remotePatterns: [
        {
            protocol: 'http',
            hostname: 'ec2-43-201-64-153.ap-northeast-2.compute.amazonaws.com', 
            port: '8001',
            pathname: '/image/compressed/**',
        },
        ],
    },
};

export default nextConfig;
