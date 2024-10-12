/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
        remotePatterns: [
        {
            protocol: 'http',
            hostname: 'ec2-13-125-58-42.ap-northeast-2.compute.amazonaws.com', 
            port: '8001',
            pathname: '/image/**/**/**',
        },
        ],
    },
};

export default nextConfig;
