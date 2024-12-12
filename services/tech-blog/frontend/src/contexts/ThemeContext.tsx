import React, { createContext, useContext, useState, useEffect } from 'react';

interface ThemeContextType {
  isDark: boolean;
  isRetro: boolean;
  toggleTheme: () => void;
  toggleRetro: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [isDark, setIsDark] = useState(true);
  const [isRetro, setIsRetro] = useState(true);

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme');
    const savedRetro = localStorage.getItem('retro');
    if (savedTheme) setIsDark(savedTheme === 'dark');
    if (savedRetro) setIsRetro(savedRetro === 'true');
  }, []);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', isDark);
    document.documentElement.classList.toggle('retro', isRetro);
  }, [isDark, isRetro]);

  const toggleTheme = () => {
    setIsDark(!isDark);
    localStorage.setItem('theme', !isDark ? 'dark' : 'light');
  };

  const toggleRetro = () => {
    setIsRetro(!isRetro);
    localStorage.setItem('retro', (!isRetro).toString());
  };

  return (
    <ThemeContext.Provider value={{ isDark, isRetro, toggleTheme, toggleRetro }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
} 