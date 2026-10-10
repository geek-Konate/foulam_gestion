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

import Form from '../../components/classes/Form';
import List from '../../components/classes/List';
import { useClasses } from '../../hooks/useClasses';
import { useAnneesScolaires } from '../../hooks/useAnneesScolaires';
import { useNiveaux } from '../../hooks/useNiveaux';
import { useAuth } from '../../hooks/useAuth';

function Classes() {
  const { activeEstablishmentId } = useAuth();

  const {
    classes,
    loading,
    error,
    saving,
    refresh,
    createClasse,
    updateClasse,
    removeClasse,
  } = useClasses(activeEstablishmentId);

  const { annees } = useAnneesScolaires(activeEstablishmentId);
  const { niveaux } = useNiveaux();

  const [formOpen, setFormOpen] = useState(false);
  const [editingClasse, setEditingClasse] = useState(null);

  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleOpenAdd = () => {
    setEditingClasse(null);
    setFormOpen(true);
  };

  const handleOpenEdit = (classe) => {
    setEditingClasse(classe);
    setFormOpen(true);
  };

  const handleCloseForm = () => {
    if (saving) return;
    setFormOpen(false);
    setEditingClasse(null);
  };

  const handleSave = async (data) => {
    try {
      if (editingClasse) {
        await updateClasse(editingClasse.id, data);
      } else {
        await createClasse(data);
      }

      setFormOpen(false);
      setEditingClasse(null);
    } catch {
      // L'erreur est déjà exposée par le hook.
    }
  };

  const handleOpenDelete = (classe) => {
    setToDelete(classe);
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
      await removeClasse(toDelete.id);
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
            Classes
          </Typography>

          <Typography variant="body1" color="text.secondary">
            Gérez les classes de votre établissement.
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
        classes={classes}
        annees={annees}
        niveaux={niveaux}
        loading={loading}
        onEdit={handleOpenEdit}
        onDelete={handleOpenDelete}
      />

      <Form
        open={formOpen}
        editingClasse={editingClasse}
        annees={annees}
        niveaux={niveaux}
        saving={saving}
        onClose={handleCloseForm}
        onSave={handleSave}
      />

      <Dialog
        open={deleteOpen}
        onClose={handleCloseDelete}
        aria-labelledby="delete-classe-title"
      >
        <DialogTitle id="delete-classe-title">Supprimer</DialogTitle>

        <DialogContent>
          <DialogContentText>
            Voulez-vous vraiment supprimer la classe{' '}
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

export default Classes;