import { Alert, Box, Chip, CircularProgress, Paper, Table, TableBody, TableCell,
  TableContainer, TableHead, TableRow, Typography } from '@mui/material';

function formatDate(value) {
  if (!value) return '—';
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? value : d.toLocaleDateString('fr-FR');
}

function List({ bulletins, loading }) {
  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}><CircularProgress /></Box>;
  if (bulletins.length === 0) return <Alert severity="info">Aucun bulletin pour cet élève.</Alert>;

  return (
    <TableContainer component={Paper} sx={{ borderRadius: 2 }}>
      <Table>
        <TableHead>
          <TableRow><TableCell>Période</TableCell><TableCell>Généré le</TableCell><TableCell>Fichier</TableCell></TableRow>
        </TableHead>
        <TableBody>
          {bulletins.map((b) => (
            <TableRow key={b.id} hover>
              <TableCell><Chip size="small" label={b.period} /></TableCell>
              <TableCell>{formatDate(b.generated_at)}</TableCell>
              <TableCell>{b.file_url ? 'PDF' : '—'}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

export default List;