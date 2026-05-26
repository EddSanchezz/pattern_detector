import { useState, useCallback, useEffect, useMemo } from 'react';
import { Send } from 'lucide-react';
import { FormField } from './FormField';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';
import { validateField } from '../../services/api';
import { useDebounce } from '../../hooks/useDebounce';

const FORM_FIELDS = [
  { name: 'email', label: 'Correo electrónico', pattern: 'email', placeholder: 'ejemplo@correo.com' },
  { name: 'phone', label: 'Teléfono', pattern: 'phone', placeholder: '+57 300 123 4567' },
  { name: 'date', label: 'Fecha', pattern: 'date', placeholder: 'DD/MM/YYYY' },
  { name: 'url', label: 'URL', pattern: 'url', placeholder: 'https://ejemplo.com' },
  { name: 'plate', label: 'Placa de vehículo', pattern: 'plate', placeholder: 'ABC-1234' },
  { name: 'document_id', label: 'Documento ID', pattern: 'document_id', placeholder: 'CC123456789' },
  { name: 'password', label: 'Contraseña', pattern: 'password', placeholder: 'Min 8 caracteres, mayúscula, número, carácter especial' }
];

export function FormValidation() {
  const [values, setValues] = useState({
    email: '',
    phone: '',
    date: '',
    url: '',
    plate: '',
    document_id: '',
    password: ''
  });

  const [statuses, setStatuses] = useState({
    email: null,
    phone: null,
    date: null,
    url: null,
    plate: null,
    document_id: null,
    password: null
  });

  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  // Individual debounced values - each is independent and only changes when its value changes
  const debouncedEmail = useDebounce(values.email, 300);
  const debouncedPhone = useDebounce(values.phone, 300);
  const debouncedDate = useDebounce(values.date, 300);
  const debouncedUrl = useDebounce(values.url, 300);
  const debouncedPlate = useDebounce(values.plate, 300);
  const debouncedDocumentId = useDebounce(values.document_id, 300);
  const debouncedPassword = useDebounce(values.password, 300);

  const debouncedValues = useMemo(() => ({
    email: debouncedEmail,
    phone: debouncedPhone,
    date: debouncedDate,
    url: debouncedUrl,
    plate: debouncedPlate,
    document_id: debouncedDocumentId,
    password: debouncedPassword
  }), [debouncedEmail, debouncedPhone, debouncedDate, debouncedUrl, debouncedPlate, debouncedDocumentId, debouncedPassword]);

  const validateFieldAsync = useCallback(async (fieldName, fieldPattern, fieldValue) => {
    if (!fieldValue.trim()) {
      setStatuses((prev) => ({ ...prev, [fieldName]: null }));
      setErrors((prev) => { const { [fieldName]: _, ...rest } = prev; return rest; });
      return;
    }

    setStatuses((prev) => ({ ...prev, [fieldName]: 'loading' }));
    try {
      const result = await validateField(fieldPattern, fieldValue);
      if (result.valid) {
        setStatuses((prev) => ({ ...prev, [fieldName]: 'valid' }));
        setErrors((prev) => { const { [fieldName]: _, ...rest } = prev; return rest; });
      } else {
        setStatuses((prev) => ({ ...prev, [fieldName]: 'invalid' }));
        setErrors((prev) => ({ ...prev, [fieldName]: result.error || 'Formato inválido' }));
      }
    } catch (err) {
      setStatuses((prev) => ({ ...prev, [fieldName]: 'invalid' }));
      setErrors((prev) => ({ ...prev, [fieldName]: 'Error de validación' }));
    }
  }, []);

  // Effect to validate when any debounced value changes
  useEffect(() => {
    for (const field of FORM_FIELDS) {
      const debouncedValue = debouncedValues[field.name];
      if (debouncedValue && debouncedValue !== values[field.name]) {
        // Only validate if debounced value differs from current value (indicating user stopped typing)
        validateFieldAsync(field.name, field.pattern, debouncedValue);
      }
    }
  }, [debouncedValues, values, validateFieldAsync]);

  const handleChange = useCallback((fieldName, fieldValue) => {
    setValues((prev) => ({ ...prev, [fieldName]: fieldValue }));
  }, []);

  const isFormValid = Object.values(statuses).every(
    (status) => status === null || status === 'valid'
  ) && Object.values(statuses).some((status) => status !== null);

  const handleSubmit = () => {
    if (isFormValid) {
      setSubmitting(true);
      setTimeout(() => {
        setSubmitting(false);
        alert('Formulario enviado correctamente');
      }, 500);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-6 py-8">
      <Card>
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {FORM_FIELDS.map((field) => (
              <FormField
                key={field.name}
                label={field.label}
                value={values[field.name]}
                onChange={(value) => handleChange(field.name, value)}
                pattern={field.pattern}
                status={statuses[field.name]}
                error={errors[field.name]}
                placeholder={field.placeholder}
              />
            ))}
          </div>
          <div className="flex items-center gap-4 pt-4">
            <Button onClick={handleSubmit} disabled={!isFormValid || submitting}>
              <Send className="w-4 h-4" />
              {submitting ? 'Enviando...' : 'Enviar Formulario'}
            </Button>
            {!isFormValid && Object.values(statuses).some((s) => s !== null) && (
              <p className="text-sm text-warning">
                Completa todos los campos correctamente
              </p>
            )}
          </div>
        </div>
      </Card>
    </div>
  );
}