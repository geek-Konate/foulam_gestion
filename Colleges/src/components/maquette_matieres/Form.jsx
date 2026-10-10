import { useEffect, useState } from 'react';

import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  TextField,
} from '@mui/material';

function Form({ open, links = [], matieres = [], saving, onClose, onSave }) {
  const [subjectId, setSubjectId] = useState('');
  const [coefficient, setCoefficient] = useState(1);
  const [weeklyHours, setWeeklyHours] = useState(1);
  const [localError, setLocalError] = useState(null);

  const available = matieres.filter((m) => !links.some((l) => l.subject_id === m.id));

  useEffect(() => {
    if (open) {
      setLocalError(null);
      setSubjectId('');
      setCoefficient(1);
      setWeeklyHours(1);
    }
  }, [open]);

  const handleSubmit = () => {
    if (!subjectId) {
      setLocalError("Veuillez choisir une matière.");
      return;
    }
    onSave(subjectId, {
      coefficient: Number(coefficient) || 1,
      weekly_hours: Number(weeklyHours) || 1,
    });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm" aria-labelledby="cm-form-title">
      <DialogTitle id="cm-form-title">Ajouter une matière à la maquette</DialogTitle>

      <DialogContent>
        {localError && <Alert severity="error" sx={{ mb: 2 }}>{localError}</Alert>}
        {available.length === 0 && (
          <Alert severity="warning" sx={{ mb: 2 }}>Toutes les matières sont déjà dans cette maquette.</Alert>
        )}

        <Box component="form" noValidate
          onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          
          <FormControl fullWidth>
            <InputLabel>Matière</InputLabel>
            <Select label="Matière" value={subjectId} onChange={(e) => setSubjectId(e.target.value)}>
              {available.map((m) => <MenuItem key={m.id} value={m.id}>{m.name} ({m.code})</MenuItem>)}
            </Select>
          </FormControl>

          <TextField label="Coefficient" type="number" value={coefficient}
            onChange={(e) => setCoefficient(e.target.value)} inputProps={{ min: 1 }} fullWidth />

          <TextField label="Heures hebdomadaires" type="number" value={weeklyHours}
            onChange={(e) => setWeeklyHours(e.target.value)} inputProps={{ min: 1 }} fullWidth />
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} disabled={saving}>Annuler</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={saving || available.length === 0}>
          {saving ? <CircularProgress size={18} color="inherit" /> : 'Ajouter'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;