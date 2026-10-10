import { useState } from 'react';

import { Add, Refresh } from '@mui/icons-material';
import { Alert, Box, Button, FormControl, InputLabel, MenuItem, Select, TextField, Typography } from '@mui/material';

import Form from '../../components/presences/Form';
import List from '../../components/presences/List';
import { usePresences } from '../../hooks/usePresences';
import { useAuth } from '../../hooks/useAuth';
import { useClasses } from '../../hooks/useClasses';
import { useEleves } from '../../hooks/useEleves';

function Presences() {
  const { activeEstablishmentId } = useAuth();
  const { classes } = useClasses(activeEstablishmentId);
  const { eleves } = useEleves(activeEstablishmentId);

  const [classId, setClassId] = useState('');
  const [date, setDate] = useState('');
  const { presences, loading, saving, error, refresh, savePresence } = usePresences(activeEstablishmentId, classId, date);

  const [formOpen, setFormOpen] = useState(false);

  const handleSave = async (data) => {
    try { await savePresence({ ...data, class_id: classId, date }); setFormOpen(false); }
    catch { /* silence */ }
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}><Typography variant="h4" fontWeight={700} gutterBottom>Présences</Typography></Box>

      {!activeEstablishmentId && <Alert severity="info" sx={{ mb: 3 }}>Aucun établissement sélectionné.</Alert>}
      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center', flexWrap: 'wrap' }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Classe</InputLabel>
          <Select label="Classe" value={classId} onChange={(e) => setClassId(e.target.value)}>
            {classes.map((c) => <MenuItem key={c.id} value={c.id}>{c.name}</MenuItem>)}
          </Select>
        </FormControl>
        <TextField label="Date" type="date" value={date} onChange={(e) => setDate(e.target.value)}
          InputLabelProps={{ shrink: true }} sx={{ minWidth: 180 }} />
        <Button variant="outlined" startIcon={<Refresh />} onClick={refresh}>Actualiser</Button>
        <Button variant="contained" startIcon={<Add />} disabled={!classId || !date} onClick={() => setFormOpen(true)}>
          Ajouter
        </Button>
      </Box>

      {!classId || !date ? <Alert severity="info">Sélectionnez une classe et une date.</Alert>
        : <List presences={presences} eleves={eleves} loading={loading} />}

      <Form open={formOpen} eleves={eleves} saving={saving}
        onClose={() => setFormOpen(false)} onSave={handleSave} />
    </Box>
  );
}

export default Presences;