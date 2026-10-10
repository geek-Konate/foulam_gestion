import { useCallback, useEffect, useState } from 'react';

import { EnrollmentsAPI } from '../services/api';

/**
 * Hook dédié aux inscriptions.
 * Centralise les appels HTTP via services/api.js (EnrollmentsAPI).
 *
 * @param {string} establishmentId Établissement actif
 */
export function useInscriptions(establishmentId) {
  const [inscriptions, setInscriptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadInscriptions = useCallback(async () => {
    if (!establishmentId) {
      setInscriptions([]);
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await EnrollmentsAPI.getAll(establishmentId);

      setInscriptions(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les inscriptions.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId]);

  useEffect(() => {
    loadInscriptions();
  }, [loadInscriptions]);

  const createInscription = useCallback(
    async (data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await EnrollmentsAPI.create(
          establishmentId,
          data
        );

        await loadInscriptions();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter l’inscription.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadInscriptions]
  );

  const updateInscription = useCallback(
    async (inscriptionId, data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await EnrollmentsAPI.update(
          establishmentId,
          inscriptionId,
          data
        );

        await loadInscriptions();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier l’inscription.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadInscriptions]
  );

  const removeInscription = useCallback(
    async (inscriptionId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await EnrollmentsAPI.remove(establishmentId, inscriptionId);

        await loadInscriptions();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer l’inscription.'
        );
        throw err;
      }
    },
    [establishmentId, loadInscriptions]
  );

  return {
    inscriptions,
    loading,
    error,
    saving,
    refresh: loadInscriptions,
    createInscription,
    updateInscription,
    removeInscription,
  };
}