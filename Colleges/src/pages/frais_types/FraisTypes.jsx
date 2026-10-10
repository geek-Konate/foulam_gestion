import { useState } from 'react';
import { Add, Refresh } from '@mui/icons-material';
import { Alert, Box, Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Typography } from '@mui/material';
import Form from '../../components/frais_types/Form';
import List from '../../components/frais_types/List';
import { useFraisTypes } from '../../hooks/useFraisTypes';
import { useAuth } from '../../hooks/useAuth';

function FraisTypes() {
  const { activeEstablishmentId } = useAuth();
  const { types, loading, error, saving, refresh, create, update, remove } = useFraisTypes(activeEstablishmentId);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState(null);
  const [toDelete, setToDelete] = useState(null);
  const [delOpen, setDelOpen] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const handleSave = async (data) => { try { if (editing) await update(editing.id, data); else await create(data); setOpen(false); setEditing(null); } catch { /* */ } };
  const handleDelete = async () => { if (!toDelete) return; try { setDeleting(true); await remove(toDelete.id); setDelOpen(false); setToDelete(null); } catch { /* */ } finally { setDeleting(false); } };

  return (
    <Box>
      <Box sx={{ mb: 4, display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div><Typography variant="h4" fontWeight={700} gutterBottom>Types de frais</Typography></div>
        <Box>
          <Button variant="outlined" startIcon={<Refresh />} onClick={refresh} sx={{ mr: 1 }}>Actualiser</Button>
          <Button variant="contained" startIcon={<Add />} onClick={() => { setEditing(null); setOpen(true); }}>Ajouter</Button>
        </Box>
      </Box>
      {!activeEstablishmentId && <Alert severity="info" sx={{ mb: 3 }}>Aucun établissement sélectionné.</Alert>}
      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
      <List types={types} loading={loading} onEdit={(t) => { setEditing(t); setOpen(true); }} onDelete={(t) => { setToDelete(t); setDelOpen(true); }} />
      <Form open={open} editing={editing} saving={saving} onClose={() => { setOpen(false); setEditing(null); }} onSave={handleSave} />
      <Dialog open={delOpen} onClose={() => { if (deleting) return; setDelOpen(false); setToDelete(null); }}>
        <DialogTitle>Supprimer</DialogTitle>
        <DialogContent><DialogContentText>Supprimer <strong>{toDelete?.name}</strong> ?</DialogContentText></DialogContent>
        <DialogActions>
          <Button onClick={() => { setDelOpen(false); setToDelete(null); }} disabled={deleting}>Annuler</Button>
          <Button variant="contained" color="error" onClick={handleDelete} disabled={deleting}>Supprimer</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default FraisTypes;