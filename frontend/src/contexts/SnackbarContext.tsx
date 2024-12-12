import { createContext, useContext, useState, useCallback } from 'react';
import { Alert, Snackbar, AlertColor } from '@mui/material';

interface SnackbarMessage {
  message: string;
  severity: AlertColor;
  autoHideDuration?: number;
}

interface SnackbarContextType {
  showMessage: (message: string, severity?: AlertColor, duration?: number) => void;
  showError: (message: string, duration?: number) => void;
  showSuccess: (message: string, duration?: number) => void;
  showWarning: (message: string, duration?: number) => void;
  showInfo: (message: string, duration?: number) => void;
}

const SnackbarContext = createContext<SnackbarContextType | undefined>(undefined);

export function SnackbarProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState<SnackbarMessage | null>(null);

  const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  const showMessage = useCallback(
    (message: string, severity: AlertColor = 'info', duration: number = 6000) => {
      setMessage({ message, severity, autoHideDuration: duration });
      setOpen(true);
    },
    []
  );

  const showError = useCallback(
    (message: string, duration?: number) => {
      showMessage(message, 'error', duration);
    },
    [showMessage]
  );

  const showSuccess = useCallback(
    (message: string, duration?: number) => {
      showMessage(message, 'success', duration);
    },
    [showMessage]
  );

  const showWarning = useCallback(
    (message: string, duration?: number) => {
      showMessage(message, 'warning', duration);
    },
    [showMessage]
  );

  const showInfo = useCallback(
    (message: string, duration?: number) => {
      showMessage(message, 'info', duration);
    },
    [showMessage]
  );

  return (
    <SnackbarContext.Provider
      value={{
        showMessage,
        showError,
        showSuccess,
        showWarning,
        showInfo,
      }}
    >
      {children}
      <Snackbar
        open={open}
        autoHideDuration={message?.autoHideDuration}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert
          onClose={handleClose}
          severity={message?.severity}
          variant="filled"
          sx={{ width: '100%' }}
        >
          {message?.message}
        </Alert>
      </Snackbar>
    </SnackbarContext.Provider>
  );
}

export function useSnackbar() {
  const context = useContext(SnackbarContext);
  if (context === undefined) {
    throw new Error('useSnackbar must be used within a SnackbarProvider');
  }
  return context;
} 