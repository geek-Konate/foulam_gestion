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
 * Formulaire des niveaux.
 * Gère à la fois l'ajout et l'édition selon la prop `editingNiveau` :
 *  - editingNiveau null/undefined => mode ajout
 *  - editingNiveau fourni            => mode édition (pré-rempli)
 */
function Form({ open, editingNiveau, saving, onClose, onSave }) {
  const [name, setName] = useState('');
  const [category, setCategory] = useState('');
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) {
      setLocalError(null);

      if (editingNiveau) {
        setName(editingNiveau.name || '');
        setCategory(editingNiveau.category || '');
      } else {
        setName('');
        setCategory('');
      }
    }
  }, [open, editingNiveau]);

  const handleSubmit = () => {
    if (!name.trim()) {
      setLocalError('Le nom est obligatoire.');
      return;
    }

    onSave({
      name: name.trim(),
      category: category.trim(),
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      aria-labelledby="niveau-form-title"
    >
      <DialogTitle id="niveau-form-title">
        {editingNiveau ? 'Modifier le niveau' : 'Ajouter un niveau'}
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
            placeholder="Ex : CP, CM2, 6ème ..."
            fullWidth
            required
          />

          <TextField
            label="Catégorie"
            value={category}
            onChange={(event) => setCategory(event.target.value)}
            placeholder="Ex : primaire, collège, lycée ..."
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
          ) : editingNiveau ? (
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