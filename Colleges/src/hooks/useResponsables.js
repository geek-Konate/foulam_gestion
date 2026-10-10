import { useCallback, useEffect, useState } from 'react';

import { GuardiansAPI } from '../services/api';

/**
 * Hook dédié aux responsables (guardians).
 * Centralise les appels HTTP via services/api.js (GuardiansAPI).
 *
 * @param {string} establishmentId Établissement actif
 */
export function useResponsables(establishmentId) {
  const [responsables, setResponsables] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadResponsables = useCallback(async () => {
    if (!establishmentId) {
      setResponsables([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await GuardiansAPI.getAll(establishmentId);

      setResponsables(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les responsables.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId]);

  useEffect(() => {
    loadResponsables();
  }, [loadResponsables]);

  const createResponsable = useCallback(
    async (data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await GuardiansAPI.create(
          establishmentId,
          data
        );

        await loadResponsables();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter le responsable.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadResponsables]
  );

  const updateResponsable = useCallback(
    async (responsableId, data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await GuardiansAPI.update(
          establishmentId,
          responsableId,
          data
        );

        await loadResponsables();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier le responsable.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadResponsables]
  );

  const removeResponsable = useCallback(
    async (responsableId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await GuardiansAPI.remove(establishmentId, responsableId);

        await loadResponsables();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer le responsable.'
        );
        throw err;
      }
    },
    [establishmentId, loadResponsables]
  );

  return {
    responsables,
    loading,
    error,
    saving,
    refresh: loadResponsables,
    createResponsable,
    updateResponsable,
    removeResponsable,
  };
}