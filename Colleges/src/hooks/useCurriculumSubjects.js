import { useCallback, useEffect, useState } from 'react';

import { CurriculumSubjectsAPI, CurriculumsAPI } from '../services/api';

/**
 * Hook dédié aux matières d'une maquette (CurriculumSubject).
 *
 * @param {string} establishmentId Établissement actif
 * @param {string} curriculumId    Maquette sélectionnée
 */
export function useCurriculumSubjects(establishmentId, curriculumId) {
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadLinks = useCallback(async () => {
    if (!establishmentId || !curriculumId) {
      setLinks([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await CurriculumSubjectsAPI.listCurriculumSubjects(
        establishmentId,
        curriculumId
      );

      setLinks(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les matières de la maquette.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId, curriculumId]);

  useEffect(() => {
    loadLinks();
  }, [loadLinks]);

  const addSubject = useCallback(
    async (subjectId, data) => {
      if (!establishmentId || !curriculumId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await CurriculumSubjectsAPI.addSubject(
          establishmentId,
          curriculumId,
          subjectId,
          data
        );

        await loadLinks();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’ajouter la matière à la maquette.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, curriculumId, loadLinks]
  );

  const removeSubject = useCallback(
    async (subjectId) => {
      if (!establishmentId || !curriculumId) return;

      try {
        setError(null);

        await CurriculumSubjectsAPI.removeSubject(
          establishmentId,
          curriculumId,
          subjectId
        );

        await loadLinks();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de retirer la matière de la maquette.'
        );
        throw err;
      }
    },
    [establishmentId, curriculumId, loadLinks]
  );

  return {
    links,
    loading,
    error,
    saving,
    refresh: loadLinks,
    addSubject,
    removeSubject,
  };
}