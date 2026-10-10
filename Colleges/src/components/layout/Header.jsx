import { DarkMode, LightMode, Logout, Menu } from '@mui/icons-material';
import {
  AppBar,
  Avatar,
  FormControl,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  Toolbar,
  Tooltip,
  Typography,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { useAuth } from '../../hooks/useAuth';
import { useTheme } from '../../hooks/useTheme';

function Header({ onMenuClick }) {
  const { isDark, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const {
    isPlatform,
    establishments,
    activeEstablishmentId,
    selectEstablishment,
    logout,
  } = useAuth();

  // Le sélecteur ne concerne que les comptes ayant plusieurs établissements
  // (admin école multi-école). Le super admin n'a pas d'établissement actif.
  const showSelector = !isPlatform && establishments.length > 1;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

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

        {showSelector && (
          <FormControl size="small" sx={{ minWidth: 200, mr: 2 }}>
            <InputLabel id="establishment-select-label">Établissement</InputLabel>

            <Select
              labelId="establishment-select-label"
              value={activeEstablishmentId || ''}
              label="Établissement"
              onChange={(event) => selectEstablishment(event.target.value)}
            >
              {establishments.map((est) => (
                <MenuItem key={est.id} value={est.id}>
                  {est.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        )}

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

        <Tooltip title="Se déconnecter">
          <IconButton onClick={handleLogout} sx={{ ml: 1 }} aria-label="Se déconnecter">
            <Logout />
          </IconButton>
        </Tooltip>
      </Toolbar>
    </AppBar>
  );
}

export default Header;
