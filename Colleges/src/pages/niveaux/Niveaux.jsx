import { useState } from 'react';

import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Typography,
} from '@mui/material';
import { Add, Refresh } from '@mui/icons-material';

import Form from '../../components/niveaux/Form';
import List from '../../components/niveaux/List';
import { useNiveaux } from '../../hooks/useNiveaux';

function Niveaux() {
  const {
    niveaux,
    loading,
    error,
    saving,
    refresh,
    createNiveau,
    updateNiveau,
    removeNiveau,
  } = useNiveaux();

  const [formOpen, setFormOpen] = useState(false);
  const [editingNiveau, setEditingNiveau] = useState(null);

  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleOpenAdd = () => {
    setEditingNiveau(null);
    setFormOpen(true);
  };

  const handleOpenEdit = (niveau) => {
    setEditingNiveau(niveau);
    setFormOpen(true);
  };

  const handleCloseForm = () => {
    if (saving) return;
    setFormOpen(false);
    setEditingNiveau(null);
  };

  const handleSave = async (data) => {
    try {
      if (editingNiveau) {
        await updateNiveau(editingNiveau.id, data);
      } else {
        await createNiveau(data);
      }

      setFormOpen(false);
      setEditingNiveau(null);
    } catch {
      // L'erreur est déjà exposée par le hook (error).
    }
  };

  const handleOpenDelete = (niveau) => {
    setToDelete(niveau);
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
      await removeNiveau(toDelete.id);
      setDeleteOpen(false);
      setToDelete(null);
    } catch {
      // L'erreur est déjà exposée par le hook (error).
    } finally {
      setDeleting(false);
    }
  };

  return (
    <Box>
      <Box
        sx={{
          mb: 4,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Niveaux
          </Typography>

          <Typography variant="body1" color="text.secondary">
            Gérez les niveaux scolaires (primaire, collège, lycée).
          </Typography>
        </Box>

        <Box>
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={refresh}
            sx={{ mr: 1 }}
          >
            Actualiser
          </Button>

          <Button variant="contained" startIcon={<Add />} onClick={handleOpenAdd}>
            Ajouter
          </Button>
        </Box>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <List
        niveaux={niveaux}
        loading={loading}
        onEdit={handleOpenEdit}
        onDelete={handleOpenDelete}
      />

      {/* Formulaire (ajout + édition) */}
      <Form
        open={formOpen}
        editingNiveau={editingNiveau}
        saving={saving}
        onClose={handleCloseForm}
        onSave={handleSave}
      />

      {/* Confirmation de suppression */}
      <Dialog
        open={deleteOpen}
        onClose={handleCloseDelete}
        aria-labelledby="delete-niveau-title"
      >
        <DialogTitle id="delete-niveau-title">Supprimer</DialogTitle>

        <DialogContent>
          <DialogContentText>
            Voulez-vous vraiment supprimer le niveau{' '}
            <strong>{toDelete?.name}</strong> ? Cette action est
            irréversible.
          </DialogContentText>
        </DialogContent>

        <DialogActions>
          <Button onClick={handleCloseDelete} disabled={deleting}>
            Annuler
          </Button>

          <Button
            variant="contained"
            color="error"
            onClick={handleDelete}
            disabled={deleting}
          >
            Supprimer
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Niveaux;