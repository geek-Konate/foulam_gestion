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

function studentName(studentId, eleves) {
  const el = eleves.find((e) => e.id === studentId);
  return el ? `${el.last_name} ${el.first_name}` : '—';
}

function List({ inscriptions, eleves = [], classes = [], loading, onEdit, onDelete }) {
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

  if (inscriptions.length === 0) {
    return (
      <Alert severity="info">
        Aucune inscription. Cliquez sur « Ajouter » pour en créer une.
      </Alert>
    );
  }

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table aria-label="inscriptions">
        <TableHead>
          <TableRow>
            <TableCell>Élève</TableCell>
            <TableCell>Classe</TableCell>
            <TableCell>Date</TableCell>
            <TableCell>Statut</TableCell>
            <TableCell align="right">Actions</TableCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {inscriptions.map((ins) => {
            const classe = classes.find((c) => c.id === ins.class_id);
            return (
              <TableRow key={ins.id} hover>
                <TableCell>
                  <Typography fontWeight={600}>
                    {studentName(ins.student_id, eleves)}
                  </Typography>
                </TableCell>

                <TableCell>{classe ? classe.name : '—'}</TableCell>

                <TableCell>{formatDate(ins.enrollment_date)}</TableCell>

                <TableCell>
                  <Chip label={ins.status} size="small" />
                </TableCell>

                <TableCell align="right">
                  <Tooltip title="Modifier">
                    <IconButton
                      size="small"
                      onClick={() => onEdit(ins)}
                      aria-label="modifier"
                    >
                      <Edit />
                    </IconButton>
                  </Tooltip>

                  <Tooltip title="Supprimer">
                    <IconButton
                      size="small"
                      color="error"
                      onClick={() => onDelete(ins)}
                      aria-label="supprimer"
                    >
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