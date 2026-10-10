import { useCallback, useEffect, useState } from 'react';

import { ClassesAPI } from '../services/api';

/**
 * Hook dédié aux classes.
 * Centralise les appels HTTP via services/api.js (ClassesAPI).
 *
 * @param {string} establishmentId Établissement actif
 */
export function useClasses(establishmentId) {
  const [classes, setClasses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadClasses = useCallback(async () => {
    if (!establishmentId) {
      setClasses([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await ClassesAPI.getAll(establishmentId);

      setClasses(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les classes.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId]);

  useEffect(() => {
    loadClasses();
  }, [loadClasses]);

  const createClasse = useCallback(
    async (data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await ClassesAPI.create(establishmentId, data);

        await loadClasses();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter la classe.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadClasses]
  );

  const updateClasse = useCallback(
    async (classeId, data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await ClassesAPI.update(
          establishmentId,
          classeId,
          data
        );

        await loadClasses();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier la classe.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadClasses]
  );

  const removeClasse = useCallback(
    async (classeId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await ClassesAPI.remove(establishmentId, classeId);

        await loadClasses();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer la classe.'
        );
        throw err;
      }
    },
    [establishmentId, loadClasses]
  );

  return {
    classes,
    loading,
    error,
    saving,
    refresh: loadClasses,
    createClasse,
    updateClasse,
    removeClasse,
  };
}