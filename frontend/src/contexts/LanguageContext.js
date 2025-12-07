import React, { createContext, useContext, useState, useEffect } from 'react';

const translations = {
  en: {
    // Header
    appTitle: 'TalkGuest Data Processing',
    appSubtitle: '',
    
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
    processDataFirst: 'Process data first',
    
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
    nightsOverTime: 'Nights',
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
    personNightsByProperty: 'Person-Nights by Property',
    netVsCommissions: 'Net Revenue vs Commissions by Property',
    ivaByRegion: 'IVA/VAT by Region',
    exportReports: 'Export Reports',
    exportDescription: 'Download detailed Excel reports with full calculations and breakdowns.',
    downloadRevenueReport: 'Download Revenue Report',
    invoiceDataAvailable: 'Invoice Data Available',
    invoiceDataDescription: 'Compare reservation data with invoice records',
    showingInvoiceData: 'Showing Invoice Data',
    showInvoiceComparison: 'Show Invoice Comparison',
    invoiceSummary: 'Invoice Summary',
    invoiceGross: 'Invoice Gross',
    invoiceIVA: 'Invoice IVA',
    invoiceNet: 'Invoice Net',
    totalInvoices: 'Total Invoices',
    
    // Errors
    uploadFailed: 'Upload failed',
    processingFailed: 'Processing failed',
    processingCompleted: 'Processing completed successfully',
    noResultsAvailable: 'No results available. Please run processing first.',
    FILE_SWAP_GUESTS_HAS_RESERVATIONS: 'This looks like a reservations file. Did you mean to upload it to the Reservations field instead?',
    FILE_SWAP_RESERVATIONS_HAS_GUESTS: 'This looks like a guests file. Did you mean to upload it to the Guests List field instead?',
    
    // Language
    language: 'Language',
    english: 'English',
    portuguese: 'Português',
    navigateToTabs: 'Navigate to the Occupancy and Revenue tabs for detailed visualizations'
  },
  pt: {
    // Header
    appTitle: 'Processamento de Dados da TalkGuest',
    appSubtitle: '',
    
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
    processDataFirst: 'Processe os dados primeiro',
    
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
    nightsOverTime: 'Noites',
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
    personNightsByProperty: 'Pessoa-Noites por Propriedade',
    netVsCommissions: 'Receita Líquida vs Comissões por Propriedade',
    ivaByRegion: 'IVA por Região',
    exportReports: 'Exportar Relatórios',
    exportDescription: 'Descarregue relatórios Excel detalhados com cálculos e discriminações completas.',
    downloadRevenueReport: 'Descarregar Relatório de Receitas',
    invoiceDataAvailable: 'Dados de Faturas Disponíveis',
    invoiceDataDescription: 'Compare os dados de reservas com os registos de faturas',
    showingInvoiceData: 'A Mostrar Dados de Faturas',
    showInvoiceComparison: 'Mostrar Comparação de Faturas',
    invoiceSummary: 'Resumo de Faturas',
    invoiceGross: 'Fatura Bruta',
    invoiceIVA: 'IVA da Fatura',
    invoiceNet: 'Fatura Líquida',
    totalInvoices: 'Total de Faturas',
    
    // Errors
    uploadFailed: 'Falha no carregamento',
    processingFailed: 'Falha no processamento',
    processingCompleted: 'Processamento concluído com sucesso',
    noResultsAvailable: 'Sem resultados disponíveis. Por favor execute o processamento primeiro.',
    FILE_SWAP_GUESTS_HAS_RESERVATIONS: 'Este parece ser um ficheiro de reservas. Será que queria carregá-lo no campo de Reservas?',
    FILE_SWAP_RESERVATIONS_HAS_GUESTS: 'Este parece ser um ficheiro de hóspedes. Será que queria carregá-lo no campo de Lista de Hóspedes?',
    
    // Language
    language: 'Idioma',
    english: 'English',
    portuguese: 'Português',
    navigateToTabs: 'Navegue para os separadores Ocupação e Receitas para visualizações detalhadas'
  }
};

const LanguageContext = createContext();

export function LanguageProvider({ children }) {
  const [language, setLanguage] = useState(() => {
    // Check localStorage for saved preference
    const saved = localStorage.getItem('talkguest-language');
    return saved || 'pt';  // Default to Portuguese
  });

  useEffect(() => {
    localStorage.setItem('talkguest-language', language);
  }, [language]);

  const t = (key) => {
    // Use hasOwnProperty to properly handle empty strings
    if (translations[language].hasOwnProperty(key)) {
      return translations[language][key];
    }
    if (translations.en.hasOwnProperty(key)) {
      return translations.en[key];
    }
    return key;
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
