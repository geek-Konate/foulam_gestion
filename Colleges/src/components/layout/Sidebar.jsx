import {
  AccountTree,
  AdminPanelSettings,
  AssignmentInd,
  CalendarMonth,
  Class,
  Dashboard,
  Description,
  FactCheck,
  FamilyRestroom,
  Grade,
  HowToReg,
  Layers,
  ManageAccounts,
  MenuBook,
  Payment,
  Payments,
  People,
  Quiz,
  Receipt,
  School,
} from '@mui/icons-material';
import {
  Box,
  Divider,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
} from '@mui/material';
import { NavLink } from 'react-router-dom';

import navigationData from '../../data/index.json';

// Permissions strictement réservées au niveau platform (Super Admin).
// Ces entrées ne s'affichent que pour scope === "PLATFORM".
const PLATFORM_PERMISSIONS = ['onboarding.review'];

// Toute permission module prefix marqué comme réservé côté platform.
const PLATFORM_MODULE_PREFIXES = ['organization.', 'subscription.'];

const ICONS = {
  Dashboard,
  People,
  Class,
  HowToReg,
  CalendarMonth,
  Layers,
  FamilyRestroom,
  AccountTree,
  MenuBook,
  AssignmentInd,
  Quiz,
  Grade,
  FactCheck,
  Description,
  Payments,
  Payment,
  Receipt,
  ManageAccounts,
  AdminPanelSettings,
  School,
};

function Sidebar({ permissions = [], scope = null, onNavigate }) {
  const isPlatform = scope === 'PLATFORM';

  const isPlatformOnly = (permission) => {
    if (PLATFORM_PERMISSIONS.includes(permission)) return true;

    return PLATFORM_MODULE_PREFIXES.some((prefix) =>
      permission.startsWith(prefix)
    );
  };

  const navigation = navigationData.navigation.filter((item) => {
    // Uniquement les entrées dont on a la permission.
    if (!permissions.includes(item.permission)) return false;

    // Les entrées réservées au platform ne s'affichent que pour un admin platform.
    if (isPlatformOnly(item.permission)) return isPlatform;

    return true;
  });

  return (
    <Box
      component="aside"
      sx={{
        width: 260,
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        borderRight: 1,
        borderColor: 'divider',
        bgcolor: 'background.paper',
      }}
    >
      {/* Logo */}
      <Box
        sx={{
          height: 72,
          display: 'flex',
          alignItems: 'center',
          px: 3,
        }}
      >
        <School
          sx={{
            mr: 1.5,
            color: 'primary.main',
            fontSize: 30,
          }}
        />

        <Typography variant="h6" fontWeight={700} color="text.primary">
          Foulam Gestion
        </Typography>
      </Box>

      <Divider />

      {/* Navigation */}
      <List
        sx={{
          px: 1.5,
          py: 2,
          overflowY: 'auto',
          flex: 1,
        }}
      >
        {navigation.map((item) => {
          const Icon = ICONS[item.icon];

          return (
            <ListItemButton
              key={item.path}
              component={NavLink}
              to={item.path}
              onClick={onNavigate}
              sx={{
                mb: 0.5,
                borderRadius: 1.5,
                color: 'text.secondary',

                '& .MuiListItemIcon-root': {
                  color: 'inherit',
                  minWidth: 40,
                },

                '&.active': {
                  bgcolor: 'primary.main',
                  color: 'primary.contrastText',

                  '&:hover': {
                    bgcolor: 'primary.dark',
                  },
                },

                '&:hover': {
                  bgcolor: 'action.hover',
                },
              }}
            >
              <ListItemIcon>{Icon && <Icon />}</ListItemIcon>

              <ListItemText
                primary={item.label}
                primaryTypographyProps={{
                  fontSize: 14,
                  fontWeight: 500,
                }}
              />
            </ListItemButton>
          );
        })}
      </List>
    </Box>
  );
}

export default Sidebar;
