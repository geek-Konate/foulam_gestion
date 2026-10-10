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

function formatDate(value) {
  if (!value) return '—';
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString('fr-FR');
}

const GENDER_LABELS = {
  M: 'Garçon',
  F: 'Fille',
  masculin: 'Masculin',
  féminin: 'Féminin',
  feminin: 'Féminin',
};

function List({ eleves, loading, onEdit, onDelete }) {
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

  if (eleves.length === 0) {
    return (
      <Alert severity="info">
        Aucun élève. Cliquez sur « Ajouter » pour en enregistrer un.
      </Alert>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table aria-label="élèves">
        <TableHead>
          <TableRow>
            <TableCell>Nom complet</TableCell>
            <TableCell>Date de naissance</TableCell>
            <TableCell>Genre</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {eleves.map((eleve) => (
            <TableRow key={eleve.id} hover>
              <TableCell>
                <Typography fontWeight={600}>
                  {eleve.last_name} {eleve.first_name}
                </Typography>
              </TableCell>

              <TableCell>{formatDate(eleve.birth_date)}</TableCell>

              <TableCell>
                <Chip
                  label={GENDER_LABELS[eleve.gender] || eleve.gender}
                  size="small"
                />
              </TableCell>

              <TableCell align="right">
                <Tooltip title="Modifier">
                  <IconButton
                    size="small"
                    onClick={() => onEdit(eleve)}
                    aria-label="modifier"
                  >
                    <Edit />
                  </IconButton>
                </Tooltip>

                <Tooltip title="Supprimer">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => onDelete(eleve)}
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