import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Tech Blog',
  description: 'A modern tech blog built with Next.js',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex">
                <Link
                  href="/"
                  className="flex items-center px-2 text-gray-900 font-semibold"
                >
                  Tech Blog
                </Link>
                <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
                  <Link
                    href="/posts"
                    className="inline-flex items-center px-1 pt-1 text-gray-500 hover:text-gray-900"
                  >
                    Posts
                  </Link>
                  <Link
                    href="/posts/new"
                    className="inline-flex items-center px-1 pt-1 text-gray-500 hover:text-gray-900"
                  >
                    Write
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>
        <main className="min-h-screen bg-gray-50">{children}</main>
        <footer className="bg-white border-t">
          <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
            <p className="text-center text-gray-500 text-sm">
              © {new Date().getFullYear()} Tech Blog. All rights reserved.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
} 