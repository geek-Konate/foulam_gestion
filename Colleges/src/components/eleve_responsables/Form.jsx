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
} from '@mui/material';

/**
 * Association d'un responsable à l'élève sélectionné.
 * Choisit un responsable + le type de lien (père, mère, tuteur...).
 */
function Form({ open, responsables = [], links = [], saving, onClose, onSave }) {
  const [guardianId, setGuardianId] = useState('');
  const [relationshipType, setRelationshipType] = useState('tuteur');
  const [localError, setLocalError] = useState(null);

  // Exclut les responsables déjà associés à cet élève
  const available = responsables.filter(
    (r) => !links.some((link) => link.guardian_id === r.id)
  );

  useEffect(() => {
    if (open) {
      setLocalError(null);
      setGuardianId('');
      setRelationshipType('tuteur');
    }
  }, [open]);

  const handleSubmit = () => {
    if (!guardianId) {
      setLocalError("Veuillez choisir un responsable.");
      return;
    }

    onSave({
      guardian_id: guardianId,
      relationship_type: relationshipType,
    });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm" aria-labelledby="link-form-title">
      <DialogTitle id="link-form-title">Associer un responsable</DialogTitle>

      <DialogContent>
        {localError && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {localError}
          </Alert>
        )}

        {available.length === 0 && (
          <Alert severity="warning" sx={{ mb: 2 }}>
            Tous les responsables sont déjà associés à cet élève.
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
          <FormControl fullWidth>
            <InputLabel>Responsable</InputLabel>
            <Select
              label="Responsable"
              value={guardianId}
              onChange={(event) => setGuardianId(event.target.value)}
            >
              {available.map((resp) => (
                <MenuItem key={resp.id} value={resp.id}>
                  {resp.last_name} {resp.first_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth>
            <InputLabel>Lien</InputLabel>
            <Select
              label="Lien"
              value={relationshipType}
              onChange={(event) => setRelationshipType(event.target.value)}
            >
              <MenuItem value="père">Père</MenuItem>
              <MenuItem value="mère">Mère</MenuItem>
              <MenuItem value="tuteur">Tuteur</MenuItem>
              <MenuItem value="autre">Autre</MenuItem>
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
          disabled={saving || available.length === 0}
        >
          {saving ? (
            <CircularProgress size={18} color="inherit" />
          ) : (
            'Associer'
          )}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;