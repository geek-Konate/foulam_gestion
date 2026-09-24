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
import { Add } from '@mui/icons-material';

import Form from '../../components/annees_scolaires/Form';
import List from '../../components/annees_scolaires/List';
import { useAnneesScolaires } from '../../hooks/useAnneesScolaires';
import { useAuth } from '../../hooks/useAuth';

function AnneesScolaires() {
  const { user } = useAuth();
  const establishmentId = user?.establishment_id;

  const {
    annees,
    loading,
    error,
    saving,
    createAnnee,
    updateAnnee,
    removeAnnee,
  } = useAnneesScolaires(establishmentId);

  const [formOpen, setFormOpen] = useState(false);
  const [editingAnnee, setEditingAnnee] = useState(null);

  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleOpenAdd = () => {
    setEditingAnnee(null);
    setFormOpen(true);
  };

  const handleOpenEdit = (annee) => {
    setEditingAnnee(annee);
    setFormOpen(true);
  };

  const handleCloseForm = () => {
    if (saving) return;
    setFormOpen(false);
    setEditingAnnee(null);
  };

  const handleSave = async (data) => {
    try {
      if (editingAnnee) {
        await updateAnnee(editingAnnee.id, data);
      } else {
        await createAnnee(data);
      }

      setFormOpen(false);
      setEditingAnnee(null);
    } catch {
      // L'erreur est déjà exposée par le hook (error).
    }
  };

  const handleOpenDelete = (annee) => {
    setToDelete(annee);
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
      await removeAnnee(toDelete.id);
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
            Années scolaires
          </Typography>

          <Typography variant="body1" color="text.secondary">
            Gérez les années scolaires de votre établissement.
          </Typography>
        </Box>

        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleOpenAdd}
        >
          Ajouter
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <List
        annees={annees}
        loading={loading}
        onEdit={handleOpenEdit}
        onDelete={handleOpenDelete}
      />

      {/* Formulaire (ajout + édition) */}
      <Form
        open={formOpen}
        editingAnnee={editingAnnee}
        saving={saving}
        onClose={handleCloseForm}
        onSave={handleSave}
      />

      {/* Confirmation de suppression */}
      <Dialog
        open={deleteOpen}
        onClose={handleCloseDelete}
        aria-labelledby="delete-annee-title"
      >
        <DialogTitle id="delete-annee-title">Supprimer</DialogTitle>

        <DialogContent>
          <DialogContentText>
            Voulez-vous vraiment supprimer l’année scolaire{' '}
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

export default AnneesScolaires;