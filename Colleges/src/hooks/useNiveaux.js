import { useCallback, useEffect, useState } from 'react';

import { LevelsAPI } from '../services/api';

/**
 * Hook dédié aux niveaux (CP, CM2, 6ème...).
 * Centralise les appels HTTP via services/api.js (LevelsAPI).
 */
export function useNiveaux() {
  const [niveaux, setNiveaux] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadNiveaux = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await LevelsAPI.getAll();

      setNiveaux(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les niveaux.'
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadNiveaux();
  }, [loadNiveaux]);

  const createNiveau = useCallback(
    async (data) => {
      try {
        setSaving(true);
        setError(null);

        const response = await LevelsAPI.create(data);

        await loadNiveaux();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter le niveau.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [loadNiveaux]
  );

  const updateNiveau = useCallback(
    async (niveauId, data) => {
      try {
        setSaving(true);
        setError(null);

        const response = await LevelsAPI.update(niveauId, data);

        await loadNiveaux();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier le niveau.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [loadNiveaux]
  );

  const removeNiveau = useCallback(
    async (niveauId) => {
      try {
        setError(null);

        await LevelsAPI.remove(niveauId);

        await loadNiveaux();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer le niveau.'
        );
        throw err;
      }
    },
    [loadNiveaux]
  );

  return {
    niveaux,
    loading,
    error,
    saving,
    refresh: loadNiveaux,
    createNiveau,
    updateNiveau,
    removeNiveau,
  };
}