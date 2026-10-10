import { useCallback, useEffect, useState } from 'react';

import { CurriculumsAPI } from '../services/api';

/**
 * Hook dédié aux maquettes (curriculums).
 * Centralise les appels HTTP via services/api.js (CurriculumsAPI).
 *
 * @param {string} establishmentId Établissement actif
 */
export function useMaquettes(establishmentId) {
  const [maquettes, setMaquettes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadMaquettes = useCallback(async () => {
    if (!establishmentId) {
      setMaquettes([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await CurriculumsAPI.getAll(establishmentId);

      setMaquettes(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les maquettes.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId]);

  useEffect(() => {
    loadMaquettes();
  }, [loadMaquettes]);

  const createMaquette = useCallback(
    async (data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await CurriculumsAPI.create(establishmentId, {
          ...data,
          establishment_id: establishmentId,
        });

        await loadMaquettes();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter la maquette.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadMaquettes]
  );

  const updateMaquette = useCallback(
    async (maquetteId, data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await CurriculumsAPI.update(
          establishmentId,
          maquetteId,
          data
        );

        await loadMaquettes();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier la maquette.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadMaquettes]
  );

  const removeMaquette = useCallback(
    async (maquetteId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await CurriculumsAPI.remove(establishmentId, maquetteId);

        await loadMaquettes();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer la maquette.'
        );
        throw err;
      }
    },
    [establishmentId, loadMaquettes]
  );

  return {
    maquettes,
    loading,
    error,
    saving,
    refresh: loadMaquettes,
    createMaquette,
    updateMaquette,
    removeMaquette,
  };
}