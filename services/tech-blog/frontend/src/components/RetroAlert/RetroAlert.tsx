import React, { useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaExclamationTriangle, FaWindowClose } from 'react-icons/fa';

interface RetroAlertProps {
  message: string;
  onClose: () => void;
  autoClose?: boolean;
  duration?: number;
}

export function RetroAlert({
  message,
  onClose,
  autoClose = true,
  duration = 3000
}: RetroAlertProps) {
  useEffect(() => {
    if (autoClose) {
      const timer = setTimeout(onClose, duration);
      return () => clearTimeout(timer);
    }
  }, [autoClose, duration, onClose]);

  return (
    <AnimatePresence>
      <motion.div
        className="retro-alert"
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: 50 }}
        transition={{
          type: 'spring',
          stiffness: 500,
          damping: 30
        }}
      >
        <div className="retro-alert-title">
          <FaExclamationTriangle className="alert-icon" />
          <span>ALERT.exe</span>
          <button onClick={onClose} className="close-button">
            <FaWindowClose />
          </button>
        </div>
        <div className="retro-alert-content">
          <pre className="alert-message">{message}</pre>
          <button onClick={onClose} className="retro-button">
            OK
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  );
} 