import { useCallback, useEffect, useState } from 'react';

import { AttendanceAPI } from '../services/api';

export function usePresences(establishmentId, classId, date) {
  const [presences, setPresences] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadPresences = useCallback(async () => {
    if (!establishmentId || !classId || !date) { setPresences([]); return; }
    try {
      setLoading(true); setError(null);
      const res = await AttendanceAPI.getByClass(establishmentId, classId, date);
      setPresences(res.data || []);
    } catch (err) {
      setError(err.response?.data?.detail || 'Impossible de charger les présences.');
    } finally { setLoading(false); }
  }, [establishmentId, classId, date]);

  useEffect(() => { loadPresences(); }, [loadPresences]);

  const savePresence = useCallback(async (data) => {
    if (!establishmentId) return null;
    try {
      setSaving(true); setError(null);
      const res = await AttendanceAPI.create(establishmentId, data);
      await loadPresences();
      return res.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Impossible d\'enregistrer.');
      throw err;
    } finally { setSaving(false); }
  }, [establishmentId, loadPresences]);

  const updatePresence = useCallback(async (presenceId, data) => {
    if (!establishmentId) return null;
    try {
      setSaving(true); setError(null);
      const res = await AttendanceAPI.update(establishmentId, presenceId, data);
      await loadPresences();
      return res.data;
    } catch (err) {
      setError(err.response?.data?.detail || 'Impossible de modifier.');
      throw err;
    } finally { setSaving(false); }
  }, [establishmentId, loadPresences]);

  return { presences, loading, error, saving, refresh: loadPresences, savePresence, updatePresence };
}