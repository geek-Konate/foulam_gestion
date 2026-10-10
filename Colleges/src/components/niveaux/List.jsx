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

function List({ niveaux, loading, onEdit, onDelete }) {
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

  if (niveaux.length === 0) {
    return (
      <Alert severity="info">
        Aucun niveau. Cliquez sur « Ajouter » pour en créer un.
      </Alert>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table aria-label="niveaux">
        <TableHead>
          <TableRow>
            <TableCell>Nom</TableCell>
            <TableCell>Catégorie</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {niveaux.map((niveau) => (
            <TableRow key={niveau.id} hover>
              <TableCell>
                <Typography fontWeight={600}>{niveau.name}</Typography>
              </TableCell>

              <TableCell>{niveau.category}</TableCell>

              <TableCell align="right">
                <Tooltip title="Modifier">
                  <IconButton
                    size="small"
                    onClick={() => onEdit(niveau)}
                    aria-label="modifier"
                  >
                    <Edit />
                  </IconButton>
                </Tooltip>

                <Tooltip title="Supprimer">
                  <IconButton
                    size="small"
                    color="error"
                    onClick={() => onDelete(niveau)}
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