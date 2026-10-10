import {
  Alert, Box, CircularProgress, IconButton, List as MuiList, ListItem, ListItemText,
  Paper, Tooltip,
} from '@mui/material';
import { Delete } from '@mui/icons-material';

function List({ affectations, matieres = [], curriculumSubjects = [], users = [], loading, onRemove }) {
  const resolveSubjectName = (csId) => {
    const cs = curriculumSubjects.find((c) => c.id === csId);
    const mat = matieres.find((m) => m.id === cs?.subject_id);
    return mat ? mat.name : '—';
  };

  const resolveUserName = (userId) => {
    const u = users.find((x) => x.id === userId);
    return u ? `${u.last_name} ${u.first_name}` : '—';
  };

  if (loading) {
    return <Box sx={{ minHeight: 120, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <CircularProgress size={28} />
    </Box>;
  }

  if (affectations.length === 0) {
    return <Alert severity="info">Aucun enseignant affecté dans cette classe.</Alert>;
  }

  return (
    <Paper sx={{ borderRadius: 2, p: 1 }}>
      <MuiList dense>
        {affectations.map((a) => {
          const cs = curriculumSubjects.find((c) => c.id === a.curriculum_subject_id);
          const coeff = cs?.coefficient || '—';
          return (
            <ListItem
              key={a.id}
              secondaryAction={
                <Tooltip title="Retirer">
                  <IconButton edge="end" size="small" color="error" onClick={() => onRemove(a.id)}>
                    <Delete />
                  </IconButton>
                </Tooltip>
              }
            >
              <ListItemText
                primary={`${resolveSubjectName(a.curriculum_subject_id)} — ${resolveUserName(a.user_id)}`}
                secondary={`Coefficient ${coeff}`}
              />
            </ListItem>
          );
        })}
      </MuiList>
    </Paper>
  );
}

export default List;