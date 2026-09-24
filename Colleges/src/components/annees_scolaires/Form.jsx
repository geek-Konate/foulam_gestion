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

function toDateInputValue(value) {
  if (!value) return '';

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) return '';

  return date.toISOString().split('T')[0];
}

/**
 * Formulaire des années scolaires.
 * Gère à la fois l'ajout et l'édition selon la prop `editingAnnee` :
 *  - editingAnnee null/undefined => mode ajout
 *  - editingAnnee fourni            => mode édition (pré-rempli)
 */
function Form({ open, editingAnnee, saving, onClose, onSave }) {
  const [name, setName] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [status, setStatus] = useState('active');
  const [localError, setLocalError] = useState(null);

  // Pré-remplit le formulaire quand on ouvre le dialog (ajout ou édition)
  useEffect(() => {
    if (open) {
      setLocalError(null);

      if (editingAnnee) {
        setName(editingAnnee.name || '');
        setStartDate(toDateInputValue(editingAnnee.start_date));
        setEndDate(toDateInputValue(editingAnnee.end_date));
        setStatus(editingAnnee.status || 'active');
      } else {
        setName('');
        setStartDate('');
        setEndDate('');
        setStatus('active');
      }
    }
  }, [open, editingAnnee]);

  const handleSubmit = () => {
    if (!name.trim()) {
      setLocalError('Le nom est obligatoire.');
      return;
    }

    if (!startDate || !endDate) {
      setLocalError(
        'Les dates de début et de fin sont obligatoires.'
      );
      return;
    }

    if (endDate < startDate) {
      setLocalError('La date de fin doit être postérieure au début.');
      return;
    }

    onSave({
      name: name.trim(),
      start_date: startDate,
      end_date: endDate,
      status,
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      aria-labelledby="annee-form-title"
    >
      <DialogTitle id="annee-form-title">
        {editingAnnee ? 'Modifier l’année scolaire' : 'Ajouter une année scolaire'}
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
          sx={{
            display: 'flex',
            flexDirection: 'column',
            gap: 2,
            mt: 1,
          }}
        >
          <TextField
            label="Nom"
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Ex : 2026-2027"
            fullWidth
            required
          />

          <TextField
            label="Date de début"
            type="date"
            value={startDate}
            onChange={(event) => setStartDate(event.target.value)}
            fullWidth
            required
            InputLabelProps={{ shrink: true }}
          />

          <TextField
            label="Date de fin"
            type="date"
            value={endDate}
            onChange={(event) => setEndDate(event.target.value)}
            fullWidth
            required
            InputLabelProps={{ shrink: true }}
          />

          <FormControl fullWidth>
            <InputLabel>Statut</InputLabel>

            <Select
              label="Statut"
              value={status}
              onChange={(event) => setStatus(event.target.value)}
            >
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="inactive">Inactive</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} disabled={saving}>
          Annuler
        </Button>

        <Button
          variant="contained"
          onClick={handleSubmit}
          disabled={saving}
        >
          {saving ? (
            <CircularProgress size={18} color="inherit" />
          ) : editingAnnee ? (
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