import { Alert, Box, CircularProgress, Grid, Paper, Typography } from '@mui/material';

import { useDashboard } from '../../hooks/useDashboard';

function StatCard({ title, value }) {
  return (
    <Paper
      sx={{
        p: 3,
        height: '100%',
        borderRadius: 2,
      }}
    >
      <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
        {title}
      </Typography>

      <Typography variant="h4" fontWeight={700}>
        {value}
      </Typography>
    </Paper>
  );
}

function Dashboard() {
  const { data, loading, error } = useDashboard();

  if (loading) {
    return (
      <Box
        sx={{
          minHeight: 300,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }}
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!data) {
    return <Alert severity="info">Aucune donnée disponible pour le tableau de bord.</Alert>;
  }

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Tableau de bord
        </Typography>

        <Typography variant="body1" color="text.secondary">
          Vue générale de votre établissement.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <StatCard title="Élèves" value={data.students_count} />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <StatCard title="Classes" value={data.classes_count} />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <StatCard title="Enseignants" value={data.teachers_count} />
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <StatCard title="Total payé" value={`${data.total_paid} FCFA`} />
        </Grid>
      </Grid>

      <Paper
        sx={{
          mt: 3,
          p: 3,
          borderRadius: 2,
        }}
      >
        <Typography variant="h6" fontWeight={600} gutterBottom>
          Année scolaire active
        </Typography>

        <Typography color="text.secondary">
          {data.academic_year_name || 'Aucune année scolaire active'}
        </Typography>
      </Paper>
    </Box>
  );
}

export default Dashboard;
