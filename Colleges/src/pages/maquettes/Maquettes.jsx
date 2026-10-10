import { useState } from 'react';

import {
  Alert, Box, Button, Dialog, DialogActions, DialogContent, DialogContentText,
  DialogTitle, Typography,
} from '@mui/material';
import { Add, Refresh } from '@mui/icons-material';

import Form from '../../components/maquettes/Form';
import List from '../../components/maquettes/List';
import { useMaquettes } from '../../hooks/useMaquettes';
import { useAnneesScolaires } from '../../hooks/useAnneesScolaires';
import { useNiveaux } from '../../hooks/useNiveaux';
import { useAuth } from '../../hooks/useAuth';

function Maquettes() {
  const { activeEstablishmentId } = useAuth();
  const { maquettes, loading, error, saving, refresh, createMaquette, updateMaquette, removeMaquette }
    = useMaquettes(activeEstablishmentId);
  const { annees } = useAnneesScolaires(activeEstablishmentId);
  const { niveaux } = useNiveaux();

  const [formOpen, setFormOpen] = useState(false);
  const [editingMaquette, setEditingMaquette] = useState(null);
  const [toDelete, setToDelete] = useState(null);
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleOpenAdd = () => { setEditingMaquette(null); setFormOpen(true); };
  const handleOpenEdit = (m) => { setEditingMaquette(m); setFormOpen(true); };
  const handleCloseForm = () => { if (saving) return; setFormOpen(false); setEditingMaquette(null); };

  const handleSave = async (data) => {
    try {
      if (editingMaquette) await updateMaquette(editingMaquette.id, data);
      else await createMaquette(data);
      setFormOpen(false); setEditingMaquette(null);
    } catch { /* L'erreur est déjà exposée par le hook */ }
  };

  const handleOpenDelete = (m) => { setToDelete(m); setDeleteOpen(true); };
  const handleCloseDelete = () => { if (deleting) return; setDeleteOpen(false); setToDelete(null); };
  const handleDelete = async () => {
    if (!toDelete) return;
    try { setDeleting(true); await removeMaquette(toDelete.id); setDeleteOpen(false); setToDelete(null); }
    catch { /* L'erreur est déjà exposée par le hook */ }
    finally { setDeleting(false); }
  };

  return (
    <Box>
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <Box>
          <Typography variant="h4" fontWeight={700} gutterBottom>Maquettes</Typography>
          <Typography variant="body1" color="text.secondary">
            Gérez les maquettes pédagogiques (programmes) de votre établissement.
          </Typography>
        </Box>
        <Box>
          <Button variant="outlined" startIcon={<Refresh />} onClick={refresh} sx={{ mr: 1 }}>Actualiser</Button>
          <Button variant="contained" startIcon={<Add />} onClick={handleOpenAdd}>Ajouter</Button>
        </Box>
      </Box>

      {!activeEstablishmentId && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Aucun établissement sélectionné. Utilisez le sélecteur dans l'en-tête.
        </Alert>
      )}

      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <List maquettes={maquettes} annees={annees} niveaux={niveaux}
        loading={loading} onEdit={handleOpenEdit} onDelete={handleOpenDelete} />

      <Form open={formOpen} editingMaquette={editingMaquette}
        annees={annees} niveaux={niveaux}
        saving={saving} onClose={handleCloseForm} onSave={handleSave} />

      <Dialog open={deleteOpen} onClose={handleCloseDelete} aria-labelledby="delete-maquette-title">
        <DialogTitle id="delete-maquette-title">Supprimer</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Voulez-vous vraiment supprimer la maquette <strong>{toDelete?.name}</strong> ?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDelete} disabled={deleting}>Annuler</Button>
          <Button variant="contained" color="error" onClick={handleDelete} disabled={deleting}>Supprimer</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default Maquettes;