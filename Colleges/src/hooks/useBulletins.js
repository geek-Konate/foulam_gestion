import { useCallback, useEffect, useState } from 'react';
import { ReportCardsAPI } from '../services/api';

export function useBulletins(establishmentId, studentId) {
  const [bulletins, setBulletins] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const loadBulletins = useCallback(async () => {
    if (!establishmentId || !studentId) { setBulletins([]); return; }
    try {
      setLoading(true); setError(null);
      const res = await ReportCardsAPI.getByStudent(establishmentId, studentId);
      setBulletins(res.data || []);
    } catch (err) { setError(err.response?.data?.detail || 'Impossible de charger les bulletins.'); }
    finally { setLoading(false); }
  }, [establishmentId, studentId]);

  useEffect(() => { loadBulletins(); }, [loadBulletins]);

  const generateBulletin = useCallback(async (data) => {
    if (!establishmentId) return null;
    try {
      setSaving(true); setError(null);
      const res = await ReportCardsAPI.create(establishmentId, data);
      await loadBulletins();
      return res.data;
    } catch (err) { setError(err.response?.data?.detail || 'Impossible de générer le bulletin.'); throw err; }
    finally { setSaving(false); }
  }, [establishmentId, loadBulletins]);

  return { bulletins, loading, error, saving, refresh: loadBulletins, generateBulletin };
}