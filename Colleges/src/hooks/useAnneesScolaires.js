import { useCallback, useEffect, useState } from 'react';

import { AcademicYearsAPI } from '../services/api';

/**
 * Hook dédié aux années scolaires.
 * Centralise les appels HTTP via services/api.js (AcademicYearsAPI).
 *
 * @param {string} establishmentId Identifiant de l'établissement courant
 */
export function useAnneesScolaires(establishmentId) {
  const [annees, setAnnees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadAnnees = useCallback(async () => {
    if (!establishmentId) {
      setAnnees([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await AcademicYearsAPI.getAll(establishmentId);

      setAnnees(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les années scolaires.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId]);

  useEffect(() => {
    loadAnnees();
  }, [loadAnnees]);

  const createAnnee = useCallback(
    async (data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await AcademicYearsAPI.create(
          establishmentId,
          data
        );

        await loadAnnees();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter l’année scolaire.'
        );

        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadAnnees]
  );

  const updateAnnee = useCallback(
    async (anneeId, data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await AcademicYearsAPI.update(
          establishmentId,
          anneeId,
          data
        );

        await loadAnnees();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier l’année scolaire.'
        );

        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadAnnees]
  );

  const removeAnnee = useCallback(
    async (anneeId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await AcademicYearsAPI.remove(establishmentId, anneeId);

        await loadAnnees();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer l’année scolaire.'
        );

        throw err;
      }
    },
    [establishmentId, loadAnnees]
  );

  return {
    annees,
    loading,
    error,
    saving,
    refresh: loadAnnees,
    createAnnee,
    updateAnnee,
    removeAnnee,
  };
}