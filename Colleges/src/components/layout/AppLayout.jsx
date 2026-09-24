import { Box } from '@mui/material';
import { useState } from 'react';
import { Outlet } from 'react-router-dom';

import { useAuth } from '../../hooks/useAuth';
import Header from './Header';
import Sidebar from './Sidebar';

function AppLayout() {
  const { permissions, scope } = useAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const handleMenuClick = () => {
    setSidebarOpen((prev) => !prev);
  };

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

      {/* Sidebar fixe */}
      {sidebarOpen && (
        <Box
          sx={{
            position: 'fixed',
            top: '72px',
            left: 0,
            bottom: 0,
            width: 260,
            zIndex: (theme) => theme.zIndex.drawer,
          }}
        >
          <Sidebar permissions={permissions} scope={scope} />
        </Box>
      )}

      {/* Contenu scrollable */}
      <Box
        component="main"
        sx={{
          position: 'absolute',
          top: '72px',
          right: 0,
          bottom: 0,
          left: sidebarOpen ? '260px' : 0,
          overflowY: 'auto',
          transition: 'left 0.2s ease',
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
