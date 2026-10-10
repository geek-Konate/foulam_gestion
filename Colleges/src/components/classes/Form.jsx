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

/**
 * Formulaire des classes.
 * Gère l'ajout et l'édition selon la prop `editingClasse`.
 */
function Form({ open, editingClasse, annees = [], niveaux = [], saving, onClose, onSave }) {
  const [name, setName] = useState('');
  const [academicYearId, setAcademicYearId] = useState('');
  const [levelId, setLevelId] = useState('');
  const [capacity, setCapacity] = useState(30);
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) {
      setLocalError(null);

      if (editingClasse) {
        setName(editingClasse.name || '');
        setAcademicYearId(editingClasse.academic_year_id || '');
        setLevelId(editingClasse.level_id || '');
        setCapacity(editingClasse.capacity ?? 30);
      } else {
        setName('');
        setAcademicYearId('');
        setLevelId('');
        setCapacity(30);
      }
    }
  }, [open, editingClasse]);

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
      capacity: Number(capacity) || 30,
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      aria-labelledby="classe-form-title"
    >
      <DialogTitle id="classe-form-title">
        {editingClasse ? 'Modifier la classe' : 'Ajouter une classe'}
      </DialogTitle>

      <DialogContent>
        {localError && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {localError}
          </Alert>
        )}

        <Box
          component="form"
          noValidate
          onSubmit={(event) => {
            event.preventDefault();
            handleSubmit();
          }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}
        >
          <TextField
            label="Nom"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Ex : CM2 A"
            fullWidth
            required
          />

          <FormControl fullWidth>
            <InputLabel>Année scolaire</InputLabel>
            <Select
              label="Année scolaire"
              value={academicYearId}
              onChange={(event) => setAcademicYearId(event.target.value)}
            >
              {annees.map((annee) => (
                <MenuItem key={annee.id} value={annee.id}>
                  {annee.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth>
            <InputLabel>Niveau</InputLabel>
            <Select
              label="Niveau"
              value={levelId}
              onChange={(event) => setLevelId(event.target.value)}
            >
              {niveaux.map((niveau) => (
                <MenuItem key={niveau.id} value={niveau.id}>
                  {niveau.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TextField
            label="Capacité"
            type="number"
            value={capacity}
            onChange={(event) => setCapacity(event.target.value)}
            inputProps={{ min: 1 }}
            fullWidth
          />
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} disabled={saving}>
          Annuler
        </Button>

        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? (
            <CircularProgress size={18} color="inherit" />
          ) : editingClasse ? (
            'Enregistrer'
          ) : (
            'Ajouter'
          )}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;