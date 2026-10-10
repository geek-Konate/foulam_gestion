import { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import { AuthAPI } from '../services/api';

export const AuthContext = createContext(null);

function decodeTokenPayload(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), '=');
    return JSON.parse(decodeURIComponent(escape(atob(padded))));
  } catch {
    return {};
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [permissions, setPermissions] = useState([]);
  const [scope, setScope] = useState(null);
  const [establishments, setEstablishments] = useState([]);
  const [activeEstablishmentId, setActiveEstablishmentId] = useState(null);
  const [loading, setLoading] = useState(true);

  const applyContext = useCallback((data) => {
    setUser(data);
    setPermissions(data.permissions || []);
    setScope(data.scope || null);
    setEstablishments(data.establishments || []);
  }, []);

  // Détermine l'établissement actif : priorité au contexte du token (JWT enrichi),
  // sinon le premier établissement accessible.
  const resolveActiveEstablishment = useCallback(
    (data, estList) => {
      const token = localStorage.getItem('token');
      const payload = token ? decodeTokenPayload(token) : {};
      const tokenEst = payload.establishment_id || null;

      if (tokenEst) {
        setActiveEstablishmentId(tokenEst);
        return;
      }

      const first = (estList || data?.establishments || [])[0];
      setActiveEstablishmentId(first?.id || null);
    },
    []
  );

  const loadCurrentUser = useCallback(async () => {
    const token = localStorage.getItem('token');

    if (!token) {
      setUser(null);
      setPermissions([]);
      setScope(null);
      setEstablishments([]);
      setActiveEstablishmentId(null);
      setLoading(false);
      return;
    }

    try {
      const response = await AuthAPI.me();
      const data = response.data;

      applyContext(data);
      resolveActiveEstablishment(data, null);
    } catch (error) {
      localStorage.removeItem('token');
      setUser(null);
      setPermissions([]);
      setScope(null);
      setEstablishments([]);
      setActiveEstablishmentId(null);
    } finally {
      setLoading(false);
    }
  }, [applyContext, resolveActiveEstablishment]);

  useEffect(() => {
    loadCurrentUser();
  }, [loadCurrentUser]);

  const login = async (email, password) => {
    const response = await AuthAPI.login({ email, password });
    const { access_token } = response.data;

    localStorage.setItem('token', access_token);

    await loadCurrentUser();
  };

  const selectEstablishment = useCallback(
    async (establishmentId) => {
      const response = await AuthAPI.selectEstablishment(establishmentId);

      const { access_token } = response.data;

      // Le nouveau token porte org_id + establishment_id (contexte enrichi).
      localStorage.setItem('token', access_token);

      setActiveEstablishmentId(establishmentId);

      // Recharge le user pour resynchroniser scope/permissions si besoin.
      await loadCurrentUser();

      return response.data;
    },
    [loadCurrentUser]
  );

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setPermissions([]);
    setScope(null);
    setEstablishments([]);
    setActiveEstablishmentId(null);
  };

  const isPlatform = scope === 'PLATFORM';

  const hasPermission = (permission) => permissions.includes(permission);

  const activeEstablishment = useMemo(() => {
    if (!activeEstablishmentId) return null;
    return (
      establishments.find((est) => est.id === activeEstablishmentId) || null
    );
  }, [establishments, activeEstablishmentId]);

  const value = useMemo(
    () => ({
      user,
      permissions,
      scope,
      isPlatform,
      loading,
      establishments,
      activeEstablishmentId,
      activeEstablishment,
      login,
      logout,
      hasPermission,
      selectEstablishment,
    }),
    [
      user,
      permissions,
      scope,
      isPlatform,
      loading,
      establishments,
      activeEstablishmentId,
      activeEstablishment,
      login,
      logout,
      hasPermission,
      selectEstablishment,
    ]
  );

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}