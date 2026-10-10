import { useCallback, useEffect, useMemo, useState } from 'react';

import { Add, Refresh } from '@mui/icons-material';
import {
  Alert, Box, Button, CircularProgress, FormControl, InputLabel, MenuItem, Select, Typography,
} from '@mui/material';

import Form from '../../components/affectations/Form';
import List from '../../components/affectations/List';
import { useAffectations } from '../../hooks/useAffectations';
import { useAuth } from '../../hooks/useAuth';
import { useClasses } from '../../hooks/useClasses';
import { useMatieres } from '../../hooks/useMatieres';
import { useAnneesScolaires } from '../../hooks/useAnneesScolaires';
import { CurriculumsAPI, CurriculumSubjectsAPI, UsersAPI } from '../../services/api';

function Affectations() {
  const { activeEstablishmentId } = useAuth();
  const { classes } = useClasses(activeEstablishmentId);
  const { matieres } = useMatieres();
  const { annees } = useAnneesScolaires(activeEstablishmentId);

  const [classId, setClassId] = useState('');
  const [curriculumSubjects, setCurriculumSubjects] = useState([]);
  const [curriculumSubjectsLoading, setCurriculumSubjectsLoading] = useState(false);
  const [users, setUsers] = useState([]);

  const { affectations, loading, saving, error, refresh, assignTeacher, removeAffectation } =
    useAffectations(activeEstablishmentId, classId);

  const [formOpen, setFormOpen] = useState(false);

  // Récupère le level_id de la classe sélectionnée
  const selectedClasse = useMemo(
    () => classes.find((c) => c.id === classId),
    [classes, classId]
  );

  // Charge les matières de la maquette associée au niveau de la classe
  // (1 maquette par niveau pour l'année courante)
  useEffect(() => {
    (async () => {
      if (!activeEstablishmentId || !selectedClasse || annees.length === 0) {
        setCurriculumSubjects([]);
        return;
      }

      // Récupérer l'année active (ou la première)
      const anneeActive = annees.find((a) => a.status === 'active') || annees[0];
      if (!anneeActive) {
        setCurriculumSubjects([]);
        return;
      }

      const levelId = selectedClasse.level_id;

      setCurriculumSubjectsLoading(true);

      try {
        // Chercher toutes les maquettes de l'établissement
        const res = await CurriculumsAPI.getAll(activeEstablishmentId);
        const curriculums = res.data || [];

        // Trouver la maquette correspondant au niveau + année active
        const maquette = curriculums.find(
          (m) => m.level_id === levelId && m.academic_year_id === anneeActive.id
        );

        if (!maquette) {
          setCurriculumSubjects([]);
          return;
        }

        // Lister les matières de cette maquette
        const resSubjects = await CurriculumSubjectsAPI.listCurriculumSubjects(
          activeEstablishmentId,
          maquette.id
        );
        setCurriculumSubjects(resSubjects.data || []);
      } catch {
        setCurriculumSubjects([]);
      } finally {
        setCurriculumSubjectsLoading(false);
      }
    })();
  }, [activeEstablishmentId, selectedClasse, annees]);

  // Charge les utilisateurs de l'établissement
  useEffect(() => {
    (async () => {
      if (!activeEstablishmentId) {
        setUsers([]);
        return;
      }
      try {
        const res = await UsersAPI.getAll(activeEstablishmentId);
        setUsers(res.data || []);
      } catch {
        setUsers([]);
      }
    })();
  }, [activeEstablishmentId]);

  const handleSave = async (csId, userId) => {
    try {
      await assignTeacher(csId, userId);
      setFormOpen(false);
    } catch {
      /* L'erreur est déjà exposée par le hook */
    }
  };

  const handleRemove = async (assignmentId) => {
    try {
      await removeAffectation(assignmentId);
    } catch {
      /* L'erreur est déjà exposée par le hook */
    }
  };

  const noMaquette = selectedClasse && !curriculumSubjectsLoading && curriculumSubjects.length === 0;

  return (
    <Box>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight={700} gutterBottom>
          Affectations enseignants
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Affectez un enseignant à une matière dans une classe.
        </Typography>
      </Box>

      {!activeEstablishmentId && (
        <Alert severity="info" sx={{ mb: 3 }}>Aucun établissement sélectionné.</Alert>
      )}
      {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

      <Box sx={{ display: 'flex', gap: 2, mb: 3, alignItems: 'center' }}>
        <FormControl sx={{ minWidth: 280 }}>
          <InputLabel>Classe</InputLabel>
          <Select label="Classe" value={classId} onChange={(e) => setClassId(e.target.value)}>
            {classes.map((c) => (
              <MenuItem key={c.id} value={c.id}>
                {c.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <Button variant="outlined" startIcon={<Refresh />} onClick={refresh}>
          Actualiser
        </Button>

        <Button
          variant="contained"
          startIcon={<Add />}
          disabled={!classId || noMaquette}
          onClick={() => setFormOpen(true)}
        >
          Affecter
        </Button>
      </Box>

      {noMaquette && (
        <Alert severity="info" sx={{ mb: 3 }}>
          Aucune maquette trouvée pour le niveau de cette classe. Créez d'abord une
          maquette pour ce niveau (et cette année) avant d'affecter des enseignants.
        </Alert>
      )}

      {classId ? (
        <>
          {curriculumSubjectsLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 4 }}>
              <CircularProgress />
            </Box>
          )}

          {!curriculumSubjectsLoading && (
            <List
              affectations={affectations}
              matieres={matieres}
              curriculumSubjects={curriculumSubjects}
              users={users}
              loading={loading}
              onRemove={handleRemove}
            />
          )}
        </>
      ) : (
        <Alert severity="info">Sélectionnez une classe pour voir ses affectations.</Alert>
      )}

      <Form
        open={formOpen}
        curriculumSubjects={curriculumSubjects}
        matieres={matieres}
        users={users}
        savings={saving}
        onClose={() => setFormOpen(false)}
        onSave={handleSave}
      />
    </Box>
  );
}

export default Affectations;