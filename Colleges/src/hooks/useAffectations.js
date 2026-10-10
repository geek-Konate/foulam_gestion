import { useCallback, useEffect, useState } from 'react';

import { TeacherAssignmentsAPI } from '../services/api';

/**
 * Hook dédié aux affectations d'enseignants.
 *
 * @param {string} establishmentId Établissement actif
 * @param {string} classId         Classe sélectionnée (optionnelle, pour lister par classe)
 */
export function useAffectations(establishmentId, classId) {
  const [affectations, setAffectations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadAffectations = useCallback(async () => {
    if (!establishmentId || !classId) {
      setAffectations([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await TeacherAssignmentsAPI.listClassAssignments(
        establishmentId,
        classId
      );

      setAffectations(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les affectations.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId, classId]);

  useEffect(() => {
    loadAffectations();
  }, [loadAffectations]);

  const assignTeacher = useCallback(
    async (curriculumSubjectId, userId) => {
      if (!establishmentId || !classId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await TeacherAssignmentsAPI.assignTeacher(
          establishmentId,
          classId,
          curriculumSubjectId,
          userId
        );

        await loadAffectations();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’affecter l’enseignant.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, classId, loadAffectations]
  );

  const removeAffectation = useCallback(
    async (assignmentId) => {
      if (!establishmentId) return;

      try {
        setError(null);

        await TeacherAssignmentsAPI.remove(establishmentId, assignmentId);

        await loadAffectations();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de retirer l’affectation.'
        );
        throw err;
      }
    },
    [establishmentId, loadAffectations]
  );

  return {
    affectations,
    loading,
    error,
    saving,
    refresh: loadAffectations,
    assignTeacher,
    removeAffectation,
  };
}