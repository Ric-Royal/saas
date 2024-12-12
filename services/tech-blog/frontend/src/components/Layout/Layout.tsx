import React, { useState } from 'react';
import Link from 'next/link';
import { useTheme } from '@/contexts/ThemeContext';
import { useAuth } from '@/contexts/AuthContext';
import { FaTerminal, FaSun, FaMoon, FaRegWindowRestore } from 'react-icons/fa';
import { RetroAlert } from '../RetroAlert/RetroAlert';
import { RetroMenu } from '../RetroMenu/RetroMenu';

interface LayoutProps {
  children: React.ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const { isDark, isRetro, toggleTheme, toggleRetro } = useTheme();
  const { user, logout } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [showAlert, setShowAlert] = useState(false);

  const handleLogout = async () => {
    try {
      await logout();
      setShowAlert(true);
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className={`layout ${isDark ? 'dark' : 'light'} ${isRetro ? 'retro' : 'modern'}`}>
      <header className="header">
        <nav className="nav">
          <div className="logo glitch-effect">
            <Link href="/">
              <FaTerminal className="inline-block mr-2" />
              <span>Tech_Blog.exe</span>
            </Link>
          </div>

          <div className="theme-toggles">
            <button onClick={toggleTheme} className="retro-button">
              {isDark ? <FaSun /> : <FaMoon />}
            </button>
            <button onClick={toggleRetro} className="retro-button ml-2">
              <FaRegWindowRestore />
            </button>
          </div>

          <RetroMenu
            isOpen={isMenuOpen}
            onClose={() => setIsMenuOpen(false)}
            items={[
              { label: 'HOME.html', href: '/' },
              { label: 'POSTS.txt', href: '/posts' },
              { label: 'CATEGORIES.dat', href: '/categories' },
              { label: 'TAGS.sys', href: '/tags' },
              ...(user ? [
                { label: 'DASHBOARD.exe', href: '/dashboard' },
                { label: 'PROFILE.cfg', href: '/profile' },
                { label: 'LOGOUT.bat', onClick: handleLogout }
              ] : [
                { label: 'LOGIN.exe', href: '/login' },
                { label: 'REGISTER.com', href: '/register' }
              ])
            ]}
          />

          <div className="hamburger" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </nav>
      </header>

      <div className="breadcrumb">
        <span>C:\\TECH_BLOG\\</span>
        <span className="blink">_</span>
      </div>

      <main className="content">
        {children}
      </main>

      <footer className="footer">
        <pre className="ascii-art">
          {`
          +-+-+-+-+-+-+-+-+
          |T|E|C|H|B|L|O|G|
          +-+-+-+-+-+-+-+-+
          `}
        </pre>
        <div className="footer-links">
          <Link href="/about">ABOUT.txt</Link>
          <Link href="/contact">CONTACT.exe</Link>
          <Link href="/privacy">PRIVACY.doc</Link>
        </div>
        <div className="copyright">
          © {new Date().getFullYear()} TECH_BLOG.exe - All rights reserved
        </div>
      </footer>

      <div className="retro-elements">
        <div className="visitor-counter">
          <span>Visitors: 000,042</span>
        </div>
        <div className="best-viewed">
          <span>Best viewed with Netscape Navigator</span>
        </div>
      </div>

      {showAlert && (
        <RetroAlert
          message="Successfully logged out. Please come back using Netscape Navigator!"
          onClose={() => setShowAlert(false)}
        />
      )}
    </div>
  );
} 