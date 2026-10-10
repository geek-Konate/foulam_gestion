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

function resolveName(id, list, fallback = '—') {
  if (!id) return fallback;
  return list.find((item) => item.id === id)?.name || fallback;
}

function List({ classes, annees = [], niveaux = [], loading, onEdit, onDelete }) {
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

  if (classes.length === 0) {
    return (
      <Alert severity="info">
        Aucune classe. Cliquez sur « Ajouter » pour en créer une.
      </Alert>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table aria-label="classes">
        <TableHead>
          <TableRow>
            <TableCell>Nom</TableCell>
            <TableCell>Année scolaire</TableCell>
            <TableCell>Niveau</TableCell>
            <TableCell>Capacité</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {classes.map((classe) => (
            <TableRow key={classe.id} hover>
              <TableCell>
                <Typography fontWeight={600}>{classe.name}</Typography>
              </TableCell>

              <TableCell>
                {resolveName(classe.academic_year_id, annees)}
              </TableCell>

              <TableCell>
                {resolveName(classe.level_id, niveaux)}
              </TableCell>

              <TableCell>
                <Chip label={classe.capacity} size="small" />
              </TableCell>

              <TableCell align="right">
                <Tooltip title="Modifier">
                  <IconButton
                    size="small"
                    onClick={() => onEdit(classe)}
                    aria-label="modifier"
                  >
                    <Edit />
                  </IconButton>
                </Tooltip>

                <Tooltip title="Supprimer">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => onDelete(classe)}
                    aria-label="supprimer"
                  >
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