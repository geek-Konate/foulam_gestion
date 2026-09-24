import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import AppLayout from '../components/layout/AppLayout';
import Login from '../pages/auth/Login';
import Dashboard from '../pages/dashboard/Dashboard';
import AnneesScolaires from '../pages/annees_scolaires/AnneesScolaires';
import ProtectedRoute from './ProtectedRoute';

function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Routes publiques */}
        <Route path="/login" element={<Login />} />

        {/* Routes protégées */}
        <Route element={<ProtectedRoute />}>
          <Route element={<AppLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/academic-years" element={<AnneesScolaires />} />
          </Route>
        </Route>

        {/* Route par défaut */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
