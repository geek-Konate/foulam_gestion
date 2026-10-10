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

import Form from '../../components/eleves/Form';
import List from '../../components/eleves/List';
import { useEleves } from '../../hooks/useEleves';
import { useAuth } from '../../hooks/useAuth';

function Eleves() {
  const { activeEstablishmentId } = useAuth();

  const {
    eleves,
    loading,
    error,
    saving,
    refresh,
    createEleve,
    updateEleve,
    removeEleve,
  } = useEleves(activeEstablishmentId);

  const [formOpen, setFormOpen] = useState(false);
  const [editingEleve, setEditingEleve] = useState(null);

  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleOpenAdd = () => {
    setEditingEleve(null);
    setFormOpen(true);
  };

  const handleOpenEdit = (eleve) => {
    setEditingEleve(eleve);
    setFormOpen(true);
  };

  const handleCloseForm = () => {
    if (saving) return;
    setFormOpen(false);
    setEditingEleve(null);
  };

  const handleSave = async (data) => {
    try {
      if (editingEleve) {
        await updateEleve(editingEleve.id, data);
      } else {
        await createEleve(data);
      }

      setFormOpen(false);
      setEditingEleve(null);
    } catch {
      // L'erreur est déjà exposée par le hook.
    }
  };

  const handleOpenDelete = (eleve) => {
    setToDelete(eleve);
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
      await removeEleve(toDelete.id);
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
            Élèves
          </Typography>

          <Typography variant="body1" color="text.secondary">
            Gérez les élèves de votre établissement.
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
        eleves={eleves}
        loading={loading}
        onEdit={handleOpenEdit}
        onDelete={handleOpenDelete}
      />

      <Form
        open={formOpen}
        editingEleve={editingEleve}
        saving={saving}
        onClose={handleCloseForm}
        onSave={handleSave}
      />

      <Dialog
        open={deleteOpen}
        onClose={handleCloseDelete}
        aria-labelledby="delete-eleve-title"
      >
        <DialogTitle id="delete-eleve-title">Supprimer</DialogTitle>

        <DialogContent>
          <DialogContentText>
            Voulez-vous vraiment supprimer l’élève{' '}
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

export default Eleves;