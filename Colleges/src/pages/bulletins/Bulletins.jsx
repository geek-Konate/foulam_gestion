import { useState } from 'react';

import { Add, Refresh } from '@mui/icons-material';
import { Alert, Box, Button, FormControl, InputLabel, MenuItem, Select, Typography } from '@mui/material';

import Form from '../../components/bulletins/Form';
import List from '../../components/bulletins/List';
import { useBulletins } from '../../hooks/useBulletins';
import { useAuth } from '../../hooks/useAuth';
import { useEleves } from '../../hooks/useEleves';
import { useAnneesScolaires } from '../../hooks/useAnneesScolaires';

function Bulletins() {
  const { activeEstablishmentId } = useAuth();
  const { eleves } = useEleves(activeEstablishmentId);
  const { annees } = useAnneesScolaires(activeEstablishmentId);
  const [studentId, setStudentId] = useState('');
  const { bulletins, loading, saving, error, refresh, generateBulletin } = useBulletins(activeEstablishmentId, studentId);
  const [formOpen, setFormOpen] = useState(false);

  const handleSave = async (data) => {
    try {
      await generateBulletin({ student_id: studentId, ...data });
      setFormOpen(false);
    } catch { /* silence */ }
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}><Typography variant="h4" fontWeight={700} gutterBottom>Bulletins</Typography></Box>

      {!activeEstablishmentId && <Alert severity="info" sx={{ mb: 3 }}>Aucun établissement sélectionné.</Alert>}
      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center', flexWrap: 'wrap' }}>
        <FormControl sx={{ minWidth: 280 }}>
          <InputLabel>Élève</InputLabel>
          <Select label="Élève" value={studentId} onChange={(e) => setStudentId(e.target.value)}>
            {eleves.map((el) => <MenuItem key={el.id} value={el.id}>{el.last_name} {el.first_name}</MenuItem>)}
          </Select>
        </FormControl>
        <Button variant="outlined" startIcon={<Refresh />} onClick={refresh}>Actualiser</Button>
        <Button variant="contained" startIcon={<Add />} disabled={!studentId} onClick={() => setFormOpen(true)}>
          Générer
        </Button>
      </Box>

      {studentId ? <List bulletins={bulletins} loading={loading} />
        : <Alert severity="info">Sélectionnez un élève pour voir ses bulletins.</Alert>}

      <Form open={formOpen} annees={annees} saving={saving}
        onClose={() => setFormOpen(false)} onSave={handleSave} />
    </Box>
  );
}

export default Bulletins;