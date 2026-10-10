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
 * Formulaire des responsables.
 * Gère l'ajout et l'édition selon la prop `editingResponsable`.
 */
function Form({ open, editingResponsable, saving, onClose, onSave }) {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [address, setAddress] = useState('');
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) {
      setLocalError(null);

      if (editingResponsable) {
        setFirstName(editingResponsable.first_name || '');
        setLastName(editingResponsable.last_name || '');
        setPhone(editingResponsable.phone || '');
        setEmail(editingResponsable.email || '');
        setAddress(editingResponsable.address || '');
      } else {
        setFirstName('');
        setLastName('');
        setPhone('');
        setEmail('');
        setAddress('');
      }
    }
  }, [open, editingResponsable]);

  const handleSubmit = () => {
    if (!firstName.trim() || !lastName.trim()) {
      setLocalError("Le prénom et le nom sont obligatoires.");
      return;
    }

    onSave({
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      phone: phone.trim() || null,
      email: email.trim() || null,
      address: address.trim() || null,
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      aria-labelledby="responsable-form-title"
    >
      <DialogTitle id="responsable-form-title">
        {editingResponsable
          ? 'Modifier le responsable'
          : 'Ajouter un responsable'}
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
            label="Téléphone"
            value={phone}
            onChange={(event) => setPhone(event.target.value)}
            fullWidth
          />

          <TextField
            label="Email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            fullWidth
          />

          <TextField
            label="Adresse"
            value={address}
            onChange={(event) => setAddress(event.target.value)}
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
          ) : editingResponsable ? (
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