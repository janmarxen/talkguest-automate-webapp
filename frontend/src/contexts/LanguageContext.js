import React, { createContext, useContext, useState, useEffect } from 'react';

const translations = {
  en: {
    // Header
    appTitle: 'TalkGuest Analytics',
    appSubtitle: 'Hospitality Data Processing',
    
    // Tabs
    tabUpload: 'Upload & Process',
    tabOccupancy: 'Occupancy',
    tabRevenue: 'Revenue',
    
    // Upload Tab
    uploadTitle: 'Upload Data Files',
    clearAll: 'Clear All',
    guestsList: 'Guests List',
    reservations: 'Reservations',
    invoicesOptional: 'Invoices (Optional)',
    requiredFiles: '* Required files. Accepts Excel files (.xlsx, .xls)',
    remove: 'Remove',
    uploading: 'Uploading...',
    dragDrop: 'Drag & drop an Excel file here',
    orClickBrowse: 'or click to browse',
    rows: 'rows',
    columns: 'columns',
    
    // Processing
    readyToProcess: 'Ready to Process',
    processData: 'Process Data',
    processing: 'Processing...',
    uploadRequired: 'Please upload guests and reservations files to proceed',
    
    // Results
    resultsSummary: 'Results Summary',
    occupancyReport: 'Occupancy Report',
    revenueReport: 'Revenue Report',
    downloadAll: 'Download All',
    occupancyOverview: 'Occupancy Overview',
    revenueOverview: 'Revenue Overview',
    totalGuests: 'Total Guests',
    totalNights: 'Total Nights',
    totalReservations: 'Reservations',
    grossRevenue: 'Gross Revenue',
    netRevenue: 'Net Revenue',
    totalCommissions: 'Total Commissions',
    totalIVA: 'Total IVA',
    
    // Occupancy Tab
    occupancyDashboard: 'Occupancy Dashboard',
    selectProperty: 'Select Property',
    allProperties: 'All Properties',
    byNationality: 'By Nationality',
    guestDistribution: 'Guest Distribution',
    nightsOverTime: 'Nights Over Time',
    detailedData: 'Detailed Data',
    nationality: 'Nationality',
    uniqueGuests: 'Unique Guests',
    totalPeople: 'Total People',
    personNights: 'Person-Nights',
    
    // Revenue Tab
    revenueDashboard: 'Revenue Dashboard',
    revenueByProperty: 'Revenue by Property',
    revenueBreakdown: 'Revenue Breakdown',
    monthlyRevenue: 'Monthly Revenue',
    property: 'Property',
    grossValue: 'Gross Value',
    commission: 'Commission',
    ivaAmount: 'IVA Amount',
    netValue: 'Net Value',
    
    // Charts
    noDataAvailable: 'No data available',
    
    // Errors
    uploadFailed: 'Upload failed',
    processingFailed: 'Processing failed',
    processingCompleted: 'Processing completed successfully',
    noResultsAvailable: 'No results available. Please run processing first.',
    
    // Language
    language: 'Language',
    english: 'English',
    portuguese: 'Português'
  },
  pt: {
    // Header
    appTitle: 'TalkGuest Analytics',
    appSubtitle: 'Processamento de Dados de Hotelaria',
    
    // Tabs
    tabUpload: 'Carregar e Processar',
    tabOccupancy: 'Ocupação',
    tabRevenue: 'Receitas',
    
    // Upload Tab
    uploadTitle: 'Carregar Ficheiros de Dados',
    clearAll: 'Limpar Tudo',
    guestsList: 'Lista de Hóspedes',
    reservations: 'Reservas',
    invoicesOptional: 'Faturas (Opcional)',
    requiredFiles: '* Ficheiros obrigatórios. Aceita ficheiros Excel (.xlsx, .xls)',
    remove: 'Remover',
    uploading: 'A carregar...',
    dragDrop: 'Arraste e solte um ficheiro Excel aqui',
    orClickBrowse: 'ou clique para procurar',
    rows: 'linhas',
    columns: 'colunas',
    
    // Processing
    readyToProcess: 'Pronto para Processar',
    processData: 'Processar Dados',
    processing: 'A processar...',
    uploadRequired: 'Por favor carregue os ficheiros de hóspedes e reservas para continuar',
    
    // Results
    resultsSummary: 'Resumo dos Resultados',
    occupancyReport: 'Relatório de Ocupação',
    revenueReport: 'Relatório de Receitas',
    downloadAll: 'Descarregar Tudo',
    occupancyOverview: 'Visão Geral de Ocupação',
    revenueOverview: 'Visão Geral de Receitas',
    totalGuests: 'Total de Hóspedes',
    totalNights: 'Total de Noites',
    totalReservations: 'Reservas',
    grossRevenue: 'Receita Bruta',
    netRevenue: 'Receita Líquida',
    totalCommissions: 'Total de Comissões',
    totalIVA: 'Total de IVA',
    
    // Occupancy Tab
    occupancyDashboard: 'Painel de Ocupação',
    selectProperty: 'Selecionar Propriedade',
    allProperties: 'Todas as Propriedades',
    byNationality: 'Por Nacionalidade',
    guestDistribution: 'Distribuição de Hóspedes',
    nightsOverTime: 'Noites ao Longo do Tempo',
    detailedData: 'Dados Detalhados',
    nationality: 'Nacionalidade',
    uniqueGuests: 'Hóspedes Únicos',
    totalPeople: 'Total de Pessoas',
    personNights: 'Pessoa-Noites',
    
    // Revenue Tab
    revenueDashboard: 'Painel de Receitas',
    revenueByProperty: 'Receitas por Propriedade',
    revenueBreakdown: 'Discriminação de Receitas',
    monthlyRevenue: 'Receitas Mensais',
    property: 'Propriedade',
    grossValue: 'Valor Bruto',
    commission: 'Comissão',
    ivaAmount: 'Valor do IVA',
    netValue: 'Valor Líquido',
    
    // Charts
    noDataAvailable: 'Sem dados disponíveis',
    
    // Errors
    uploadFailed: 'Falha no carregamento',
    processingFailed: 'Falha no processamento',
    processingCompleted: 'Processamento concluído com sucesso',
    noResultsAvailable: 'Sem resultados disponíveis. Por favor execute o processamento primeiro.',
    
    // Language
    language: 'Idioma',
    english: 'English',
    portuguese: 'Português'
  }
};

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(() => {
    // Check localStorage for saved preference
    const saved = localStorage.getItem('talkguest-language');
    return saved || 'en';
  });

  useEffect(() => {
    localStorage.setItem('talkguest-language', language);
  }, [language]);

  const t = (key) => {
    return translations[language][key] || translations.en[key] || key;
  };

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'en' ? 'pt' : 'en');
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}

export default LanguageContext;
