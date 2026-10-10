import {
  Alert,
  Box,
  CircularProgress,
  IconButton,
  List as MuiList,
  ListItem,
  ListItemText,
  Paper,
  Tooltip,
  Typography,
} from '@mui/material';
import { Delete } from '@mui/icons-material';

function List({ links, matieres = [], loading, onRemove }) {
  const resolveName = (subjectId) => {
    const m = matieres.find((x) => x.id === subjectId);
    return m ? m.name : '—';
  };

  if (loading) {
    return (
      <Box sx={{ minHeight: 120, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <CircularProgress size={28} />
      </Box>
    );
  }

  if (links.length === 0) {
    return (
      <Alert severity="info">Aucune matière dans cette maquette pour l'instant.</Alert>
    );
  }

  return (
    <Paper sx={{ borderRadius: 2, p: 1 }}>
      <MuiList dense>
        {links.map((link) => (
          <ListItem
            key={link.id}
            secondaryAction={
              <Tooltip title="Retirer">
                <IconButton edge="end" size="small" color="error" onClick={() => onRemove(link.subject_id)}>
                  <Delete />
                </IconButton>
              </Tooltip>
            }
          >
            <ListItemText
              primary={resolveName(link.subject_id)}
              secondary={`Coefficient : ${link.coefficient} — ${link.weekly_hours}h/semaine`}
            />
          </ListItem>
        ))}
      </MuiList>
    </Paper>
  );
}

export default List;