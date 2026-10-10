import {
  Alert,
  Box,
  Chip,
  CircularProgress,
  IconButton,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tooltip,
  Typography,
} from '@mui/material';
import { Delete, Edit } from '@mui/icons-material';

function List({ maquettes, annees = [], niveaux = [], loading, onEdit, onDelete }) {
  const resolveName = (id, list) => {
    if (!id) return '—';
    return list.find((item) => item.id === id)?.name || '—';
  };

  if (loading) {
    return (
      <Box
        sx={{
          minHeight: 200,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (maquettes.length === 0) {
    return (
      <Alert severity="info">
        Aucune maquette. Cliquez sur « Ajouter » pour en créer une.
      </Alert>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table aria-label="maquettes">
        <TableHead>
          <TableRow>
            <TableCell>Nom</TableCell>
            <TableCell>Année scolaire</TableCell>
            <TableCell>Niveau</TableCell>
            <TableCell>Statut</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {maquettes.map((m) => (
            <TableRow key={m.id} hover>
              <TableCell>
                <Typography fontWeight={600}>{m.name}</Typography>
              </TableCell>
              <TableCell>{resolveName(m.academic_year_id, annees)}</TableCell>
              <TableCell>{resolveName(m.level_id, niveaux)}</TableCell>
              <TableCell>
                <Chip
                  label={m.status === 'active' ? 'Active' : 'Inactive'}
                  size="small"
                  color={m.status === 'active' ? 'success' : 'default'}
                />
              </TableCell>
              <TableCell align="right">
                <Tooltip title="Modifier">
                  <IconButton size="small" onClick={() => onEdit(m)} aria-label="modifier">
                    <Edit />
                  </IconButton>
                </Tooltip>
                <Tooltip title="Supprimer">
                  <IconButton size="small" color="error" onClick={() => onDelete(m)} aria-label="supprimer">
                    <Delete />
                  </IconButton>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default List;