import { Alert, Box, CircularProgress, IconButton, Paper, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Tooltip, Typography } from '@mui/material';
import { Delete, Edit } from '@mui/icons-material';

function List({ types, loading, onEdit, onDelete }) {
  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}><CircularProgress /></Box>;
  if (types.length === 0) return <Alert severity="info">Aucun type de frais. Cliquez sur « Ajouter ».</Alert>;
  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table>
        <TableHead>
          <TableRow><TableCell>Nom</TableCell><TableCell>Montant</TableCell><TableCell align="right">Actions</TableCell></TableRow>
        </TableHead>
        <TableBody>
          {types.map((t) => (
            <TableRow key={t.id} hover>
              <TableCell><Typography fontWeight={600}>{t.name}</Typography></TableCell>
              <TableCell>{t.amount} FCFA</TableCell>
              <TableCell align="right">
                <Tooltip title="Modifier"><IconButton size="small" onClick={() => onEdit(t)}><Edit /></IconButton></Tooltip>
                <Tooltip title="Supprimer"><IconButton size="small" color="error" onClick={() => onDelete(t)}><Delete /></IconButton></Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default List;