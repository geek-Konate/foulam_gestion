import { useEffect, useState } from 'react';

import {
  Alert, Box, Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle,
  FormControl, InputLabel, MenuItem, Select, TextField,
} from '@mui/material';

/**
 * Formulaire des évaluations (ajout uniquement, pas d'édition).
 */
function Form({ open, classes = [], matieres = [], saving, onClose, onSave }) {
  const [classId, setClassId] = useState('');
  const [subjectId, setSubjectId] = useState('');
  const [name, setName] = useState('');
  const [period, setPeriod] = useState('trimestre 1');
  const [date, setDate] = useState('');
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) {
      setLocalError(null);
      setClassId('');
      setSubjectId('');
      setName('');
      setPeriod('trimestre 1');
      setDate('');
    }
  }, [open]);

  const handleSubmit = () => {
    if (!classId) { setLocalError("Veuillez choisir une classe."); return; }
    if (!subjectId) { setLocalError("Veuillez choisir une matière."); return; }
    if (!name.trim()) { setLocalError("Le nom est obligatoire."); return; }
    if (!date) { setLocalError("La date est obligatoire."); return; }
    onSave({ class_id: classId, subject_id: subjectId, name: name.trim(), period, date });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Ajouter une évaluation</DialogTitle>
      <DialogContent>
        {localError && <Alert severity="error" sx={{ mb: 2 }}>{localError}</Alert>}
        <Box component="form" noValidate onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <FormControl fullWidth>
            <InputLabel>Classe</InputLabel>
            <Select label="Classe" value={classId} onChange={(e) => setClassId(e.target.value)}>
              {classes.map((c) => <MenuItem key={c.id} value={c.id}>{c.name}</MenuItem>)}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Matière</InputLabel>
            <Select label="Matière" value={subjectId} onChange={(e) => setSubjectId(e.target.value)}>
              {matieres.map((m) => <MenuItem key={m.id} value={m.id}>{m.name}</MenuItem>)}
            </Select>
          </FormControl>
          <TextField label="Nom" value={name} onChange={(e) => setName(e.target.value)} placeholder="Ex : DS n°1" fullWidth required />
          <TextField label="Date" type="date" value={date} onChange={(e) => setDate(e.target.value)} fullWidth required InputLabelProps={{ shrink: true }} />
          <FormControl fullWidth>
            <InputLabel>Période</InputLabel>
            <Select label="Période" value={period} onChange={(e) => setPeriod(e.target.value)}>
              <MenuItem value="trimestre 1">Trimestre 1</MenuItem>
              <MenuItem value="trimestre 2">Trimestre 2</MenuItem>
              <MenuItem value="trimestre 3">Trimestre 3</MenuItem>
              <MenuItem value="semestre 1">Semestre 1</MenuItem>
              <MenuItem value="semestre 2">Semestre 2</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={saving}>Annuler</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? <CircularProgress size={18} color="inherit" /> : 'Ajouter'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;