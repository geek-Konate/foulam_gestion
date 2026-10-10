import { useEffect, useState } from 'react';

import {
  Alert, Box, Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle,
  FormControl, InputLabel, MenuItem, Select, TextField,
} from '@mui/material';

function Form({ open, eleves = [], notes = [], saving, onClose, onSave }) {
  const [studentId, setStudentId] = useState('');
  const [value, setValue] = useState('');
  const [comment, setComment] = useState('');
  const [localError, setLocalError] = useState(null);

  // Élèves pas encore notés
  const available = eleves.filter((e) => !notes.some((n) => n.student_id === e.id));

  useEffect(() => {
    if (open) { setLocalError(null); setStudentId(''); setValue(''); setComment(''); }
  }, [open]);

  const handleSubmit = () => {
    if (!studentId) { setLocalError("Veuillez choisir un élève."); return; }
    if (value === '' || Number(value) < 0 || Number(value) > 20) {
      setLocalError("La note doit être entre 0 et 20."); return;
    }
    onSave({
      student_id: studentId,
      value: Number(value),
      comment: comment.trim() || null,
    });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Ajouter une note</DialogTitle>
      <DialogContent>
        {localError && <Alert severity="error" sx={{ mb: 2 }}>{localError}</Alert>}
        {available.length === 0 && (
          <Alert severity="warning" sx={{ mb: 2 }}>Tous les élèves de la classe ont déjà une note.</Alert>
        )}
        <Box component="form" noValidate onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <FormControl fullWidth>
            <InputLabel>Élève</InputLabel>
            <Select label="Élève" value={studentId} onChange={(e) => setStudentId(e.target.value)}>
              {available.map((el) => (
                <MenuItem key={el.id} value={el.id}>{el.last_name} {el.first_name}</MenuItem>
              ))}
            </Select>
          </FormControl>
          <TextField label="Note /20" type="number" value={value}
            onChange={(e) => setValue(e.target.value)} inputProps={{ min: 0, max: 20, step: 0.25 }} fullWidth required />
          <TextField label="Commentaire" value={comment} onChange={(e) => setComment(e.target.value)} fullWidth multiline rows={2} />
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