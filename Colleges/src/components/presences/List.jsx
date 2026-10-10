import { Alert, Box, Chip, CircularProgress, Paper, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Typography } from '@mui/material';

const STATUS_LABELS = { present: 'Présent', absent: 'Absent', retard: 'Retard' };
const STATUS_COLORS = { present: 'success', absent: 'error', retard: 'warning' };

function List({ presences, eleves = [], loading }) {
  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}><CircularProgress /></Box>;
  if (presences.length === 0) return <Alert severity="info">Aucune présence enregistrée pour cette date.</Alert>;

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Élève</TableCell>
            <TableCell>Statut</TableCell>
            <TableCell>Remarque</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {presences.map((p) => {
            const el = eleves.find((e) => e.id === p.student_id);
            return (
              <TableRow key={p.id} hover>
                <TableCell><Typography fontWeight={600}>{el ? `${el.last_name} ${el.first_name}` : '—'}</Typography></TableCell>
                <TableCell><Chip size="small" color={STATUS_COLORS[p.status] || 'default'} label={STATUS_LABELS[p.status] || p.status} /></TableCell>
                <TableCell>{p.remark || '—'}</TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default List;