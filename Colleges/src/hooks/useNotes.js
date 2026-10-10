import { useCallback, useEffect, useState } from 'react';

import { EvaluationsAPI, GradesAPI } from '../services/api';

/**
 * Hook dédié aux notes.
 * Centralise les appels HTTP via services/api.js (GradesAPI).
 *
 * @param {string} establishmentId Établissement actif
 * @param {string} evaluationId    Évaluation sélectionnée
 */
export function useNotes(establishmentId, evaluationId) {
  const [notes, setNotes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadNotes = useCallback(async () => {
    if (!establishmentId || !evaluationId) {
      setNotes([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Récupérer les notes de l'évaluation
      const response = await GradesAPI.getByEvaluation(
        establishmentId,
        evaluationId
      );

      setNotes(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les notes.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId, evaluationId]);

  useEffect(() => {
    loadNotes();
  }, [loadNotes]);

  const createNote = useCallback(
    async (data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await GradesAPI.create(establishmentId, data);

        await loadNotes();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter la note.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadNotes]
  );

  const updateNote = useCallback(
    async (noteId, data) => {
      if (!establishmentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await GradesAPI.update(
          establishmentId,
          noteId,
          data
        );

        await loadNotes();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de modifier la note.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, loadNotes]
  );

  const removeNote = useCallback(
    async (noteId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await GradesAPI.remove(establishmentId, noteId);

        await loadNotes();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de supprimer la note.'
        );
        throw err;
      }
    },
    [establishmentId, loadNotes]
  );

  return {
    notes,
    loading,
    error,
    saving,
    refresh: loadNotes,
    createNote,
    updateNote,
    removeNote,
  };
}