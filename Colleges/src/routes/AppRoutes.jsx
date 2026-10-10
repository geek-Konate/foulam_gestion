import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import AppLayout from '../components/layout/AppLayout';
import Login from '../pages/auth/Login';
import Dashboard from '../pages/dashboard/Dashboard';
import AnneesScolaires from '../pages/annees_scolaires/AnneesScolaires';
import Niveaux from '../pages/niveaux/Niveaux';
import Classes from '../pages/classes/Classes';
import Eleves from '../pages/eleves/Eleves';
import Inscriptions from '../pages/inscriptions/Inscriptions';
import Responsables from '../pages/responsables/Responsables';
import EleveResponsables from '../pages/eleve_responsables/EleveResponsables';
import Matieres from '../pages/matieres/Matieres';
import Maquettes from '../pages/maquettes/Maquettes';
import MaquetteMatieres from '../pages/maquette_matieres/MaquetteMatieres';
import Affectations from '../pages/affectations/Affectations';
import Evaluations from '../pages/evaluations/Evaluations';
import Notes from '../pages/notes/Notes';
import Presences from '../pages/presences/Presences';
import Bulletins from '../pages/bulletins/Bulletins';
import FraisTypes from '../pages/frais_types/FraisTypes';
import Paiements from '../pages/paiements/Paiements';
import Recus from '../pages/recus/Recus';
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
            <Route path="/levels" element={<Niveaux />} />
            <Route path="/classes" element={<Classes />} />
            <Route path="/students" element={<Eleves />} />
            <Route path="/enrollments" element={<Inscriptions />} />
            <Route path="/guardians" element={<Responsables />} />
            <Route path="/student-guardians" element={<EleveResponsables />} />
            <Route path="/subjects" element={<Matieres />} />
            <Route path="/curriculums" element={<Maquettes />} />
            <Route path="/curriculum-subjects" element={<MaquetteMatieres />} />
            <Route path="/teacher-assignments" element={<Affectations />} />
            <Route path="/evaluations" element={<Evaluations />} />
            <Route path="/grades" element={<Notes />} />
            <Route path="/attendance" element={<Presences />} />
            <Route path="/report-cards" element={<Bulletins />} />
            <Route path="/fee-types" element={<FraisTypes />} />
            <Route path="/payments" element={<Paiements />} />
            <Route path="/receipts" element={<Recus />} />
          </Route>
        </Route>

        {/* Route par défaut */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default AppRoutes;
