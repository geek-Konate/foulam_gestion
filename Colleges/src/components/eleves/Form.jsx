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
 * Formulaire des élèves.
 * Gère l'ajout et l'édition selon la prop `editingEleve`.
 */
function Form({ open, editingEleve, saving, onClose, onSave }) {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [gender, setGender] = useState('M');
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) {
      setLocalError(null);

      if (editingEleve) {
        setFirstName(editingEleve.first_name || '');
        setLastName(editingEleve.last_name || '');
        setBirthDate(editingEleve.birth_date || '');
        setGender(editingEleve.gender || 'M');
      } else {
        setFirstName('');
        setLastName('');
        setBirthDate('');
        setGender('M');
      }
    }
  }, [open, editingEleve]);

  const handleSubmit = () => {
    if (!firstName.trim() || !lastName.trim()) {
      setLocalError("Le prénom et le nom sont obligatoires.");
      return;
    }

    if (!birthDate) {
      setLocalError("La date de naissance est obligatoire.");
      return;
    }

    onSave({
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      birth_date: birthDate,
      gender,
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      aria-labelledby="eleve-form-title"
    >
      <DialogTitle id="eleve-form-title">
        {editingEleve ? 'Modifier l’élève' : 'Ajouter un élève'}
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
            label="Prénom"
            value={firstName}
            onChange={(event) => setFirstName(event.target.value)}
            fullWidth
            required
          />

          <TextField
            label="Nom"
            value={lastName}
            onChange={(event) => setLastName(event.target.value)}
            fullWidth
            required
          />

          <TextField
            label="Date de naissance"
            type="date"
            value={birthDate}
            onChange={(event) => setBirthDate(event.target.value)}
            fullWidth
            required
            InputLabelProps={{ shrink: true }}
          />

          <FormControl fullWidth>
            <InputLabel>Genre</InputLabel>
            <Select
              label="Genre"
              value={gender}
              onChange={(event) => setGender(event.target.value)}
            >
              <MenuItem value="M">Garçon</MenuItem>
              <MenuItem value="F">Fille</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </DialogContent>

      <DialogActions>
        <Button onClick={onClose} disabled={saving}>
          Annuler
        </Button>

        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? (
            <CircularProgress size={18} color="inherit" />
          ) : editingEleve ? (
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