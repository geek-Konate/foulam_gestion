import { createContext, useEffect, useMemo, useState } from 'react';

import { darkTheme, lightTheme } from '../theme/theme';

export const ThemeContext = createContext(null);

const STORAGE_KEY = 'theme-mode';

export function ThemeProvider({ children }) {
  const [mode, setMode] = useState(() => {
    const savedMode = localStorage.getItem(STORAGE_KEY);

    return savedMode === 'dark' ? 'dark' : 'light';
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, mode);
  }, [mode]);

  const toggleTheme = () => {
    setMode((currentMode) => (currentMode === 'light' ? 'dark' : 'light'));
  };

  const theme = mode === 'light' ? lightTheme : darkTheme;

  const value = useMemo(
    () => ({
      mode,
      theme,
      toggleTheme,
      isDark: mode === 'dark',
    }),
    [mode, theme]
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}
