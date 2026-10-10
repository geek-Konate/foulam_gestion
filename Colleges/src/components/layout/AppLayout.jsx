import { Box } from '@mui/material';
import { useState } from 'react';
import { Outlet } from 'react-router-dom';

import { useAuth } from '../../hooks/useAuth';
import Header from './Header';
import Sidebar from './Sidebar';

function AppLayout() {
  const { permissions } = useAuth();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(true);

  const handleMenuClick = () => {
    setSidebarCollapsed((prev) => !prev);
  };

  const sidebarWidth = sidebarCollapsed ? 72 : 260;

  return (
    <Box
      sx={{
        height: '100vh',
        overflow: 'hidden',
        bgcolor: 'background.default',
      }}
    >
      {/* Header fixe */}
      <Header onMenuClick={handleMenuClick} />

      {/* Sidebar fixe (toujours visible) */}
      <Box
        sx={{
          position: 'fixed',
          top: '72px',
          left: 0,
          bottom: 0,
          width: sidebarWidth,
          zIndex: (theme) => theme.zIndex.drawer,
          transition: 'width 0.2s ease',
        }}
      >
        <Sidebar permissions={permissions} collapsed={sidebarCollapsed} />
      </Box>

      {/* Contenu scrollable */}
      <Box
        component="main"
        sx={{
          position: 'absolute',
          top: '72px',
          right: 0,
          bottom: 0,
          left: `${sidebarWidth}px`,
          overflowY: 'auto',
          transition: 'left 0.2s ease',
          // Scrollbar fine et adaptée au thème
          scrollbarWidth: 'thin',
          scrollbarColor: (theme) => `${theme.palette.action.selected} transparent`,
          '&::-webkit-scrollbar': {
            width: 6,
            height: 6,
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
        <Box sx={{ p: 3 }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
}

export default AppLayout;
