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

import Form from '../../components/matieres/Form';
import List from '../../components/matieres/List';
import { useMatieres } from '../../hooks/useMatieres';

function Matieres() {
  const {
    matieres,
    loading,
    error,
    saving,
    refresh,
    createMatiere,
    updateMatiere,
    removeMatiere,
  } = useMatieres();

  const [formOpen, setFormOpen] = useState(false);
  const [editingMatiere, setEditingMatiere] = useState(null);

  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleOpenAdd = () => {
    setEditingMatiere(null);
    setFormOpen(true);
  };

  const handleOpenEdit = (matiere) => {
    setEditingMatiere(matiere);
    setFormOpen(true);
  };

  const handleCloseForm = () => {
    if (saving) return;
    setFormOpen(false);
    setEditingMatiere(null);
  };

  const handleSave = async (data) => {
    try {
      if (editingMatiere) {
        await updateMatiere(editingMatiere.id, data);
      } else {
        await createMatiere(data);
      }

      setFormOpen(false);
      setEditingMatiere(null);
    } catch {
      // L'erreur est déjà exposée par le hook.
    }
  };

  const handleOpenDelete = (matiere) => {
    setToDelete(matiere);
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
      await removeMatiere(toDelete.id);
      setDeleteOpen(false);
      setToDelete(null);
    } catch {
      // L'erreur est déjà exposée par le hook.
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
            Matières
          </Typography>

          <Typography variant="body1" color="text.secondary">
            Gérez les matières enseignées.
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
        matieres={matieres}
        loading={loading}
        onEdit={handleOpenEdit}
        onDelete={handleOpenDelete}
      />

      <Form
        open={formOpen}
        editingMatiere={editingMatiere}
        saving={saving}
        onClose={handleCloseForm}
        onSave={handleSave}
      />

      <Dialog
        open={deleteOpen}
        onClose={handleCloseDelete}
        aria-labelledby="delete-matiere-title"
      >
        <DialogTitle id="delete-matiere-title">Supprimer</DialogTitle>

        <DialogContent>
          <DialogContentText>
            Voulez-vous vraiment supprimer la matière{' '}
            <strong>{toDelete?.name}</strong> ? Cette action est irréversible.
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

export default Matieres;