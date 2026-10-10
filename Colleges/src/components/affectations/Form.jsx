import { useEffect, useState } from 'react';

import {
  Alert, Box, Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle,
  FormControl, InputLabel, MenuItem, Select,
} from '@mui/material';

function Form({ open, curriculumSubjects = [], matieres = [], users = [], savings, onClose, onSave }) {
  const [csId, setCsId] = useState('');
  const [userId, setUserId] = useState('');
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) { setLocalError(null); setCsId(''); setUserId(''); }
  }, [open]);

  const handleSubmit = () => {
    if (!csId) { setLocalError("Veuillez choisir une matière."); return; }
    if (!userId) { setLocalError("Veuillez choisir un enseignant."); return; }
    onSave(csId, userId);
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm" aria-labelledby="aff-form-title">
      <DialogTitle id="aff-form-title">Affecter un enseignant</DialogTitle>
      <DialogContent>
        {localError && <Alert severity="error" sx={{ mb: 2 }}>{localError}</Alert>}
        <Box component="form" noValidate
          onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          
          <FormControl fullWidth>
            <InputLabel>Matière</InputLabel>
            <Select label="Matière" value={csId} onChange={(e) => setCsId(e.target.value)}>
              {curriculumSubjects.map((cs) => {
                const mat = matieres.find((m) => m.id === cs.subject_id);
                return <MenuItem key={cs.id} value={cs.id}>{mat ? mat.name : '—'}</MenuItem>;
              })}
            </Select>
          </FormControl>

          <FormControl fullWidth>
            <InputLabel>Enseignant</InputLabel>
            <Select label="Enseignant" value={userId} onChange={(e) => setUserId(e.target.value)}>
              {users.map((u) => (
                <MenuItem key={u.id} value={u.id}>{u.last_name} {u.first_name}</MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={savings}>Annuler</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={savings}>
          {savings ? <CircularProgress size={18} color="inherit" /> : 'Affecter'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;