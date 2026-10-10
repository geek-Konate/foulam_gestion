import { useState } from 'react';

import {
  Alert,
  Box,
  Button,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from '@mui/material';
import { Add, Refresh } from '@mui/icons-material';

import Form from '../../components/eleve_responsables/Form';
import List from '../../components/eleve_responsables/List';
import { useStudentGuardians } from '../../hooks/useStudentGuardians';
import { useEleves } from '../../hooks/useEleves';
import { useResponsables } from '../../hooks/useResponsables';
import { useAuth } from '../../hooks/useAuth';

function EleveResponsables() {
  const { activeEstablishmentId } = useAuth();

  const { eleves } = useEleves(activeEstablishmentId);
  const { responsables } = useResponsables(activeEstablishmentId);

  const [studentId, setStudentId] = useState('');
  const {
    links,
    loading,
    error,
    saving,
    refresh,
    addLink,
    removeLink,
  } = useStudentGuardians(activeEstablishmentId, studentId);

  const [formOpen, setFormOpen] = useState(false);

  const selectedEleve = eleves.find((e) => e.id === studentId);

  const handleSave = async (data) => {
    try {
      await addLink(data);
      setFormOpen(false);
    } catch {
      // L'erreur est déjà exposée par le hook.
    }
  };

  const handleRemove = async (guardianId) => {
    try {
      await removeLink(guardianId);
    } catch {
      // L'erreur est déjà exposée par le hook.
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Responsables des élèves
        </Typography>

        <Typography variant="body1" color="text.secondary">
          Associez un ou plusieurs responsables à un élève.
        </Typography>
      </Box>

      {!activeEstablishmentId && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Aucun établissement sélectionné. Utilisez le sélecteur
          d'établissement dans l'en-tête.
        </Alert>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Sélecteur d'élève */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center' }}>
        <FormControl sx={{ minWidth: 280 }}>
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

        <Button variant="outlined" startIcon={<Refresh />} onClick={refresh}>
          Actualiser
        </Button>

        <Button
          variant="contained"
          startIcon={<Add />}
          disabled={!studentId}
          onClick={() => setFormOpen(true)}
        >
          Associer
        </Button>
      </Box>

      {studentId ? (
        <Box>
          <Typography variant="h6" fontWeight={600} sx={{ mb: 2 }}>
            Responsables de&nbsp;
            {selectedEleve
              ? `${selectedEleve.last_name} ${selectedEleve.first_name}`
              : 'cet élève'}
          </Typography>

          <List
            links={links}
            responsables={responsables}
            loading={loading}
            onRemove={handleRemove}
          />
        </Box>
      ) : (
        <Alert severity="info">
          Sélectionnez un élève pour voir et gérer ses responsables.
        </Alert>
      )}

      <Form
        open={formOpen}
        responsables={responsables}
        links={links}
        saving={saving}
        onClose={() => setFormOpen(false)}
        onSave={handleSave}
      />
    </Box>
  );
}

export default EleveResponsables;