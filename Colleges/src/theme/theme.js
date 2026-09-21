import { createTheme } from '@mui/material/styles';

const commonTypography = {
  fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
};

export const lightTheme = createTheme({
  palette: {
    mode: 'light',

    primary: {
      main: '#2563EB',
      contrastText: '#FFFFFF',
    },

    secondary: {
      main: '#7C3AED',
      contrastText: '#FFFFFF',
    },

    background: {
      default: '#F8FAFC',
      paper: '#FFFFFF',
    },

    text: {
      primary: '#0F172A',
      secondary: '#64748B',
    },

    divider: '#E2E8F0',
  },

  typography: commonTypography,

  shape: {
    borderRadius: 10,
  },

  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },

    MuiTextField: {
      defaultProps: {
        variant: 'outlined',
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});

export const darkTheme = createTheme({
  palette: {
    mode: 'dark',

    primary: {
      main: '#60A5FA',
      contrastText: '#0F172A',
    },

    secondary: {
      main: '#A78BFA',
      contrastText: '#0F172A',
    },

    background: {
      default: '#0F172A',
      paper: '#1E293B',
    },

    text: {
      primary: '#F8FAFC',
      secondary: '#CBD5E1',
    },

    divider: '#334155',
  },

  typography: commonTypography,

  shape: {
    borderRadius: 10,
  },

  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },

    MuiTextField: {
      defaultProps: {
        variant: 'outlined',
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
        },
      },
    },
  },
});
