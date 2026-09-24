import { createContext, useEffect, useMemo, useState } from 'react';
import { AuthAPI } from '../services/api';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [permissions, setPermissions] = useState([]);
  const [scope, setScope] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadCurrentUser = async () => {
    const token = localStorage.getItem('token');

    if (!token) {
      setUser(null);
      setPermissions([]);
      setScope(null);
      setLoading(false);
      return;
    }

    try {
      const response = await AuthAPI.me();

      setUser(response.data);
      setPermissions(response.data.permissions || []);
      setScope(response.data.scope || null);
    } catch (error) {
      localStorage.removeItem('token');
      setUser(null);
      setPermissions([]);
      setScope(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCurrentUser();
  }, []);

  const login = async (email, password) => {
    const response = await AuthAPI.login({
      email,
      password,
    });

    const { access_token } = response.data;

    localStorage.setItem('token', access_token);

    await loadCurrentUser();
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setPermissions([]);
    setScope(null);
  };

  const isPlatform = scope === 'PLATFORM';

  const hasPermission = (permission) => {
    return permissions.includes(permission);
  };

  const value = useMemo(
    () => ({
      user,
      permissions,
      scope,
      isPlatform,
      loading,
      login,
      logout,
      hasPermission,
    }),
    [user, permissions, scope, isPlatform, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
