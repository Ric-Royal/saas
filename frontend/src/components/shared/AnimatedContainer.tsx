'use client';

import { ReactNode } from 'react';
import { motion, AnimatePresence, Variants } from 'framer-motion';
import { Box } from '@chakra-ui/react';
import { fadeIn, slideIn, scaleIn } from './animations';

interface AnimatedContainerProps {
  children: ReactNode;
  variant?: 'fade' | 'slide' | 'scale';
  delay?: number;
  duration?: number;
  className?: string;
}

export default function AnimatedContainer({
  children,
  variant = 'fade',
  delay = 0,
  duration,
  className,
}: AnimatedContainerProps) {
  const getVariant = (): Variants => {
    switch (variant) {
      case 'slide':
        return slideIn;
      case 'scale':
        return scaleIn;
      default:
        return fadeIn;
    }
  };

  const variants = getVariant();
  if (duration || delay) {
    const animate = variants.animate as { transition?: { duration?: number; delay?: number } };
    if (animate) {
      animate.transition = {
        ...animate.transition,
        duration: duration || animate.transition?.duration,
        delay,
      };
    }
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial="initial"
        animate="animate"
        exit="exit"
        variants={variants}
      >
        <Box className={className}>{children}</Box>
      </motion.div>
    </AnimatePresence>
  );
} 