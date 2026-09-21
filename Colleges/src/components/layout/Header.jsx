import { DarkMode, LightMode, Menu } from '@mui/icons-material';
import { AppBar, Avatar, IconButton, Toolbar, Tooltip, Typography } from '@mui/material';

import { useTheme } from '../../hooks/useTheme';

function Header({ onMenuClick }) {
  const { isDark, toggleTheme } = useTheme();

  return (
    <AppBar
      position="fixed"
      elevation={0}
      sx={{
        zIndex: (theme) => theme.zIndex.drawer + 1,
        bgcolor: 'background.paper',
        color: 'text.primary',
        borderBottom: 1,
        borderColor: 'divider',
      }}
    >
      <Toolbar sx={{ minHeight: 72 }}>
        <IconButton
          edge="start"
          onClick={onMenuClick}
          sx={{ mr: 2 }}
          aria-label="Ouvrir ou fermer le menu"
        >
          <Menu />
        </IconButton>

        <Typography variant="h6" fontWeight={600} sx={{ flexGrow: 1 }}>
          Tableau de bord
        </Typography>

        <Tooltip title={isDark ? 'Activer le mode clair' : 'Activer le mode sombre'}>
          <IconButton onClick={toggleTheme} sx={{ mr: 1 }} aria-label="Changer le thème">
            {isDark ? <LightMode /> : <DarkMode />}
          </IconButton>
        </Tooltip>

        <Avatar
          sx={{
            width: 38,
            height: 38,
            bgcolor: 'primary.main',
            color: 'primary.contrastText',
          }}
        >
          U
        </Avatar>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
