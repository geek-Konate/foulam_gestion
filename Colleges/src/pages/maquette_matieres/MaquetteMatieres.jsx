import { useState } from 'react';

import {
  Alert, Box, Button, FormControl, InputLabel, MenuItem, Select, Typography,
} from '@mui/material';
import { Add, Refresh } from '@mui/icons-material';

import Form from '../../components/maquette_matieres/Form';
import List from '../../components/maquette_matieres/List';
import { useCurriculumSubjects } from '../../hooks/useCurriculumSubjects';
import { useMaquettes } from '../../hooks/useMaquettes';
import { useMatieres } from '../../hooks/useMatieres';
import { useAuth } from '../../hooks/useAuth';

function MaquetteMatieres() {
  const { activeEstablishmentId } = useAuth();
  const { maquettes } = useMaquettes(activeEstablishmentId);
  const { matieres } = useMatieres();

  const [curriculumId, setCurriculumId] = useState('');

  const { links, loading, error, saving, refresh, addSubject, removeSubject }
    = useCurriculumSubjects(activeEstablishmentId, curriculumId);

  const [formOpen, setFormOpen] = useState(false);
  const selectedMaquette = maquettes.find((m) => m.id === curriculumId);

  const handleSave = async (subjectId, data) => {
    try {
      await addSubject(subjectId, data);
      setFormOpen(false);
    } catch { /* L'erreur est déjà exposée par le hook */ }
  };

  const handleRemove = async (subjectId) => {
    try { await removeSubject(subjectId); }
    catch { /* L'erreur est déjà exposée par le hook */ }
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>Matières des maquettes</Typography>
        <Typography variant="body1" color="text.secondary">
          Ajoutez ou retirez des matières (coefficient, heures) dans une maquette.
        </Typography>
      </Box>

      {!activeEstablishmentId && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Aucun établissement sélectionné. Utilisez le sélecteur dans l'en-tête.
        </Alert>
      )}

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center' }}>
        <FormControl sx={{ minWidth: 280 }}>
          <InputLabel>Maquette</InputLabel>
          <Select label="Maquette" value={curriculumId} onChange={(e) => setCurriculumId(e.target.value)}>
            {maquettes.map((m) => <MenuItem key={m.id} value={m.id}>{m.name}</MenuItem>)}
          </Select>
        </FormControl>

        <Button variant="outlined" startIcon={<Refresh />} onClick={refresh}>Actualiser</Button>
        <Button variant="contained" startIcon={<Add />} disabled={!curriculumId} onClick={() => setFormOpen(true)}>
          Ajouter une matière
        </Button>
      </Box>

      {curriculumId ? (
        <Box>
          <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>
            Matières de : {selectedMaquette?.name || 'cette maquette'}
          </Typography>
          <List links={links} matieres={matieres} loading={loading} onRemove={handleRemove} />
        </Box>
      ) : (
        <Alert severity="info">Sélectionnez une maquette pour voir et gérer ses matières.</Alert>
      )}

      <Form open={formOpen} links={links} matieres={matieres} saving={saving}
        onClose={() => setFormOpen(false)} onSave={handleSave} />
    </Box>
  );
}

export default MaquetteMatieres;