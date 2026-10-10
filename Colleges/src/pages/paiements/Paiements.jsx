import { useState } from 'react';
import { Add, Refresh } from '@mui/icons-material';
import { Alert, Box, Button, FormControl, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';
import { useAuth } from '../../hooks/useAuth';
import { useEleves } from '../../hooks/useEleves';
import { useFraisTypes } from '../../hooks/useFraisTypes';
import { PaymentsAPI } from '../../services/api';

function Paiements() {
  const { activeEstablishmentId, user } = useAuth();
  const { eleves } = useEleves(activeEstablishmentId);
  const { types: fraisTypes } = useFraisTypes(activeEstablishmentId);

  const [studentId, setStudentId] = useState('');
  const [feeTypeId, setFeeTypeId] = useState('');
  const [amount, setAmount] = useState('');
  const [paymentDate, setPaymentDate] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('especes');
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [done, setDone] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!studentId || !feeTypeId || !amount || !paymentDate) {
      setError('Tous les champs sont obligatoires.');
      return;
    }
    try {
      setSaving(true); setError(null);
      await PaymentsAPI.create(activeEstablishmentId, {
        student_id: studentId,
        fee_type_id: feeTypeId,
        amount: Number(amount),
        payment_date: paymentDate,
        payment_method: paymentMethod,
        created_by: user?.id || '',
      });
      setDone(true);
      setStudentId(''); setFeeTypeId(''); setAmount(''); setPaymentDate(''); setPaymentMethod('especes');
    } catch (err) {
      const d = err.response?.data?.detail;
      setError(Array.isArray(d) && d.length ? d[0]?.msg : d || 'Erreur');
    } finally { setSaving(false); }
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}><Typography variant="h4" fontWeight={700} gutterBottom>Paiements</Typography></Box>
      {!activeEstablishmentId && <Alert severity="info">Aucun établissement sélectionné.</Alert>}
      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
      {done && <Alert severity="success" sx={{ mb: 3 }}>Paiement enregistré !</Alert>}

      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2, maxWidth: 500 }}>
        <FormControl fullWidth>
          <InputLabel>Élève</InputLabel>
          <Select label="Élève" value={studentId} onChange={(e) => setStudentId(e.target.value)}>
            {eleves.map((el) => <MenuItem key={el.id} value={el.id}>{el.last_name} {el.first_name}</MenuItem>)}
          </Select>
        </FormControl>
        <FormControl fullWidth>
          <InputLabel>Type de frais</InputLabel>
          <Select label="Type de frais" value={feeTypeId} onChange={(e) => setFeeTypeId(e.target.value)}>
            {fraisTypes.map((ft) => <MenuItem key={ft.id} value={ft.id}>{ft.name} ({ft.amount} FCFA)</MenuItem>)}
          </Select>
        </FormControl>
        <TextField label="Montant" type="number" value={amount} onChange={(e) => setAmount(e.target.value)} fullWidth required />
        <TextField label="Date" type="date" value={paymentDate} onChange={(e) => setPaymentDate(e.target.value)} fullWidth required InputLabelProps={{ shrink: true }} />
        <FormControl fullWidth>
          <InputLabel>Méthode</InputLabel>
          <Select label="Méthode" value={paymentMethod} onChange={(e) => setPaymentMethod(e.target.value)}>
            <MenuItem value="especes">Espèces</MenuItem>
            <MenuItem value="virement">Virement</MenuItem>
            <MenuItem value="cheque">Chèque</MenuItem>
            <MenuItem value="mobile">Mobile money</MenuItem>
          </Select>
        </FormControl>
        <Button type="submit" variant="contained" disabled={saving}>
          {saving ? 'Enregistrement...' : 'Enregistrer le paiement'}
        </Button>
      </Box>
    </Box>
  );
}

export default Paiements;