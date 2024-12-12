'use client';

import { useEffect } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [loading, user, router]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">Dashboard</h1>
            </div>
            <div className="flex items-center">
              <span className="text-gray-700 mr-4">{user.email}</span>
              <button
                onClick={logout}
                className="bg-indigo-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-medium mb-4">Welcome, {user.name}!</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-indigo-50 p-4 rounded-lg">
                <h3 className="font-medium text-indigo-700">Profile Status</h3>
                <p className="mt-2 text-sm text-gray-600">
                  Email verification:{' '}
                  <span
                    className={`font-medium ${
                      user.isEmailVerified ? 'text-green-600' : 'text-red-600'
                    }`}
                  >
                    {user.isEmailVerified ? 'Verified' : 'Not Verified'}
                  </span>
                </p>
              </div>
              <div className="bg-indigo-50 p-4 rounded-lg">
                <h3 className="font-medium text-indigo-700">Account Type</h3>
                <p className="mt-2 text-sm text-gray-600">
                  Role: <span className="font-medium">{user.role}</span>
                </p>
              </div>
              <div className="bg-indigo-50 p-4 rounded-lg">
                <h3 className="font-medium text-indigo-700">Profile Settings</h3>
                <button
                  onClick={() => router.push('/profile')}
                  className="mt-2 text-sm text-indigo-600 hover:text-indigo-500"
                >
                  Edit Profile →
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
} 