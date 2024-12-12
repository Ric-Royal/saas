'use client';

import { ReactNode, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';
import LoadingState from '@/components/shared/LoadingState';

interface ProtectedRouteProps {
  children: ReactNode;
  allowedRoles?: Array<'user' | 'admin'>;
}

export default function ProtectedRoute({ children, allowedRoles }: ProtectedRouteProps) {
  const router = useRouter();
  const pathname = usePathname();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (typeof window === 'undefined') return;

    if (!loading) {
      if (!user) {
        const returnUrl = encodeURIComponent(pathname || '/');
        router.push(`/unauthorized?returnUrl=${returnUrl}`);
        return;
      }

      if (allowedRoles?.length && !allowedRoles.includes(user.role)) {
        router.push('/unauthorized');
        return;
      }
    }
  }, [user, loading, router, pathname, allowedRoles]);

  if (loading) {
    return <LoadingState />;
  }

  if (!user || (allowedRoles?.length && !allowedRoles.includes(user.role))) {
    return null;
  }

  return <>{children}</>;
} 