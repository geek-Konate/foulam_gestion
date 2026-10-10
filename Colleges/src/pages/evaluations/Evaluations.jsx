import { useState } from 'react';

import { Add, Refresh } from '@mui/icons-material';
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from '@mui/material';

import Form from '../../components/evaluations/Form';
import List from '../../components/evaluations/List';
import { useAuth } from '../../hooks/useAuth';
import { useClasses } from '../../hooks/useClasses';
import { useEvaluations } from '../../hooks/useEvaluations';
import { useMatieres } from '../../hooks/useMatieres';

function Evaluations() {
  const { activeEstablishmentId } = useAuth();
  const { classes } = useClasses(activeEstablishmentId);
  const { matieres } = useMatieres();

  const [classId, setClassId] = useState('');
  const { evaluations, loading, saving, error, refresh, createEvaluation, removeEvaluation } =
    useEvaluations(activeEstablishmentId, classId);

  const [formOpen, setFormOpen] = useState(false);
  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleSave = async (data) => {
    try {
      await createEvaluation(data);
      setFormOpen(false);
    } catch {
      /* hook */
    }
  };

  const handleOpenDelete = (ev) => {
    setToDelete(ev);
    setDeleteOpen(true);
  };
  const handleCloseDelete = () => {
    if (deleting) return;
    setDeleteOpen(false);
    setToDelete(null);
  };
  const handleDelete = async () => {
    if (!toDelete) return;
    try {
      setDeleting(true);
      await removeEvaluation(toDelete.id);
      setDeleteOpen(false);
      setToDelete(null);
    } catch {
      /* hook */
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Évaluations
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Gérez les évaluations par classe.
          </Typography>
        </Box>
      </Box>

      {!activeEstablishmentId && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Aucun établissement sélectionné.
        </Alert>
      )}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center' }}>
        <FormControl sx={{ minWidth: 280 }}>
          <InputLabel>Classe</InputLabel>
          <Select label="Classe" value={classId} onChange={(e) => setClassId(e.target.value)}>
            {classes.map((c) => (
              <MenuItem key={c.id} value={c.id}>
                {c.name}
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
          disabled={!classId}
          onClick={() => setFormOpen(true)}
        >
          Ajouter
        </Button>
      </Box>

      {classId ? (
        <List
          evaluations={evaluations}
          classes={classes}
          matieres={matieres}
          loading={loading}
          onDelete={handleOpenDelete}
        />
      ) : (
        <Alert severity="info">Sélectionnez une classe pour voir ses évaluations.</Alert>
      )}

      <Form
        open={formOpen}
        classes={classes}
        matieres={matieres}
        saving={saving}
        onClose={() => setFormOpen(false)}
        onSave={handleSave}
      />

      <Dialog open={deleteOpen} onClose={handleCloseDelete}>
        <DialogTitle>Supprimer</DialogTitle>
        <DialogContent>
          Voulez-vous vraiment supprimer l'évaluation <strong>{toDelete?.name}</strong> ?
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDelete} disabled={deleting}>
            Annuler
          </Button>
          <Button variant="contained" color="error" onClick={handleDelete} disabled={deleting}>
            Supprimer
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Evaluations;
