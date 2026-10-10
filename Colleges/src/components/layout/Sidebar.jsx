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
  Tooltip,
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

function Sidebar({ permissions = [], collapsed = false }) {
  const navigation = navigationData.navigation.filter((item) =>
    permissions.includes(item.permission)
  );

  return (
    <Box
      component="aside"
      sx={{
        width: '100%',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        borderRight: 1,
        borderColor: 'divider',
        bgcolor: 'background.paper',
        overflowX: 'hidden',
      }}
    >
      {/* Logo */}
      <Box
        sx={{
          height: 72,
          display: 'flex',
          alignItems: 'center',
          justifyContent: collapsed ? 'center' : 'flex-start',
          px: collapsed ? 0 : 3,
          flexShrink: 0,
        }}
      >
        <School
          sx={{
            mr: collapsed ? 0 : 1.5,
            color: 'primary.main',
            fontSize: 30,
          }}
        />

        {!collapsed && (
          <Typography variant="h6" fontWeight={700} color="text.primary">
            Foulam Gestion
          </Typography>
        )}
      </Box>

      <Divider />

      {/* Navigation */}
      <List
        sx={{
          px: collapsed ? 0.5 : 1.5,
          py: 2,
          flex: 1,
          overflowY: 'auto',
          overflowX: 'hidden',

          // Scrollbar fine adaptée au thème
          scrollbarWidth: 'thin',
          scrollbarColor: (theme) => `${theme.palette.action.selected} transparent`,
          '&::-webkit-scrollbar': {
            width: 6,
          },
          '&::-webkit-scrollbar-track': {
            backgroundColor: 'transparent',
          },
          '&::-webkit-scrollbar-thumb': {
            backgroundColor: (theme) => theme.palette.action.selected,
            borderRadius: 3,
            '&:hover': {
              backgroundColor: (theme) => theme.palette.action.focus,
            },
          },
        }}
      >
        {navigation.map((item) => {
          const Icon = ICONS[item.icon];

          const button = (
            <ListItemButton
              key={item.path}
              component={NavLink}
              to={item.path}
              sx={{
                mb: 0.5,
                borderRadius: 1.5,
                color: 'text.secondary',
                minHeight: 48,
                justifyContent: collapsed ? 'center' : 'flex-start',
                px: collapsed ? 1 : 2,

                '& .MuiListItemIcon-root': {
                  color: 'inherit',
                  minWidth: collapsed ? 0 : 40,
                  justifyContent: 'center',
                  mr: collapsed ? 0 : 1,
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

              {!collapsed && (
                <ListItemText
                  primary={item.label}
                  primaryTypographyProps={{
                    fontSize: 14,
                    fontWeight: 500,
                    noWrap: true,
                  }}
                />
              )}
            </ListItemButton>
          );

          return collapsed ? (
            <Tooltip key={item.path} title={item.label} placement="right" arrow>
              {button}
            </Tooltip>
          ) : (
            button
          );
        })}
      </List>
    </Box>
  );
}

export default Sidebar;
