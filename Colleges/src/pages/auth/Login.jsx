import { Alert, Box, Button, CircularProgress, Paper, TextField, Typography } from '@mui/material';
import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { useAuth } from '../../hooks/useAuth';

function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [form, setForm] = useState({
    email: '',
    password: '',
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    setError('');
    setLoading(true);

    try {
      await login(form.email, form.password);

      const destination = location.state?.from?.pathname || '/dashboard';

      navigate(destination, { replace: true });
    } catch (error) {
      const message = error.response?.data?.detail || 'Email ou mot de passe incorrect.';

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        px: 2,
      }}
    >
      <Paper
        elevation={3}
        sx={{
          width: '100%',
          maxWidth: 420,
          p: 4,
          borderRadius: 3,
        }}
      >
        <Box sx={{ mb: 4, textAlign: 'center' }}>
          <Typography variant="h4" fontWeight={700} gutterBottom>
            Connexion
          </Typography>

          <Typography variant="body2" color="text.secondary">
            Connectez-vous à votre espace
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit}>
          <TextField
            fullWidth
            required
            label="Adresse email"
            name="email"
            type="email"
            value={form.email}
            onChange={handleChange}
            autoComplete="email"
            sx={{ mb: 2 }}
          />

          <TextField
            fullWidth
            required
            label="Mot de passe"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            autoComplete="current-password"
            sx={{ mb: 3 }}
          />

          <Button fullWidth type="submit" variant="contained" size="large" disabled={loading}>
            {loading ? <CircularProgress size={24} color="inherit" /> : 'Se connecter'}
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}

export default Login;
