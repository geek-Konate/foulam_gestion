import { useEffect, useState } from 'react';
import { Alert, Box, Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle, TextField } from '@mui/material';

function Form({ open, editing, saving, onClose, onSave }) {
  const [name, setName] = useState('');
  const [amount, setAmount] = useState('');
  const [localError, setLocalError] = useState(null);
  useEffect(() => { if (open) { setLocalError(null); setName(editing?.name || ''); setAmount(editing?.amount || ''); } }, [open, editing]);
  const handleSubmit = () => {
    if (!name.trim()) { setLocalError('Le nom est obligatoire.'); return; }
    if (!amount) { setLocalError('Le montant est obligatoire.'); return; }
    onSave({ name: name.trim(), amount: Number(amount) });
  };
  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>{editing ? 'Modifier' : 'Ajouter'} un type de frais</DialogTitle>
      <DialogContent>
        {localError && <Alert severity="error" sx={{ mb: 2 }}>{localError}</Alert>}
        <Box component="form" noValidate onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <TextField label="Nom" value={name} onChange={(e) => setName(e.target.value)} placeholder="Ex : Scolarité" fullWidth required />
          <TextField label="Montant" type="number" value={amount} onChange={(e) => setAmount(e.target.value)} fullWidth required />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={saving}>Annuler</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? <CircularProgress size={18} color="inherit" /> : editing ? 'Enregistrer' : 'Ajouter'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;