import {
  Alert,
  Box,
  Chip,
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

const RELATION_LABELS = {
  père: 'Père',
  mere: 'Mère',
  mère: 'Mère',
  tuteur: 'Tuteur',
  tutrice: 'Tutrice',
  autre: 'Autre',
};

function List({ links, responsables = [], loading, onRemove }) {
  const resolveName = (guardianId) => {
    const resp = responsables.find((r) => r.id === guardianId);
    return resp ? `${resp.last_name} ${resp.first_name}` : '—';
  };

  if (loading) {
    return (
      <Box
        sx={{
          minHeight: 120,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <CircularProgress size={28} />
      </Box>
    );
  }

  if (links.length === 0) {
    return (
      <Alert severity="info">
        Aucun responsable n'est associé à cet élève pour l'instant.
      </Alert>
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
                <IconButton
                  edge="end"
                  size="small"
                  color="error"
                  onClick={() => onRemove(link.guardian_id)}
                  aria-label="retirer"
                >
                  <Delete />
                </IconButton>
              </Tooltip>
            }
          >
            <ListItemText
              primary={resolveName(link.guardian_id)}
              secondary={
                <Chip
                  size="small"
                  label={
                    RELATION_LABELS[link.relationship_type] ||
                    link.relationship_type
                  }
                />
              }
            />
          </ListItem>
        ))}
      </MuiList>
    </Paper>
  );
}

export default List;