import { useState } from 'react';

const Layout = ({ children }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <div className="layout">
      <header className="header">
        <nav className="nav">
          <div className="logo glitch-effect">
            <h1>Tech_Blog.exe</h1>
          </div>

          {/* Hamburger Menu */}
          <div className="hamburger" onClick={toggleMenu}>
            <span></span>
            <span></span>
            <span></span>
          </div>

          {/* Navigation Links */}
          <div className={`nav-links ${isMenuOpen ? 'active' : ''}`}>
            <a href="/" className="glitch-effect">HOME.html</a>
            <a href="/posts" className="glitch-effect">POSTS.txt</a>
            <a href="/categories" className="glitch-effect">CATEGORIES.dat</a>
            <a href="/tags" className="glitch-effect">TAGS.sys</a>
            {/* Conditional rendering for authenticated users */}
            <a href="/dashboard" className="glitch-effect">DASHBOARD.exe</a>
            <a href="/profile" className="glitch-effect">PROFILE.cfg</a>
          </div>
        </nav>
      </header>

      {/* Retro-style breadcrumb */}
      <div className="breadcrumb">
        <span>C:\\TECH_BLOG\\</span>
        <span className="blink">_</span>
      </div>

      {/* Main content */}
      <main className="content">
        {children}
      </main>

      {/* Footer with ASCII art */}
      <footer className="footer">
        <pre className="ascii-art">
          {`
          +-+-+-+-+-+-+-+-+
          |T|E|C|H|B|L|O|G|
          +-+-+-+-+-+-+-+-+
          `}
        </pre>
        <div className="footer-links">
          <a href="/about">ABOUT.txt</a>
          <a href="/contact">CONTACT.exe</a>
          <a href="/privacy">PRIVACY.doc</a>
        </div>
        <div className="copyright">
          © {new Date().getFullYear()} TECH_BLOG.exe - All rights reserved
        </div>
      </footer>

      {/* Additional 90s style elements */}
      <div className="retro-elements">
        <div className="visitor-counter">
          <span>Visitors: 000,042</span>
        </div>
        <div className="best-viewed">
          <span>Best viewed with Netscape Navigator</span>
        </div>
      </div>
    </div>
  );
};

export default Layout; 