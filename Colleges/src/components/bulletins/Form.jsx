import { useEffect, useState } from 'react';
import { Alert, Box, Button, CircularProgress, Dialog, DialogActions, DialogContent, DialogTitle,
  FormControl, InputLabel, MenuItem, Select } from '@mui/material';

function Form({ open, annees = [], saving, onClose, onSave }) {
  const [academicYearId, setAcademicYearId] = useState('');
  const [period, setPeriod] = useState('trimestre 1');
  const [localError, setLocalError] = useState(null);

  useEffect(() => { if (open) { setLocalError(null); setAcademicYearId(''); setPeriod('trimestre 1'); } }, [open]);

  const handleSubmit = () => {
    if (!academicYearId) { setLocalError("Veuillez choisir une année scolaire."); return; }
    onSave({
      academic_year_id: academicYearId,
      period,
      file_url: `https://example.com/bulletins/${Date.now()}.pdf`,
      generated_at: new Date().toISOString(),
    });
  };

  return (
    <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
      <DialogTitle>Générer un bulletin</DialogTitle>
      <DialogContent>
        {localError && <Alert severity="error" sx={{ mb: 2 }}>{localError}</Alert>}
        <Box component="form" noValidate onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}
          sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 1 }}>
          <FormControl fullWidth>
            <InputLabel>Année scolaire</InputLabel>
            <Select label="Année scolaire" value={academicYearId} onChange={(e) => setAcademicYearId(e.target.value)}>
              {annees.map((a) => <MenuItem key={a.id} value={a.id}>{a.name}</MenuItem>)}
            </Select>
          </FormControl>
          <FormControl fullWidth>
            <InputLabel>Période</InputLabel>
            <Select label="Période" value={period} onChange={(e) => setPeriod(e.target.value)}>
              <MenuItem value="trimestre 1">Trimestre 1</MenuItem>
              <MenuItem value="trimestre 2">Trimestre 2</MenuItem>
              <MenuItem value="trimestre 3">Trimestre 3</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} disabled={saving}>Annuler</Button>
        <Button variant="contained" onClick={handleSubmit} disabled={saving}>
          {saving ? <CircularProgress size={18} color="inherit" /> : 'Générer'}
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default Form;