import React from 'react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { FaWindowClose } from 'react-icons/fa';

interface MenuItem {
  label: string;
  href?: string;
  onClick?: () => void;
}

interface RetroMenuProps {
  isOpen: boolean;
  onClose: () => void;
  items: MenuItem[];
}

export function RetroMenu({ isOpen, onClose, items }: RetroMenuProps) {
  const menuVariants = {
    closed: {
      opacity: 0,
      x: '100%',
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 30
      }
    },
    open: {
      opacity: 1,
      x: 0,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 30
      }
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="retro-modal-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            className="retro-modal"
            variants={menuVariants}
            initial="closed"
            animate="open"
            exit="closed"
          >
            <div className="retro-modal-title">
              <span>Menu.exe</span>
              <button onClick={onClose} className="close-button">
                <FaWindowClose />
              </button>
            </div>
            <div className="retro-modal-content">
              {items.map((item, index) => (
                <div key={index} className="menu-item">
                  {item.href ? (
                    <Link href={item.href} onClick={onClose} className="glitch-effect">
                      {item.label}
                    </Link>
                  ) : (
                    <button onClick={() => {
                      item.onClick?.();
                      onClose();
                    }} className="glitch-effect">
                      {item.label}
                    </button>
                  )}
                </div>
              ))}
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
} 