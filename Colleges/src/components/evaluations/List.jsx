import {
  Alert, Box, Chip, CircularProgress, IconButton, Paper, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Tooltip, Typography,
} from '@mui/material';
import { Delete } from '@mui/icons-material';

function formatDate(value) {
  if (!value) return '—';
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? value : d.toLocaleDateString('fr-FR');
}

function List({ evaluations, classes = [], matieres = [], loading, onDelete }) {
  if (loading) {
    return <Box sx={{ minHeight: 200, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <CircularProgress />
    </Box>;
  }
  if (evaluations.length === 0) {
    return <Alert severity="info">Aucune évaluation. Cliquez sur « Ajouter » pour en créer une.</Alert>;
  }
  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Nom</TableCell>
            <TableCell>Classe</TableCell>
            <TableCell>Matière</TableCell>
            <TableCell>Période</TableCell>
            <TableCell>Date</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {evaluations.map((e) => {
            const cl = classes.find((c) => c.id === e.class_id);
            const mat = matieres.find((m) => m.id === e.subject_id);
            return (
              <TableRow key={e.id} hover>
                <TableCell><Typography fontWeight={600}>{e.name}</Typography></TableCell>
                <TableCell>{cl ? cl.name : '—'}</TableCell>
                <TableCell>{mat ? mat.name : '—'}</TableCell>
                <TableCell><Chip label={e.period} size="small" /></TableCell>
                <TableCell>{formatDate(e.date)}</TableCell>
                <TableCell align="right">
                  <Tooltip title="Supprimer">
                    <IconButton size="small" color="error" onClick={() => onDelete(e)}><Delete /></IconButton>
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