import { useCallback, useEffect, useState } from 'react';
import { FeeTypesAPI } from '../services/api';

function extractError(err) {
  if (!err) return null;
  const detail = err.response?.data?.detail;
  if (Array.isArray(detail) && detail.length > 0) {
    return detail[0]?.msg || 'Erreur de validation';
  }
  return detail || 'Erreur inconnue';
}

export function useFraisTypes(establishmentId) {
  const [types, setTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    if (!establishmentId) { setTypes([]); setLoading(false); return; }
    try { setLoading(true); setError(null); const r = await FeeTypesAPI.getAll(establishmentId); setTypes(r.data || []); }
    catch (err) { setError(extractError(err)); }
    finally { setLoading(false); }
  }, [establishmentId]);

  useEffect(() => { load(); }, [load]);

  const create = useCallback(async (data) => {
    if (!establishmentId) return null;
    try { setSaving(true); setError(null); const r = await FeeTypesAPI.create(establishmentId, data); await load(); return r.data; }
    catch (err) { setError(extractError(err)); throw err; }
    finally { setSaving(false); }
  }, [establishmentId, load]);

  const update = useCallback(async (id, data) => {
    if (!establishmentId) return null;
    try { setSaving(true); setError(null); const r = await FeeTypesAPI.update(establishmentId, id, data); await load(); return r.data; }
    catch (err) { setError(extractError(err)); throw err; }
    finally { setSaving(false); }
  }, [establishmentId, load]);

  const remove = useCallback(async (id) => {
    if (!establishmentId) return;
    try { setError(null); await FeeTypesAPI.remove(establishmentId, id); await load(); }
    catch (err) { setError(extractError(err)); throw err; }
  }, [establishmentId, load]);

  return { types, loading, error, saving, refresh: load, create, update, remove };
}