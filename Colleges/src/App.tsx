import { CssBaseline, ThemeProvider as MuiThemeProvider } from '@mui/material';

import { useContext } from 'react';
import { AuthProvider } from './context/AuthContext';
import { ThemeContext, ThemeProvider } from './context/ThemeContext';
import AppRoutes from './routes/AppRoutes';

function AppContent() {
  const { theme } = useContext(ThemeContext);

  return (
    <MuiThemeProvider theme={theme}>
      <CssBaseline />
      <AppRoutes />
    </MuiThemeProvider>
  );
}

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
