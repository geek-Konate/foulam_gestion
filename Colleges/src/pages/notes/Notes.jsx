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

import Form from '../../components/notes/Form';
import List from '../../components/notes/List';
import { useAuth } from '../../hooks/useAuth';
import { useClasses } from '../../hooks/useClasses';
import { useEleves } from '../../hooks/useEleves';
import { useEvaluations } from '../../hooks/useEvaluations';
import { useNotes } from '../../hooks/useNotes';

function Notes() {
  const { activeEstablishmentId, user } = useAuth();
  const currentUserId = user?.id;
  const { classes } = useClasses(activeEstablishmentId);

  const [classId, setClassId] = useState('');
  const [evaluationId, setEvaluationId] = useState('');

  const { evaluations } = useEvaluations(activeEstablishmentId, classId);
  const { eleves } = useEleves(activeEstablishmentId);
  const { notes, loading, saving, error, refresh, createNote, removeNote } = useNotes(
    activeEstablishmentId,
    evaluationId
  );

  const [formOpen, setFormOpen] = useState(false);
  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  // Récupérer les élèves de la classe sélectionnée via l'évaluation
  const classEleves = classId ? eleves.filter((e) => e.class_id === classId) : [];

  const handleSave = async (data) => {
    try {
      await createNote({ ...data, evaluation_id: evaluationId, teacher_id: currentUserId });
      setFormOpen(false);
    } catch {
      /* silence */
    }
  };

  const handleOpenDelete = (note) => {
    setToDelete(note);
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
      await removeNote(toDelete.id);
      setDeleteOpen(false);
      setToDelete(null);
    } catch {
      /* silence */
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Notes
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Saisissez les notes des élèves par évaluation.
        </Typography>
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

      <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center', flexWrap: 'wrap' }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Classe</InputLabel>
          <Select
            label="Classe"
            value={classId}
            onChange={(e) => {
              setClassId(e.target.value);
              setEvaluationId('');
            }}
          >
            {classes.map((c) => (
              <MenuItem key={c.id} value={c.id}>
                {c.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl sx={{ minWidth: 250 }}>
          <InputLabel>Évaluation</InputLabel>
          <Select
            label="Évaluation"
            value={evaluationId}
            onChange={(e) => setEvaluationId(e.target.value)}
            disabled={!classId}
          >
            {evaluations.map((ev) => (
              <MenuItem key={ev.id} value={ev.id}>
                {ev.name} ({ev.date})
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
          disabled={!evaluationId}
          onClick={() => setFormOpen(true)}
        >
          Ajouter une note
        </Button>
      </Box>

      {!evaluationId && (
        <Alert severity="info">Sélectionnez une évaluation pour voir les notes.</Alert>
      )}

      {evaluationId && (
        <List notes={notes} eleves={eleves} loading={loading} onDelete={handleOpenDelete} />
      )}

      <Form
        open={formOpen}
        eleves={eleves}
        notes={notes}
        saving={saving}
        onClose={() => setFormOpen(false)}
        onSave={handleSave}
      />

      <Dialog open={deleteOpen} onClose={handleCloseDelete}>
        <DialogTitle>Supprimer</DialogTitle>
        <DialogContent>Supprimer la note de cet élève ?</DialogContent>
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

export default Notes;
