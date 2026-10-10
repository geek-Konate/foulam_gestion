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

import Form from '../../components/responsables/Form';
import List from '../../components/responsables/List';
import { useResponsables } from '../../hooks/useResponsables';
import { useAuth } from '../../hooks/useAuth';

function Responsables() {
  const { activeEstablishmentId } = useAuth();

  const {
    responsables,
    loading,
    error,
    saving,
    refresh,
    createResponsable,
    updateResponsable,
    removeResponsable,
  } = useResponsables(activeEstablishmentId);

  const [formOpen, setFormOpen] = useState(false);
  const [editingResponsable, setEditingResponsable] = useState(null);

  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleOpenAdd = () => {
    setEditingResponsable(null);
    setFormOpen(true);
  };

  const handleOpenEdit = (responsable) => {
    setEditingResponsable(responsable);
    setFormOpen(true);
  };

  const handleCloseForm = () => {
    if (saving) return;
    setFormOpen(false);
    setEditingResponsable(null);
  };

  const handleSave = async (data) => {
    try {
      if (editingResponsable) {
        await updateResponsable(editingResponsable.id, data);
      } else {
        await createResponsable(data);
      }

      setFormOpen(false);
      setEditingResponsable(null);
    } catch {
      // L'erreur est déjà exposée par le hook.
    }
  };

  const handleOpenDelete = (responsable) => {
    setToDelete(responsable);
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
      await removeResponsable(toDelete.id);
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
            Responsables
          </Typography>

          <Typography variant="body1" color="text.secondary">
            Gérez les responsables (parents, tuteurs...) de votre établissement.
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

      <List
        responsables={responsables}
        loading={loading}
        onEdit={handleOpenEdit}
        onDelete={handleOpenDelete}
      />

      <Form
        open={formOpen}
        editingResponsable={editingResponsable}
        saving={saving}
        onClose={handleCloseForm}
        onSave={handleSave}
      />

      <Dialog
        open={deleteOpen}
        onClose={handleCloseDelete}
        aria-labelledby="delete-responsable-title"
      >
        <DialogTitle id="delete-responsable-title">Supprimer</DialogTitle>

        <DialogContent>
          <DialogContentText>
            Voulez-vous vraiment supprimer le responsable{' '}
            <strong>
              {toDelete?.last_name} {toDelete?.first_name}
            </strong>{' '}
            ? Cette action est irréversible.
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

export default Responsables;