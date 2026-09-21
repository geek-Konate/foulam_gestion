import { useCallback, useEffect, useState } from 'react';
import { DashboardAPI } from '../services/api';
import { useAuth } from './useAuth';

export function useDashboard() {
  const { user } = useAuth();

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const loadDashboard = useCallback(async () => {
    if (!user?.establishment_id) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await DashboardAPI.getEstablishmentDashboard(user.establishment_id);

      setData(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Impossible de charger le tableau de bord.');
    } finally {
      setLoading(false);
    }
  }, [user?.establishment_id]);

  useEffect(() => {
    loadDashboard();
  }, [loadDashboard]);

  return {
    data,
    loading,
    error,
    refresh: loadDashboard,
  };
}
