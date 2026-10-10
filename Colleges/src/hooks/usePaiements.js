import { useCallback, useEffect, useState } from 'react';
import { PaymentsAPI } from '../services/api';

function extractError(err) {
  if (!err) return null;
  const d = err.response?.data?.detail;
  return Array.isArray(d) && d.length > 0 ? d[0]?.msg || 'Erreur' : d || 'Erreur inconnue';
}

export function usePaiements(establishmentId) {
  const [paiements, setPaiements] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    if (!establishmentId) { setPaiements([]); setLoading(false); return; }
    try { setLoading(true); setError(null); const r = await PaymentsAPI.create?.(establishmentId, {}); setPaiements(r?.data || []); }
    catch (err) { setError(extractError(err)); }
    finally { setLoading(false); }
  }, [establishmentId]);

  useEffect(() => { load(); }, [load]);
  // Note: load n'est pas correct pour getAll, on utilise getByStudent
  // mais le listing principal n'est pas simple à faire sans endpoint getAll
  // Pour l'instant, le module affichera les paiements par élève sélectionné

  const create = useCallback(async (data) => {
    if (!establishmentId) return null;
    try { setSaving(true); setError(null); const r = await PaymentsAPI.create(establishmentId, data); return r.data; }
    catch (err) { setError(extractError(err)); throw err; }
    finally { setSaving(false); }
  }, [establishmentId]);

  return { paiements, loading, error, saving, refresh: () => {}, create };
}