import { createTheme } from '@mui/material/styles';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',

    primary: {
      main: '#60A5FA',
    },

    secondary: {
      main: '#A78BFA',
    },

    background: {
      default: '#0F172A',
      paper: '#1E293B',
    },

    text: {
      primary: '#F8FAFC',
      secondary: '#94A3B8',
    },

    divider: '#334155',
  },

  shape: {
    borderRadius: 10,
  },

  typography: {
    fontFamily: ['Inter', 'Roboto', 'Arial', 'sans-serif'].join(','),
  },

  components: {
    MuiButton: {
      defaultProps: {
        disableElevation: true,
      },

      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
          fontWeight: 600,
        },
      },
    },

    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.25)',
        },
      },
    },

    MuiTextField: {
      defaultProps: {
        size: 'small',
      },
    },

    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
});

export default darkTheme;
