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
 * Formulaire des inscriptions.
 * Gère l'ajout et l'édition selon la prop `editingInscription`.
 */
function Form({
  open,
  editingInscription,
  eleves = [],
  classes = [],
  saving,
  onClose,
  onSave,
}) {
  const [studentId, setStudentId] = useState('');
  const [classId, setClassId] = useState('');
  const [enrollmentDate, setEnrollmentDate] = useState('');
  const [status, setStatus] = useState('active');
  const [localError, setLocalError] = useState(null);

  useEffect(() => {
    if (open) {
      setLocalError(null);

      if (editingInscription) {
        setStudentId(editingInscription.student_id || '');
        setClassId(editingInscription.class_id || '');
        setEnrollmentDate(editingInscription.enrollment_date || '');
        setStatus(editingInscription.status || 'active');
      } else {
        setStudentId('');
        setClassId('');
        setEnrollmentDate('');
        setStatus('active');
      }
    }
  }, [open, editingInscription]);

  const handleSubmit = () => {
    if (!studentId) {
      setLocalError("Veuillez choisir un élève.");
      return;
    }

    if (!classId) {
      setLocalError("Veuillez choisir une classe.");
      return;
    }

    if (!enrollmentDate) {
      setLocalError("La date d'inscription est obligatoire.");
      return;
    }

    onSave({
      student_id: studentId,
      class_id: classId,
      enrollment_date: enrollmentDate,
      status,
    });
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      fullWidth
      maxWidth="sm"
      aria-labelledby="inscription-form-title"
    >
      <DialogTitle id="inscription-form-title">
        {editingInscription
          ? 'Modifier l’inscription'
          : 'Ajouter une inscription'}
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
          <FormControl fullWidth>
            <InputLabel>Élève</InputLabel>
            <Select
              label="Élève"
              value={studentId}
              onChange={(event) => setStudentId(event.target.value)}
            >
              {eleves.map((el) => (
                <MenuItem key={el.id} value={el.id}>
                  {el.last_name} {el.first_name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl fullWidth>
            <InputLabel>Classe</InputLabel>
            <Select
              label="Classe"
              value={classId}
              onChange={(event) => setClassId(event.target.value)}
            >
              {classes.map((cl) => (
                <MenuItem key={cl.id} value={cl.id}>
                  {cl.name}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <TextField
            label="Date d'inscription"
            type="date"
            value={enrollmentDate}
            onChange={(event) => setEnrollmentDate(event.target.value)}
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

        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? (
            <CircularProgress size={18} color="inherit" />
          ) : editingInscription ? (
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