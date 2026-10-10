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

function List({ matieres, loading, onEdit, onDelete }) {
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

  if (matieres.length === 0) {
    return (
      <Alert severity="info">
        Aucune matière. Cliquez sur « Ajouter » pour en créer une.
      </Alert>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table aria-label="matières">
        <TableHead>
          <TableRow>
            <TableCell>Nom</TableCell>
            <TableCell>Code</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {matieres.map((matiere) => (
            <TableRow key={matiere.id} hover>
              <TableCell>
                <Typography fontWeight={600}>{matiere.name}</Typography>
              </TableCell>

              <TableCell>{matiere.code}</TableCell>

              <TableCell align="right">
                <Tooltip title="Modifier">
                  <IconButton
                    size="small"
                    onClick={() => onEdit(matiere)}
                    aria-label="modifier"
                  >
                    <Edit />
                  </IconButton>
                </Tooltip>

                <Tooltip title="Supprimer">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => onDelete(matiere)}
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