import { Alert, Box, Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle,
  FormControl, InputLabel, MenuItem, Select, TextField } from '@mui/material';
import { useEffect, useState } from 'react';

function Form({ open, eleves = [], saving, onClose, onSave }) {
  const [studentId, setStudentId] = useState('');
  const [status, setStatus] = useState('present');
  const [remark, setRemark] = useState('');
  const [localError, setLocalError] = useState(null);

  useEffect(() => { if (open) { setLocalError(null); setStudentId(''); setStatus('present'); setRemark(''); } }, [open]);

  const handleSubmit = () => {
    if (!studentId) { setLocalError("Veuillez choisir un élève."); return; }
    onSave({ student_id: studentId, status, remark: remark.trim() || null });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Enregistrer une présence</DialogTitle>
      <DialogContent>
        {localError && <Alert severity="error" sx={{ mb: 2 }}>{localError}</Alert>}
        <Box component="form" noValidate onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <FormControl fullWidth>
            <InputLabel>Élève</InputLabel>
            <Select label="Élève" value={studentId} onChange={(e) => setStudentId(e.target.value)}>
              {eleves.map((el) => <MenuItem key={el.id} value={el.id}>{el.last_name} {el.first_name}</MenuItem>)}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Statut</InputLabel>
            <Select label="Statut" value={status} onChange={(e) => setStatus(e.target.value)}>
              <MenuItem value="present">Présent</MenuItem>
              <MenuItem value="absent">Absent</MenuItem>
              <MenuItem value="retard">Retard</MenuItem>
            </Select>
          </FormControl>
          <TextField label="Remarque" value={remark} onChange={(e) => setRemark(e.target.value)} fullWidth />
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={saving}>Annuler</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? <CircularProgress size={18} color="inherit" /> : 'Enregistrer'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;