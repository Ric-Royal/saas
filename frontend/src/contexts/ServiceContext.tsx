'use client';

import { createContext, useContext, ReactNode } from 'react';

interface ServiceConfig {
  name: string;
  apiUrl: string;
  description: string;
}

interface ServiceContextType {
  services: {
    agriInsights: ServiceConfig;
    publicParticipation: ServiceConfig;
    civilBot: ServiceConfig;
    techBlog: ServiceConfig;
  };
}

const serviceConfigs: ServiceContextType = {
  services: {
    agriInsights: {
      name: 'Agri Insights',
      apiUrl: '/api/agri',
      description: 'Agricultural market insights and analytics',
    },
    publicParticipation: {
      name: 'Public Participation',
      apiUrl: '/api/participation',
      description: 'Public participation in governance',
    },
    civilBot: {
      name: 'Civil Bot',
      apiUrl: '/api/civilbot',
      description: 'Civil service chatbot assistant',
    },
    techBlog: {
      name: 'Tech Blog',
      apiUrl: '/blog',
      description: 'Technology blog and articles',
    },
  },
};

const ServiceContext = createContext<ServiceContextType>(serviceConfigs);

export function useServiceConfig() {
  return useContext(ServiceContext);
}

interface ServiceProviderProps {
  children: ReactNode;
}

export function ServiceProvider({ children }: ServiceProviderProps) {
  return (
    <ServiceContext.Provider value={serviceConfigs}>
      {children}
    </ServiceContext.Provider>
  );
} 