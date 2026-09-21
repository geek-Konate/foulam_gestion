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

function Sidebar({ permissions = [], onNavigate }) {
  const navigation = navigationData.navigation.filter((item) =>
    permissions.includes(item.permission)
  );

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
