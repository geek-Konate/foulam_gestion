import { useCallback, useEffect, useState } from 'react';

import { StudentGuardiansAPI } from '../services/api';

/**
 * Hook dédié à l'association Élève ↔ Responsables.
 * Centralise les appels HTTP via StudentGuardiansAPI.
 *
 * @param {string} establishmentId Établissement actif
 * @param {string} studentId       Élève sélectionné
 */
export function useStudentGuardians(establishmentId, studentId) {
  const [links, setLinks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadLinks = useCallback(async () => {
    if (!establishmentId || !studentId) {
      setLinks([]);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const response = await StudentGuardiansAPI.listGuardians(
        establishmentId,
        studentId
      );

      setLinks(response.data || []);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Impossible de charger les responsables de l’élève.'
      );
    } finally {
      setLoading(false);
    }
  }, [establishmentId, studentId]);

  useEffect(() => {
    loadLinks();
  }, [loadLinks]);

  const addLink = useCallback(
    async (data) => {
      if (!establishmentId || !studentId) return null;

      try {
        setSaving(true);
        setError(null);

        const response = await StudentGuardiansAPI.createLink(
          establishmentId,
          studentId,
          data
        );

        await loadLinks();

        return response.data;
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible d’associer le responsable.'
        );
        throw err;
      } finally {
        setSaving(false);
      }
    },
    [establishmentId, studentId, loadLinks]
  );

  const removeLink = useCallback(
    async (guardianId) => {
      if (!establishmentId || !studentId) return;

      try {
        setError(null);

        await StudentGuardiansAPI.deleteLink(
          establishmentId,
          studentId,
          guardianId
        );

        await loadLinks();
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Impossible de retirer le responsable.'
        );
        throw err;
      }
    },
    [establishmentId, studentId, loadLinks]
  );

  return {
    links,
    loading,
    error,
    saving,
    refresh: loadLinks,
    addLink,
    removeLink,
  };
}