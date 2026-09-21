import { createContext, useContext, useState } from 'react';

const LayoutContext = createContext(null);

export const LayoutProvider = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const openSidebar = () => {
    setSidebarOpen(true);
  };

  const closeSidebar = () => {
    setSidebarOpen(false);
  };

  const toggleSidebar = () => {
    setSidebarOpen((prev) => !prev);
  };

  return (
    <LayoutContext.Provider
      value={{
        sidebarOpen,
        openSidebar,
        closeSidebar,
        toggleSidebar,
      }}
    >
      {children}
    </LayoutContext.Provider>
  );
};

export const useLayoutContext = () => {
  const context = useContext(LayoutContext);

  if (!context) {
    throw new Error('useLayoutContext doit être utilisé à l’intérieur de LayoutProvider.');
  }

  return context;
};

export default LayoutContext;
