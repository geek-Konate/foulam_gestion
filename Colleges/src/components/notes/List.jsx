import {
  Alert, Box, CircularProgress, IconButton, Paper, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Tooltip, Typography,
} from '@mui/material';
import { Delete } from '@mui/icons-material';

function List({ notes, eleves = [], loading, onDelete }) {
  if (loading) {
    return <Box sx={{ minHeight: 200, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <CircularProgress />
    </Box>;
  }
  if (notes.length === 0) {
    return <Alert severity="info">Aucune note saisie pour cette évaluation.</Alert>;
  }
  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Élève</TableCell>
            <TableCell>Note /20</TableCell>
            <TableCell>Commentaire</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {notes.map((n) => {
            const el = eleves.find((e) => e.id === n.student_id);
            return (
              <TableRow key={n.id} hover>
                <TableCell>
                  <Typography fontWeight={600}>
                    {el ? `${el.last_name} ${el.first_name}` : '—'}
                  </Typography>
                </TableCell>
                <TableCell>{n.value}</TableCell>
                <TableCell>{n.comment || '—'}</TableCell>
                <TableCell align="right">
                  <Tooltip title="Supprimer">
                    <IconButton size="small" color="error" onClick={() => onDelete(n)}>
                      <Delete />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default List;