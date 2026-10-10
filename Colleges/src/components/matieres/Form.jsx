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
  TextField,
} from '@mui/material';

/**
 * Formulaire des matières.
 * Gère l'ajout et l'édition selon la prop `editingMatiere`.
 */
function Form({ open, editingMatiere, saving, onClose, onSave }) {
  const [name, setName] = useState('');
  const [code, setCode] = useState('');
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) {
      setLocalError(null);

      if (editingMatiere) {
        setName(editingMatiere.name || '');
        setCode(editingMatiere.code || '');
      } else {
        setName('');
        setCode('');
      }
    }
  }, [open, editingMatiere]);

  const handleSubmit = () => {
    if (!name.trim()) {
      setLocalError('Le nom est obligatoire.');
      return;
    }

    if (!code.trim()) {
      setLocalError('Le code est obligatoire.');
      return;
    }

    onSave({
      name: name.trim(),
      code: code.trim(),
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      aria-labelledby="matiere-form-title"
    >
      <DialogTitle id="matiere-form-title">
        {editingMatiere ? 'Modifier la matière' : 'Ajouter une matière'}
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
            placeholder="Ex : Mathématiques"
            fullWidth
            required
          />

          <TextField
            label="Code"
            value={code}
            onChange={(event) => setCode(event.target.value)}
            placeholder="Ex : MATH"
            fullWidth
            required
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
          ) : editingMatiere ? (
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