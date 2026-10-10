import { useCallback, useEffect, useState } from 'react';

import { StudentsAPI } from '../services/api';

/**
 * Hook dédié aux élèves.
 * Centralise les appels HTTP via services/api.js (StudentsAPI).
 *
 * @param {string} establishmentId Établissement actif
 */
export function useEleves(establishmentId) {
  const [eleves, setEleves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadEleves = useCallback(async () => {
    if (!establishmentId) {
      setEleves([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await StudentsAPI.getAll(establishmentId);

      setEleves(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les élèves.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId]);

  useEffect(() => {
    loadEleves();
  }, [loadEleves]);

  const createEleve = useCallback(
    async (data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await StudentsAPI.create(establishmentId, data);

        await loadEleves();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter l’élève.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadEleves]
  );

  const updateEleve = useCallback(
    async (eleveId, data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await StudentsAPI.update(
          establishmentId,
          eleveId,
          data
        );

        await loadEleves();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier l’élève.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadEleves]
  );

  const removeEleve = useCallback(
    async (eleveId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await StudentsAPI.remove(establishmentId, eleveId);

        await loadEleves();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer l’élève.'
        );
        throw err;
      }
    },
    [establishmentId, loadEleves]
  );

  return {
    eleves,
    loading,
    error,
    saving,
    refresh: loadEleves,
    createEleve,
    updateEleve,
    removeEleve,
  };
}