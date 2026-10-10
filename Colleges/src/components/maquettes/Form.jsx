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

function Form({ open, editingMaquette, annees = [], niveaux = [], saving, onClose, onSave }) {
  const [name, setName] = useState('');
  const [academicYearId, setAcademicYearId] = useState('');
  const [levelId, setLevelId] = useState('');
  const [status, setStatus] = useState('active');
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) {
      setLocalError(null);
      if (editingMaquette) {
        setName(editingMaquette.name || '');
        setAcademicYearId(editingMaquette.academic_year_id || '');
        setLevelId(editingMaquette.level_id || '');
        setStatus(editingMaquette.status || 'active');
      } else {
        setName('');
        setAcademicYearId('');
        setLevelId('');
        setStatus('active');
      }
    }
  }, [open, editingMaquette]);

  const handleSubmit = () => {
    if (!name.trim()) {
      setLocalError('Le nom est obligatoire.');
      return;
    }
    if (!academicYearId) {
      setLocalError("Veuillez choisir une année scolaire.");
      return;
    }
    if (!levelId) {
      setLocalError("Veuillez choisir un niveau.");
      return;
    }

    onSave({
      name: name.trim(),
      academic_year_id: academicYearId,
      level_id: levelId,
      status,
    });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm" aria-labelledby="maquette-form-title">
      <DialogTitle id="maquette-form-title">
        {editingMaquette ? 'Modifier la maquette' : 'Ajouter une maquette'}
      </DialogTitle>

      <DialogContent>
        {localError && <Alert severity="error" sx={{ mb: 2 }}>{localError}</Alert>}

        <Box
          component="form"
          noValidate
          onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}
        >
          <TextField label="Nom" value={name} onChange={(e) => setName(e.target.value)}
            placeholder="Ex : Programme CM2 - 2027" fullWidth required />

          <FormControl fullWidth>
            <InputLabel>Année scolaire</InputLabel>
            <Select label="Année scolaire" value={academicYearId}
              onChange={(e) => setAcademicYearId(e.target.value)}>
              {annees.map((a) => <MenuItem key={a.id} value={a.id}>{a.name}</MenuItem>)}
            </Select>
          </FormControl>

          <FormControl fullWidth>
            <InputLabel>Niveau</InputLabel>
            <Select label="Niveau" value={levelId}
              onChange={(e) => setLevelId(e.target.value)}>
              {niveaux.map((n) => <MenuItem key={n.id} value={n.id}>{n.name}</MenuItem>)}
            </Select>
          </FormControl>

          <FormControl fullWidth>
            <InputLabel>Statut</InputLabel>
            <Select label="Statut" value={status}
              onChange={(e) => setStatus(e.target.value)}>
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="inactive">Inactive</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} disabled={saving}>Annuler</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? <CircularProgress size={18} color="inherit" /> : editingMaquette ? 'Enregistrer' : 'Ajouter'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;