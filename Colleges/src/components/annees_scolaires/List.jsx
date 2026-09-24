import {
  Alert,
  Box,
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

function formatDate(value) {
  if (!value) return '—';

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) return value;

  return date.toLocaleDateString('fr-FR');
}

function StatusBadge({ status }) {
  const isActive = status === 'active';

  return (
    <Box
      component="span"
      sx={{
        px: 1.2,
        py: 0.4,
        borderRadius: 1,
        fontSize: 12,
        fontWeight: 600,
        bgcolor: isActive ? 'success.main' : 'grey.400',
        color: isActive ? 'success.contrastText' : 'grey.800',
      }}
    >
      {isActive ? 'Active' : 'Inactive'}
    </Box>
  );
}

function List({ annees, loading, onEdit, onDelete }) {
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

  if (annees.length === 0) {
    return (
      <Alert severity="info">
        Aucune année scolaire. Cliquez sur « Ajouter » pour en créer une.
      </Alert>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table aria-label="années scolaires">
        <TableHead>
          <TableRow>
            <TableCell>Nom</TableCell>
            <TableCell>Début</TableCell>
            <TableCell>Fin</TableCell>
            <TableCell>Statut</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {annees.map((annee) => (
            <TableRow key={annee.id} hover>
              <TableCell>
                <Typography fontWeight={600}>{annee.name}</Typography>
              </TableCell>

              <TableCell>{formatDate(annee.start_date)}</TableCell>

              <TableCell>{formatDate(annee.end_date)}</TableCell>

              <TableCell>
                <StatusBadge status={annee.status} />
              </TableCell>

              <TableCell align="right">
                <Tooltip title="Modifier">
                  <IconButton
                    size="small"
                    onClick={() => onEdit(annee)}
                    aria-label="modifier"
                  >
                    <Edit />
                  </IconButton>
                </Tooltip>

                <Tooltip title="Supprimer">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => onDelete(annee)}
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