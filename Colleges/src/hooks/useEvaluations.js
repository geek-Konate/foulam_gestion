import { useCallback, useEffect, useState } from 'react';

import { EvaluationsAPI } from '../services/api';

/**
 * Hook dédié aux évaluations.
 * Centralise les appels HTTP via services/api.js (EvaluationsAPI).
 *
 * @param {string} establishmentId Établissement actif
 * @param {string} classId         Classe sélectionnée (optionnel)
 */
export function useEvaluations(establishmentId, classId) {
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadEvaluations = useCallback(async () => {
    if (!establishmentId || !classId) {
      setEvaluations([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await EvaluationsAPI.getByClass(establishmentId, classId);

      setEvaluations(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les évaluations.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId, classId]);

  useEffect(() => {
    loadEvaluations();
  }, [loadEvaluations]);

  const createEvaluation = useCallback(
    async (data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await EvaluationsAPI.create(establishmentId, data);

        await loadEvaluations();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter l’évaluation.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadEvaluations]
  );

  const removeEvaluation = useCallback(
    async (evaluationId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await EvaluationsAPI.remove(establishmentId, evaluationId);

        await loadEvaluations();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer l’évaluation.'
        );
        throw err;
      }
    },
    [establishmentId, loadEvaluations]
  );

  return {
    evaluations,
    loading,
    error,
    saving,
    refresh: loadEvaluations,
    createEvaluation,
    removeEvaluation,
  };
}