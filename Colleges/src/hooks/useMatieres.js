import { useCallback, useEffect, useState } from 'react';

import { SubjectsAPI } from '../services/api';

/**
 * Hook dédié aux matières.
 * Centralise les appels HTTP via services/api.js (SubjectsAPI).
 * Les matières sont globales (pas rattachées à un établissement).
 */
export function useMatieres() {
  const [matieres, setMatieres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadMatieres = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await SubjectsAPI.getAll();

      setMatieres(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les matières.'
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadMatieres();
  }, [loadMatieres]);

  const createMatiere = useCallback(
    async (data) => {
      try {
        setSaving(true);
        setError(null);

        const response = await SubjectsAPI.create(data);

        await loadMatieres();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter la matière.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [loadMatieres]
  );

  const updateMatiere = useCallback(
    async (matiereId, data) => {
      try {
        setSaving(true);
        setError(null);

        const response = await SubjectsAPI.update(matiereId, data);

        await loadMatieres();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier la matière.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [loadMatieres]
  );

  const removeMatiere = useCallback(
    async (matiereId) => {
      try {
        setError(null);

        await SubjectsAPI.remove(matiereId);

        await loadMatieres();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer la matière.'
        );
        throw err;
      }
    },
    [loadMatieres]
  );

  return {
    matieres,
    loading,
    error,
    saving,
    refresh: loadMatieres,
    createMatiere,
    updateMatiere,
    removeMatiere,
  };
}