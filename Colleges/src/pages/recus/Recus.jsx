import { useCallback, useEffect, useState } from 'react';
import { Refresh } from '@mui/icons-material';
import { Alert, Box, Button, FormControl, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';
import { useAuth } from '../../hooks/useAuth';
import { useEleves } from '../../hooks/useEleves';
import { PaymentsAPI, ReceiptsAPI } from '../../services/api';

function Recus() {
  const { activeEstablishmentId } = useAuth();
  const { eleves } = useEleves(activeEstablishmentId);

  const [studentId, setStudentId] = useState('');
  const [paiements, setPaiements] = useState([]);
  const [paymentId, setPaymentId] = useState('');
  const [reference, setReference] = useState('');
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [receipt, setReceipt] = useState(null);

  // Charger les paiements de l'élève sélectionné
  useEffect(() => {
    if (!activeEstablishmentId || !studentId) { setPaiements([]); return; }
    (async () => {
      try {
        const res = await PaymentsAPI.getByStudent(activeEstablishmentId, studentId);
        setPaiements(res.data || []);
      } catch { setPaiements([]); }
    })();
  }, [activeEstablishmentId, studentId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!paymentId || !reference.trim()) {
      setError('Choisissez un paiement et saisissez une référence.');
      return;
    }
    try {
      setSaving(true); setError(null);
      const res = await ReceiptsAPI.create(activeEstablishmentId, {
        payment_id: paymentId,
        reference: reference.trim(),
        generated_at: new Date().toISOString(),
      });
      setReceipt(res.data);
      setStudentId(''); setPaymentId(''); setReference(''); setPaiements([]);
    } catch (err) {
      const d = err.response?.data?.detail;
      setError(Array.isArray(d) && d.length ? d[0]?.msg : d || 'Erreur');
    } finally { setSaving(false); }
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}><Typography variant="h4" fontWeight={700} gutterBottom>Reçus</Typography></Box>
      {!activeEstablishmentId && <Alert severity="info">Aucun établissement sélectionné.</Alert>}
      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
      {receipt && <Alert severity="success" sx={{ mb: 3 }}>Reçu créé : {receipt.reference}</Alert>}

      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 500 }}>
        <FormControl fullWidth>
          <InputLabel>Élève</InputLabel>
          <Select label="Élève" value={studentId} onChange={(e) => { setStudentId(e.target.value); setPaymentId(''); }}>
            {eleves.map((el) => <MenuItem key={el.id} value={el.id}>{el.last_name} {el.first_name}</MenuItem>)}
          </Select>
        </FormControl>

        <FormControl fullWidth disabled={!studentId}>
          <InputLabel>Paiement</InputLabel>
          <Select label="Paiement" value={paymentId} onChange={(e) => setPaymentId(e.target.value)}>
            {paiements.map((p) => (
              <MenuItem key={p.id} value={p.id}>
                {new Date(p.payment_date).toLocaleDateString('fr-FR')} — {p.amount} FCFA
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField label="Référence" value={reference} onChange={(e) => setReference(e.target.value)} 
          placeholder="Ex : REC-2027-001" fullWidth required />
        
        <Button type="submit" variant="contained" disabled={saving || !paymentId}>
          {saving ? 'Création...' : 'Créer le reçu'}
        </Button>
      </Box>
    </Box>
  );
}

export default Recus;