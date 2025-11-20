/**
 * Simple i18n Translation System
 * Supports 5 languages: English, Spanish, French, German, Chinese, Japanese
 *
 * Usage:
 * 1. Add data-i18n="key" to HTML elements
 * 2. Call setLanguage('en') to change language
 * 3. Language preference is stored in localStorage per user
 */

const translations = {
    en: {
        // Navigation
        'nav.dashboard': 'Dashboard',
        'nav.about': 'About Us',
        'nav.indices': 'Indices',
        'nav.news': 'News',
        'nav.trading': 'Trading',
        'nav.language': 'Language',
        'nav.logout': 'Logout',

        // Onboarding Modal
        'onboarding.title.language': 'Select Your Language',
        'onboarding.subtitle.language': 'Choose your preferred language for the dashboard',
        'onboarding.button.continue': 'Continue',
        'onboarding.title.disclaimer': 'Important Disclaimer',
        'onboarding.disclaimer.heading': 'Risk Warning',
        'onboarding.disclaimer.text': 'Trading Futures, Forex, CFDs and Stocks involves a risk of loss. Please consider carefully if such trading is appropriate for you. Past performance is not indicative of future results. Any and all signals or educational advice provided by PhoenixBinary and/or Phoenix Algo, LLC and/or any indicators provided by aforementioned are for educational purposes only and do not constitute investment recommendations or advice.',
        'onboarding.disclaimer.checkbox': 'I understand and acknowledge the risks associated with trading',

        // Legal Notice
        'legal.title': 'Risk Warning',
        'legal.text': 'Trading Futures, Forex, CFDs and Stocks involves a risk of loss. Please consider carefully if such trading is appropriate for you. Past performance is not indicative of future results. Any and all signals or educational advice provided by PhoenixBinary and/or Phoenix Algo, LLC and/or any indicators provided by aforementioned are for educational purposes only and do not constitute investment recommendations or advice.',

        // About Page
        'about.page.title': 'About the NASDAQ Sentiment Tracker',
        'about.section1.title': 'What is the NASDAQ Sentiment Tracker?',
        'about.section1.text1': 'The NASDAQ Sentiment Tracker is a real-time dashboard that helps you understand how the market "feels" about the NASDAQ stock exchange. Instead of just looking at prices going up or down, we analyze multiple sources of information to give you a complete picture of market sentiment.',
        'about.section1.text2': 'Think of it as taking the temperature of the market. Our tool processes news articles, social media discussions, technical indicators, analyst recommendations, and market breadth data to create a single, easy-to-understand score that tells you whether the overall mood is positive, negative, or neutral.',
        'about.section2.title': 'Understanding the Sentiment Score',
        'about.section2.text1': 'The Sentiment Score is the heart of our dashboard. It\'s a number between -100 and +100 that represents the overall market sentiment:',
        'about.section2.bullish': 'BULLISH',
        'about.section2.bullish.text': 'Positive market sentiment',
        'about.section2.neutral': 'NEUTRAL',
        'about.section2.neutral.text': 'Mixed or balanced sentiment',
        'about.section2.bearish': 'BEARISH',
        'about.section2.bearish.text': 'Negative market sentiment',
        'about.section2.important': 'Important:',
        'about.section2.important.text': 'The score updates automatically during market hours (9:30 AM - 4:00 PM ET) and reflects real-time changes in market sentiment as new data comes in.',
        'about.section3.title': 'How We Calculate the Score',
        'about.section3.text1': 'Our Sentiment Score combines five key "drivers" of market sentiment. Each driver is analyzed independently and then weighted to create the final score:',
        'about.section3.driver1': '<strong>News Sentiment (40%)</strong> - We analyze financial news from major sources to determine if headlines are positive, negative, or neutral about the NASDAQ.',
        'about.section3.driver2': '<strong>Social Media (30%)</strong> - We monitor discussions on platforms like Twitter and Reddit to gauge retail investor sentiment and trending topics.',
        'about.section3.driver3': '<strong>Technical Indicators (30%)</strong> - We examine price movements, trading volumes, and technical patterns that professional traders watch.',
        'about.section3.driver4': '<strong>Analyst Recommendations</strong> - We track upgrades, downgrades, and target price changes from financial analysts.',
        'about.section3.driver5': '<strong>Market Breadth</strong> - We measure how many stocks are rising versus falling to understand overall market strength.',
        'about.section3.text2': 'These drivers work together to give you a comprehensive view that goes beyond just price movements.',
        'about.section4.title': 'How to Use This Tool',
        'about.section4.item1': '<strong>Check the Sentiment Score</strong> - Start with the main sentiment score (left side of the dashboard) to get an instant read on market mood.',
        'about.section4.item2': '<strong>Review Sentiment Drivers</strong> - Look at the individual drivers to see what\'s influencing the overall score. Are all drivers aligned, or are some positive while others are negative?',
        'about.section4.item3': '<strong>Examine the Historical Trend</strong> - Use the chart at the bottom to see how sentiment has changed over the past few hours. Is it improving or deteriorating?',
        'about.section4.item4': '<strong>Adjust Timeframes</strong> - Click the timeframe buttons (1m, 5m, 15m, 30m, 1h) to see sentiment trends over different time periods.',
        'about.section4.item5': '<strong>Use Any Timezone</strong> - Click the time display in the top right to switch between different timezones for your convenience.',
        'about.section4.protip': 'Pro Tip:',
        'about.section4.protip.text': 'This tool is most useful when combined with other research. Use it to confirm your trading ideas, spot sentiment shifts, or identify when the market mood might be changing direction.',
        'about.section5.title': 'Important Disclaimer',
        'about.section5.text1': 'This tool provides market sentiment analysis for informational purposes only. It is <strong>not</strong> financial advice, and should not be your only source of information when making investment decisions.',
        'about.section5.text2': 'Market sentiment can change rapidly, and past sentiment does not predict future market movements. Always do your own research, consult with financial professionals, and consider your personal financial situation before making any investment decisions.',

        // News Page
        'news.title': 'Latest News Feed',
        'news.filter.all': 'All',
        'news.filter.most-impactful': 'Most Impactful',
        'news.stat.total': 'Total Articles',
        'news.loading': 'Loading news articles...',
        'news.no-articles': 'No news articles found',
        'news.no-articles.subtitle': 'Check back later for the latest NASDAQ news',
        'news.article.read-more': 'Read full article →',

        // Dashboard
        'dashboard.score.label': 'Sentiment Score',
        'dashboard.drivers.title': 'Sentiment Drivers',
        'dashboard.driver.indicators': 'Indicators',
        'dashboard.driver.social': 'Social Media',
        'dashboard.driver.news': 'News',
        'dashboard.driver.recommendations': 'Recommendations',
        'dashboard.driver.breadth': 'Market Breadth',
        'dashboard.driver.vix': 'VIX',
        'dashboard.chart.title': 'NASDAQ',
        'dashboard.chart.timeframe.1m': '1 min',
        'dashboard.chart.timeframe.5m': '5 min',
        'dashboard.chart.timeframe.15m': '15 min',
        'dashboard.chart.timeframe.30m': '30 min',
        'dashboard.chart.timeframe.1h': '1 hr',
        'dashboard.chart.timeframe.2h': '2 hrs',
        'dashboard.chart.timeframe.4h': '4 hrs',
        'dashboard.chart.timeframe.6h': 'Session',
        'dashboard.chart.timeframe.2d': '2 days',
        'dashboard.chart.timeframe.3d': '3 days',
        'dashboard.status.bullish': 'BULLISH',
        'dashboard.status.neutral': 'NEUTRAL',
        'dashboard.status.bearish': 'BEARISH',

        // Common
        'common.app-name': 'NASDAQ Sentiment Tracker',
        'common.app-name-short': 'NASDAQ',
        'common.app-name-subtitle': 'Sentiment Tracker',
    },

    es: {
        // Navigation
        'nav.dashboard': 'Panel',
        'nav.about': 'Acerca de',
        'nav.indices': 'Índices',
        'nav.news': 'Noticias',
        'nav.trading': 'Trading',
        'nav.language': 'Idioma',
        'nav.logout': 'Cerrar sesión',

        // Onboarding Modal
        'onboarding.title.language': 'Selecciona tu idioma',
        'onboarding.subtitle.language': 'Elige tu idioma preferido para el panel',
        'onboarding.button.continue': 'Continuar',
        'onboarding.title.disclaimer': 'Aviso importante',
        'onboarding.disclaimer.heading': 'Advertencia de riesgo',
        'onboarding.disclaimer.text': 'El comercio de futuros, Forex, CFDs y acciones implica un riesgo de pérdida. Considere cuidadosamente si dicho comercio es apropiado para usted. El rendimiento pasado no es indicativo de resultados futuros. Todas las señales o consejos educativos proporcionados por PhoenixBinary y/o Phoenix Algo, LLC y/o cualquier indicador proporcionado por los mencionados son solo para fines educativos y no constituyen recomendaciones o consejos de inversión.',
        'onboarding.disclaimer.checkbox': 'Entiendo y reconozco los riesgos asociados con el comercio',

        // Legal Notice
        'legal.title': 'Advertencia de riesgo',
        'legal.text': 'El comercio de futuros, Forex, CFDs y acciones implica un riesgo de pérdida. Considere cuidadosamente si dicho comercio es apropiado para usted. El rendimiento pasado no es indicativo de resultados futuros. Todas las señales o consejos educativos proporcionados por PhoenixBinary y/o Phoenix Algo, LLC y/o cualquier indicador proporcionado por los mencionados son solo para fines educativos y no constituyen recomendaciones o consejos de inversión.',

        // About Page
        'about.page.title': 'Acerca del Rastreador de Sentimiento NASDAQ',
        'about.section1.title': '¿Qué es el Rastreador de Sentimiento NASDAQ?',
        'about.section1.text1': 'El Rastreador de Sentimiento NASDAQ es un panel en tiempo real que te ayuda a entender cómo "se siente" el mercado sobre la bolsa NASDAQ. En lugar de solo mirar los precios subiendo o bajando, analizamos múltiples fuentes de información para darte una imagen completa del sentimiento del mercado.',
        'about.section1.text2': 'Piénsalo como tomar la temperatura del mercado. Nuestra herramienta procesa artículos de noticias, discusiones en redes sociales, indicadores técnicos, recomendaciones de analistas y datos de amplitud del mercado para crear una puntuación única y fácil de entender que te dice si el estado de ánimo general es positivo, negativo o neutral.',
        'about.section2.title': 'Entendiendo la Puntuación Compuesta',
        'about.section2.text1': 'La Puntuación de Sentimiento Compuesta es el corazón de nuestro panel. Es un número entre -100 y +100 que representa el sentimiento general del mercado:',
        'about.section2.bullish': 'ALCISTA',
        'about.section2.bullish.text': 'Sentimiento positivo del mercado',
        'about.section2.neutral': 'NEUTRAL',
        'about.section2.neutral.text': 'Sentimiento mixto o equilibrado',
        'about.section2.bearish': 'BAJISTA',
        'about.section2.bearish.text': 'Sentimiento negativo del mercado',
        'about.section2.important': 'Importante:',
        'about.section2.important.text': 'La puntuación se actualiza automáticamente durante el horario de mercado (9:30 AM - 4:00 PM ET) y refleja cambios en tiempo real en el sentimiento del mercado a medida que llegan nuevos datos.',
        'about.section3.title': 'Cómo Calculamos la Puntuación',
        'about.section3.text1': 'Nuestra Puntuación Compuesta combina cinco "impulsores" clave del sentimiento del mercado. Cada impulsor se analiza de forma independiente y luego se pondera para crear la puntuación final:',
        'about.section3.driver1': '<strong>Sentimiento de Noticias (40%)</strong> - Analizamos noticias financieras de fuentes principales para determinar si los titulares son positivos, negativos o neutrales sobre el NASDAQ.',
        'about.section3.driver2': '<strong>Redes Sociales (30%)</strong> - Monitoreamos discusiones en plataformas como Twitter y Reddit para medir el sentimiento de los inversores minoristas y temas de tendencia.',
        'about.section3.driver3': '<strong>Indicadores Técnicos (30%)</strong> - Examinamos movimientos de precios, volúmenes de negociación y patrones técnicos que observan los traders profesionales.',
        'about.section3.driver4': '<strong>Recomendaciones de Analistas</strong> - Rastreamos mejoras, rebajas y cambios en el precio objetivo de analistas financieros.',
        'about.section3.driver5': '<strong>Amplitud del Mercado</strong> - Medimos cuántas acciones están subiendo versus bajando para entender la fuerza general del mercado.',
        'about.section3.text2': 'Estos impulsores trabajan juntos para darte una vista completa que va más allá de los movimientos de precios.',
        'about.section4.title': 'Cómo Usar Esta Herramienta',
        'about.section4.item1': '<strong>Verifica la Puntuación Compuesta</strong> - Comienza con la puntuación de sentimiento principal (lado izquierdo del panel) para obtener una lectura instantánea del estado de ánimo del mercado.',
        'about.section4.item2': '<strong>Revisa los Impulsores de Sentimiento</strong> - Mira los impulsores individuales para ver qué está influyendo en la puntuación general. ¿Todos los impulsores están alineados, o algunos son positivos mientras otros son negativos?',
        'about.section4.item3': '<strong>Examina la Tendencia Histórica</strong> - Usa el gráfico en la parte inferior para ver cómo ha cambiado el sentimiento en las últimas horas. ¿Está mejorando o deteriorándose?',
        'about.section4.item4': '<strong>Ajusta los Marcos de Tiempo</strong> - Haz clic en los botones de marco de tiempo (1m, 5m, 15m, 30m, 1h) para ver las tendencias de sentimiento en diferentes períodos.',
        'about.section4.item5': '<strong>Usa Cualquier Zona Horaria</strong> - Haz clic en la visualización de hora en la parte superior derecha para cambiar entre diferentes zonas horarias para tu conveniencia.',
        'about.section4.protip': 'Consejo profesional:',
        'about.section4.protip.text': 'Esta herramienta es más útil cuando se combina con otras investigaciones. Úsala para confirmar tus ideas comerciales, detectar cambios de sentimiento o identificar cuándo el estado de ánimo del mercado podría estar cambiando de dirección.',
        'about.section5.title': 'Aviso Importante',
        'about.section5.text1': 'Esta herramienta proporciona análisis de sentimiento del mercado solo con fines informativos. <strong>No</strong> es asesoramiento financiero y no debe ser su única fuente de información al tomar decisiones de inversión.',
        'about.section5.text2': 'El sentimiento del mercado puede cambiar rápidamente, y el sentimiento pasado no predice movimientos futuros del mercado. Siempre haga su propia investigación, consulte con profesionales financieros y considere su situación financiera personal antes de tomar decisiones de inversión.',

        // News Page
        'news.title': 'Últimas Noticias',
        'news.filter.all': 'Todas',
        'news.filter.most-impactful': 'Más Impactantes',
        'news.stat.total': 'Total de Artículos',
        'news.loading': 'Cargando noticias...',
        'news.no-articles': 'No se encontraron noticias',
        'news.no-articles.subtitle': 'Vuelve más tarde para las últimas noticias del NASDAQ',
        'news.article.read-more': 'Leer artículo completo →',

        // Dashboard
        'dashboard.score.label': 'Puntuación de Sentimiento Compuesto',
        'dashboard.drivers.title': 'Impulsores de Sentimiento',
        'dashboard.driver.indicators': 'Indicadores',
        'dashboard.driver.social': 'Redes Sociales',
        'dashboard.driver.news': 'Sentimiento de Noticias',
        'dashboard.driver.recommendations': 'Recomendaciones',
        'dashboard.driver.breadth': 'Amplitud del Mercado',
        'dashboard.driver.vix': 'VIX',
        'dashboard.chart.title': 'NASDAQ',
        'dashboard.chart.timeframe.1m': '1 min',
        'dashboard.chart.timeframe.5m': '5 min',
        'dashboard.chart.timeframe.15m': '15 min',
        'dashboard.chart.timeframe.30m': '30 min',
        'dashboard.chart.timeframe.1h': '1 hr',
        'dashboard.chart.timeframe.2h': '2 hrs',
        'dashboard.chart.timeframe.4h': '4 hrs',
        'dashboard.chart.timeframe.6h': 'Sesión',
        'dashboard.chart.timeframe.2d': '2 días',
        'dashboard.chart.timeframe.3d': '3 días',
        'dashboard.status.bullish': 'ALCISTA',
        'dashboard.status.neutral': 'NEUTRAL',
        'dashboard.status.bearish': 'BAJISTA',

        // Common
        'common.app-name': 'Rastreador de Sentimiento NASDAQ',
        'common.app-name-short': 'NASDAQ',
        'common.app-name-subtitle': 'Sentiment Tracker',
    },

    fr: {
        // Navigation
        'nav.dashboard': 'Tableau de bord',
        'nav.about': 'À propos',
        'nav.indices': 'Indices',
        'nav.news': 'Actualités',
        'nav.trading': 'Trading',
        'nav.language': 'Langue',
        'nav.logout': 'Déconnexion',

        // Onboarding Modal
        'onboarding.title.language': 'Sélectionnez votre langue',
        'onboarding.subtitle.language': 'Choisissez votre langue préférée pour le tableau de bord',
        'onboarding.button.continue': 'Continuer',
        'onboarding.title.disclaimer': 'Avis important',
        'onboarding.disclaimer.heading': 'Avertissement sur les risques',
        'onboarding.disclaimer.text': 'Le trading de contrats à terme, Forex, CFD et actions comporte un risque de perte. Veuillez examiner attentivement si ce type de trading vous convient. Les performances passées ne sont pas indicatives des résultats futurs. Tous les signaux ou conseils éducatifs fournis par PhoenixBinary et/ou Phoenix Algo, LLC et/ou tous les indicateurs fournis par ces derniers sont à des fins éducatives uniquement et ne constituent pas des recommandations ou des conseils d\'investissement.',
        'onboarding.disclaimer.checkbox': 'Je comprends et reconnais les risques associés au trading',

        // Legal Notice
        'legal.title': 'Avertissement sur les risques',
        'legal.text': 'Le trading de contrats à terme, Forex, CFD et actions comporte un risque de perte. Veuillez examiner attentivement si ce type de trading vous convient. Les performances passées ne sont pas indicatives des résultats futurs. Tous les signaux ou conseils éducatifs fournis par PhoenixBinary et/ou Phoenix Algo, LLC et/ou tous les indicateurs fournis par ces derniers sont à des fins éducatives uniquement et ne constituent pas des recommandations ou des conseils d\'investissement.',

        // About Page
        'about.page.title': 'À propos du Tracker de Sentiment NASDAQ',
        'about.section1.title': 'Qu\'est-ce que le Tracker de Sentiment NASDAQ?',
        'about.section1.text1': 'Le Tracker de Sentiment NASDAQ est un tableau de bord en temps réel qui vous aide à comprendre comment le marché "ressent" la bourse NASDAQ. Au lieu de simplement regarder les prix monter ou descendre, nous analysons plusieurs sources d\'information pour vous donner une image complète du sentiment du marché.',
        'about.section1.text2': 'Pensez-y comme prendre la température du marché. Notre outil traite les articles de presse, les discussions sur les réseaux sociaux, les indicateurs techniques, les recommandations d\'analystes et les données de largeur du marché pour créer un score unique et facile à comprendre qui vous indique si l\'humeur générale est positive, négative ou neutre.',
        'about.section2.title': 'Comprendre le Score de Sentiment',
        'about.section2.text1': 'Le Score de Sentiment est le cœur de notre tableau de bord. C\'est un nombre entre -100 et +100 qui représente le sentiment global du marché:',
        'about.section2.bullish': 'HAUSSIER',
        'about.section2.bullish.text': 'Sentiment positif du marché',
        'about.section2.neutral': 'NEUTRE',
        'about.section2.neutral.text': 'Sentiment mixte ou équilibré',
        'about.section2.bearish': 'BAISSIER',
        'about.section2.bearish.text': 'Sentiment négatif du marché',
        'about.section2.important': 'Important:',
        'about.section2.important.text': 'Le score se met à jour automatiquement pendant les heures de marché (9:30 AM - 4:00 PM ET) et reflète les changements en temps réel du sentiment du marché à mesure que de nouvelles données arrivent.',
        'about.section3.title': 'Comment Nous Calculons le Score',
        'about.section3.text1': 'Notre Score de Sentiment combine cinq "moteurs" clés du sentiment du marché. Chaque moteur est analysé indépendamment puis pondéré pour créer le score final:',
        'about.section3.driver1': '<strong>Sentiment des Actualités (40%)</strong> - Nous analysons les actualités financières de sources majeures pour déterminer si les titres sont positifs, négatifs ou neutres à propos du NASDAQ.',
        'about.section3.driver2': '<strong>Médias Sociaux (30%)</strong> - Nous surveillons les discussions sur des plateformes comme Twitter et Reddit pour mesurer le sentiment des investisseurs particuliers et les sujets tendance.',
        'about.section3.driver3': '<strong>Indicateurs Techniques (30%)</strong> - Nous examinons les mouvements de prix, les volumes de trading et les modèles techniques que les traders professionnels surveillent.',
        'about.section3.driver4': '<strong>Recommandations d\'Analystes</strong> - Nous suivons les améliorations, les dégradations et les changements de prix cibles des analystes financiers.',
        'about.section3.driver5': '<strong>Largeur du Marché</strong> - Nous mesurons combien d\'actions montent par rapport à celles qui descendent pour comprendre la force globale du marché.',
        'about.section3.text2': 'Ces moteurs travaillent ensemble pour vous donner une vue complète qui va au-delà des simples mouvements de prix.',
        'about.section4.title': 'Comment Utiliser Cet Outil',
        'about.section4.item1': '<strong>Vérifiez le Score de Sentiment</strong> - Commencez par le score de sentiment principal (côté gauche du tableau de bord) pour obtenir une lecture instantanée de l\'humeur du marché.',
        'about.section4.item2': '<strong>Examinez les Moteurs de Sentiment</strong> - Regardez les moteurs individuels pour voir ce qui influence le score global. Tous les moteurs sont-ils alignés, ou certains sont positifs tandis que d\'autres sont négatifs?',
        'about.section4.item3': '<strong>Examinez la Tendance Historique</strong> - Utilisez le graphique en bas pour voir comment le sentiment a changé au cours des dernières heures. S\'améliore-t-il ou se détériore-t-il?',
        'about.section4.item4': '<strong>Ajustez les Périodes</strong> - Cliquez sur les boutons de période (1m, 5m, 15m, 30m, 1h) pour voir les tendances de sentiment sur différentes périodes.',
        'about.section4.item5': '<strong>Utilisez N\'importe Quel Fuseau Horaire</strong> - Cliquez sur l\'affichage de l\'heure en haut à droite pour basculer entre différents fuseaux horaires pour votre commodité.',
        'about.section4.protip': 'Conseil de pro:',
        'about.section4.protip.text': 'Cet outil est plus utile lorsqu\'il est combiné avec d\'autres recherches. Utilisez-le pour confirmer vos idées de trading, repérer les changements de sentiment ou identifier quand l\'humeur du marché pourrait changer de direction.',
        'about.section5.title': 'Avis Important',
        'about.section5.text1': 'Cet outil fournit une analyse du sentiment du marché à des fins d\'information uniquement. Ce <strong>n\'est pas</strong> un conseil financier et ne doit pas être votre seule source d\'information lors de la prise de décisions d\'investissement.',
        'about.section5.text2': 'Le sentiment du marché peut changer rapidement, et le sentiment passé ne prédit pas les mouvements futurs du marché. Faites toujours vos propres recherches, consultez des professionnels de la finance et tenez compte de votre situation financière personnelle avant de prendre des décisions d\'investissement.',

        // News Page
        'news.title': 'Dernières Actualités',
        'news.filter.all': 'Toutes',
        'news.filter.most-impactful': 'Plus Impactantes',
        'news.stat.total': 'Total d\'Articles',
        'news.loading': 'Chargement des actualités...',
        'news.no-articles': 'Aucune actualité trouvée',
        'news.no-articles.subtitle': 'Revenez plus tard pour les dernières actualités du NASDAQ',
        'news.article.read-more': 'Lire l\'article complet →',

        // Dashboard
        'dashboard.score.label': 'Score de Sentiment',
        'dashboard.drivers.title': 'Moteurs de Sentiment',
        'dashboard.driver.indicators': 'Indicateurs',
        'dashboard.driver.social': 'Médias Sociaux',
        'dashboard.driver.news': 'Sentiment des Actualités',
        'dashboard.driver.recommendations': 'Recommandations',
        'dashboard.driver.breadth': 'Largeur du Marché',
        'dashboard.driver.vix': 'VIX',
        'dashboard.chart.title': 'NASDAQ',
        'dashboard.chart.timeframe.1m': '1 min',
        'dashboard.chart.timeframe.5m': '5 min',
        'dashboard.chart.timeframe.15m': '15 min',
        'dashboard.chart.timeframe.30m': '30 min',
        'dashboard.chart.timeframe.1h': '1 h',
        'dashboard.chart.timeframe.2h': '2 h',
        'dashboard.chart.timeframe.4h': '4 h',
        'dashboard.chart.timeframe.6h': 'Session',
        'dashboard.chart.timeframe.2d': '2 jours',
        'dashboard.chart.timeframe.3d': '3 jours',
        'dashboard.status.bullish': 'HAUSSIER',
        'dashboard.status.neutral': 'NEUTRE',
        'dashboard.status.bearish': 'BAISSIER',

        // Common
        'common.app-name': 'Tracker de Sentiment NASDAQ',
        'common.app-name-short': 'NASDAQ',
        'common.app-name-subtitle': 'Sentiment Tracker',
    },

    de: {
        // Navigation
        'nav.dashboard': 'Dashboard',
        'nav.about': 'Über uns',
        'nav.indices': 'Indizes',
        'nav.news': 'Nachrichten',
        'nav.trading': 'Trading',
        'nav.language': 'Sprache',
        'nav.logout': 'Abmelden',

        // Onboarding Modal
        'onboarding.title.language': 'Wählen Sie Ihre Sprache',
        'onboarding.subtitle.language': 'Wählen Sie Ihre bevorzugte Sprache für das Dashboard',
        'onboarding.button.continue': 'Weiter',
        'onboarding.title.disclaimer': 'Wichtiger Hinweis',
        'onboarding.disclaimer.heading': 'Risikowarnung',
        'onboarding.disclaimer.text': 'Der Handel mit Futures, Forex, CFDs und Aktien birgt ein Verlustrisiko. Bitte überlegen Sie sorgfältig, ob dieser Handel für Sie geeignet ist. Die Wertentwicklung in der Vergangenheit ist kein Indikator für zukünftige Ergebnisse. Alle Signale oder Bildungsratschläge von PhoenixBinary und/oder Phoenix Algo, LLC und/oder alle von den genannten bereitgestellten Indikatoren dienen nur Bildungszwecken und stellen keine Anlageempfehlungen oder -beratung dar.',
        'onboarding.disclaimer.checkbox': 'Ich verstehe und erkenne die mit dem Handel verbundenen Risiken an',

        // Legal Notice
        'legal.title': 'Risikowarnung',
        'legal.text': 'Der Handel mit Futures, Forex, CFDs und Aktien birgt ein Verlustrisiko. Bitte überlegen Sie sorgfältig, ob dieser Handel für Sie geeignet ist. Die Wertentwicklung in der Vergangenheit ist kein Indikator für zukünftige Ergebnisse. Alle Signale oder Bildungsratschläge von PhoenixBinary und/oder Phoenix Algo, LLC und/oder alle von den genannten bereitgestellten Indikatoren dienen nur Bildungszwecken und stellen keine Anlageempfehlungen oder -beratung dar.',

        // About Page
        'about.page.title': 'Über den NASDAQ Stimmungs-Tracker',
        'about.section1.title': 'Was ist der NASDAQ Stimmungs-Tracker?',
        'about.section1.text1': 'Der NASDAQ Stimmungs-Tracker ist ein Echtzeit-Dashboard, das Ihnen hilft zu verstehen, wie der Markt über die NASDAQ-Börse "denkt". Anstatt nur Preise zu betrachten, die steigen oder fallen, analysieren wir mehrere Informationsquellen, um Ihnen ein vollständiges Bild der Marktstimmung zu geben.',
        'about.section1.text2': 'Denken Sie daran als Temperaturmessung des Marktes. Unser Tool verarbeitet Nachrichtenartikel, Social-Media-Diskussionen, technische Indikatoren, Analystenempfehlungen und Marktbreitendaten, um einen einzelnen, leicht verständlichen Score zu erstellen, der Ihnen sagt, ob die allgemeine Stimmung positiv, negativ oder neutral ist.',
        'about.section2.title': 'Den Stimmungs-Score Verstehen',
        'about.section2.text1': 'Der Stimmungs-Score ist das Herzstück unseres Dashboards. Es ist eine Zahl zwischen -100 und +100, die die allgemeine Marktstimmung darstellt:',
        'about.section2.bullish': 'BULLISH',
        'about.section2.bullish.text': 'Positive Marktstimmung',
        'about.section2.neutral': 'NEUTRAL',
        'about.section2.neutral.text': 'Gemischte oder ausgewogene Stimmung',
        'about.section2.bearish': 'BEARISH',
        'about.section2.bearish.text': 'Negative Marktstimmung',
        'about.section2.important': 'Wichtig:',
        'about.section2.important.text': 'Der Score wird automatisch während der Marktzeiten (9:30 AM - 4:00 PM ET) aktualisiert und spiegelt Echtzeit-Änderungen der Marktstimmung wider, sobald neue Daten eingehen.',
        'about.section3.title': 'Wie Wir den Score Berechnen',
        'about.section3.text1': 'Unser Stimmungs-Score kombiniert fünf wichtige "Treiber" der Marktstimmung. Jeder Treiber wird unabhängig analysiert und dann gewichtet, um den endgültigen Score zu erstellen:',
        'about.section3.driver1': '<strong>Nachrichtenstimmung (40%)</strong> - Wir analysieren Finanznachrichten von großen Quellen, um festzustellen, ob Schlagzeilen über das NASDAQ positiv, negativ oder neutral sind.',
        'about.section3.driver2': '<strong>Social Media (30%)</strong> - Wir überwachen Diskussionen auf Plattformen wie Twitter und Reddit, um die Stimmung der Privatanleger und Trendthemen zu messen.',
        'about.section3.driver3': '<strong>Technische Indikatoren (30%)</strong> - Wir untersuchen Preisbewegungen, Handelsvolumen und technische Muster, die professionelle Trader beobachten.',
        'about.section3.driver4': '<strong>Analystenempfehlungen</strong> - Wir verfolgen Upgrades, Downgrades und Kurszieländerungen von Finanzanalysten.',
        'about.section3.driver5': '<strong>Marktbreite</strong> - Wir messen, wie viele Aktien steigen im Vergleich zu fallenden, um die allgemeine Marktstärke zu verstehen.',
        'about.section3.text2': 'Diese Treiber arbeiten zusammen, um Ihnen eine umfassende Ansicht zu geben, die über bloße Preisbewegungen hinausgeht.',
        'about.section4.title': 'Wie Man Dieses Tool Verwendet',
        'about.section4.item1': '<strong>Überprüfen Sie den Stimmungs-Score</strong> - Beginnen Sie mit dem Hauptstimmungs-Score (linke Seite des Dashboards), um eine sofortige Einschätzung der Marktstimmung zu erhalten.',
        'about.section4.item2': '<strong>Überprüfen Sie die Stimmungstreiber</strong> - Sehen Sie sich die einzelnen Treiber an, um zu sehen, was den Gesamtscore beeinflusst. Sind alle Treiber ausgerichtet oder sind einige positiv, während andere negativ sind?',
        'about.section4.item3': '<strong>Untersuchen Sie den Historischen Trend</strong> - Verwenden Sie das Diagramm unten, um zu sehen, wie sich die Stimmung in den letzten Stunden verändert hat. Verbessert sie sich oder verschlechtert sie sich?',
        'about.section4.item4': '<strong>Zeitrahmen Anpassen</strong> - Klicken Sie auf die Zeitrahmen-Schaltflächen (1m, 5m, 15m, 30m, 1h), um Stimmungstrends über verschiedene Zeiträume zu sehen.',
        'about.section4.item5': '<strong>Beliebige Zeitzone Verwenden</strong> - Klicken Sie auf die Zeitanzeige oben rechts, um zwischen verschiedenen Zeitzonen zu wechseln.',
        'about.section4.protip': 'Profi-Tipp:',
        'about.section4.protip.text': 'Dieses Tool ist am nützlichsten, wenn es mit anderen Recherchen kombiniert wird. Verwenden Sie es, um Ihre Handelsideen zu bestätigen, Stimmungsänderungen zu erkennen oder zu identifizieren, wann sich die Marktstimmung ändern könnte.',
        'about.section5.title': 'Wichtiger Hinweis',
        'about.section5.text1': 'Dieses Tool bietet Marktstimmungsanalysen nur zu Informationszwecken. Es ist <strong>keine</strong> Finanzberatung und sollte nicht Ihre einzige Informationsquelle bei Investitionsentscheidungen sein.',
        'about.section5.text2': 'Die Marktstimmung kann sich schnell ändern, und vergangene Stimmungen sagen keine zukünftigen Marktbewegungen voraus. Führen Sie immer Ihre eigene Recherche durch, konsultieren Sie Finanzexperten und berücksichtigen Sie Ihre persönliche finanzielle Situation, bevor Sie Investitionsentscheidungen treffen.',

        // News Page
        'news.title': 'Neueste Nachrichten',
        'news.filter.all': 'Alle',
        'news.filter.most-impactful': 'Wirkungsvollste',
        'news.stat.total': 'Gesamtartikel',
        'news.loading': 'Nachrichten werden geladen...',
        'news.no-articles': 'Keine Nachrichten gefunden',
        'news.no-articles.subtitle': 'Schauen Sie später für die neuesten NASDAQ-Nachrichten vorbei',
        'news.article.read-more': 'Vollständigen Artikel lesen →',

        // Dashboard
        'dashboard.score.label': 'Stimmungs-Score',
        'dashboard.drivers.title': 'Stimmungstreiber',
        'dashboard.driver.indicators': 'Indikatoren',
        'dashboard.driver.social': 'Social Media',
        'dashboard.driver.news': 'Nachrichtenstimmung',
        'dashboard.driver.recommendations': 'Empfehlungen',
        'dashboard.driver.breadth': 'Marktbreite',
        'dashboard.driver.vix': 'VIX',
        'dashboard.chart.title': 'NASDAQ',
        'dashboard.chart.timeframe.1m': '1 Min',
        'dashboard.chart.timeframe.5m': '5 Min',
        'dashboard.chart.timeframe.15m': '15 Min',
        'dashboard.chart.timeframe.30m': '30 Min',
        'dashboard.chart.timeframe.1h': '1 Std',
        'dashboard.chart.timeframe.2h': '2 Std',
        'dashboard.chart.timeframe.4h': '4 Std',
        'dashboard.chart.timeframe.6h': 'Sitzung',
        'dashboard.chart.timeframe.2d': '2 Tage',
        'dashboard.chart.timeframe.3d': '3 Tage',
        'dashboard.status.bullish': 'BULLISH',
        'dashboard.status.neutral': 'NEUTRAL',
        'dashboard.status.bearish': 'BEARISH',

        // Common
        'common.app-name': 'NASDAQ Stimmungs-Tracker',
        'common.app-name-short': 'NASDAQ',
        'common.app-name-subtitle': 'Sentiment Tracker',
    },

    zh: {
        // Navigation
        'nav.dashboard': '仪表板',
        'nav.about': '关于我们',
        'nav.indices': '指数',
        'nav.news': '新闻',
        'nav.trading': '交易',
        'nav.language': '语言',
        'nav.logout': '登出',

        // Onboarding Modal
        'onboarding.title.language': '选择您的语言',
        'onboarding.subtitle.language': '为仪表板选择您喜欢的语言',
        'onboarding.button.continue': '继续',
        'onboarding.title.disclaimer': '重要免责声明',
        'onboarding.disclaimer.heading': '风险警告',
        'onboarding.disclaimer.text': '交易期货、外汇、差价合约和股票涉及亏损风险。请仔细考虑此类交易是否适合您。过去的表现并不代表未来的结果。PhoenixBinary 和/或 Phoenix Algo, LLC 提供的任何及所有信号或教育建议，以及上述提供的任何指标，仅用于教育目的，不构成投资建议或推荐。',
        'onboarding.disclaimer.checkbox': '我理解并承认与交易相关的风险',

        // Legal Notice
        'legal.title': '风险警告',
        'legal.text': '交易期货、外汇、差价合约和股票涉及亏损风险。请仔细考虑此类交易是否适合您。过去的表现并不代表未来的结果。PhoenixBinary 和/或 Phoenix Algo, LLC 提供的任何及所有信号或教育建议，以及上述提供的任何指标，仅用于教育目的，不构成投资建议或推荐。',

        // About Page
        'about.page.title': '关于NASDAQ情绪跟踪器',
        'about.section1.title': '什么是NASDAQ情绪跟踪器？',
        'about.section1.text1': 'NASDAQ情绪跟踪器是一个实时仪表板，帮助您了解市场对NASDAQ股票交易所的"感觉"。我们不仅仅关注价格的涨跌，而是分析多个信息来源，为您提供市场情绪的完整画面。',
        'about.section1.text2': '把它想象成测量市场的温度。我们的工具处理新闻文章、社交媒体讨论、技术指标、分析师建议和市场广度数据，创建一个单一的、易于理解的分数，告诉您整体情绪是积极的、消极的还是中性的。',
        'about.section2.title': '理解综合得分',
        'about.section2.text1': '综合情绪得分是我们仪表板的核心。它是一个介于-100和+100之间的数字，代表整体市场情绪：',
        'about.section2.bullish': '看涨',
        'about.section2.bullish.text': '积极的市场情绪',
        'about.section2.neutral': '中性',
        'about.section2.neutral.text': '混合或平衡的情绪',
        'about.section2.bearish': '看跌',
        'about.section2.bearish.text': '消极的市场情绪',
        'about.section2.important': '重要：',
        'about.section2.important.text': '得分在市场时间内自动更新（美国东部时间上午9:30 - 下午4:00），并随着新数据的到来实时反映市场情绪的变化。',
        'about.section3.title': '我们如何计算得分',
        'about.section3.text1': '我们的综合得分结合了市场情绪的五个关键"驱动因素"。每个驱动因素都被独立分析，然后加权以创建最终得分：',
        'about.section3.driver1': '<strong>新闻情绪（40%）</strong> - 我们分析来自主要来源的财经新闻，以确定关于NASDAQ的标题是积极的、消极的还是中性的。',
        'about.section3.driver2': '<strong>社交媒体（30%）</strong> - 我们监控Twitter和Reddit等平台上的讨论，以衡量散户投资者的情绪和热门话题。',
        'about.section3.driver3': '<strong>技术指标（30%）</strong> - 我们检查专业交易员关注的价格走势、交易量和技术模式。',
        'about.section3.driver4': '<strong>分析师建议</strong> - 我们跟踪金融分析师的升级、降级和目标价格变化。',
        'about.section3.driver5': '<strong>市场广度</strong> - 我们衡量有多少股票在上涨与下跌，以了解整体市场强度。',
        'about.section3.text2': '这些驱动因素共同为您提供一个全面的视图，超越了单纯的价格走势。',
        'about.section4.title': '如何使用此工具',
        'about.section4.item1': '<strong>检查综合得分</strong> - 从主要情绪得分开始（仪表板左侧），立即了解市场情绪。',
        'about.section4.item2': '<strong>查看情绪驱动因素</strong> - 查看各个驱动因素，看看是什么影响了整体得分。所有驱动因素是否一致，还是有些积极而其他消极？',
        'about.section4.item3': '<strong>检查历史趋势</strong> - 使用底部的图表查看情绪在过去几个小时内的变化。它是在改善还是在恶化？',
        'about.section4.item4': '<strong>调整时间框架</strong> - 点击时间框架按钮（1m、5m、15m、30m、1h）以查看不同时间段的情绪趋势。',
        'about.section4.item5': '<strong>使用任何时区</strong> - 点击右上角的时间显示以在不同时区之间切换，以方便使用。',
        'about.section4.protip': '专业提示：',
        'about.section4.protip.text': '当与其他研究相结合时，此工具最有用。使用它来确认您的交易想法、发现情绪变化或识别市场情绪何时可能改变方向。',
        'about.section5.title': '重要免责声明',
        'about.section5.text1': '此工具仅提供市场情绪分析，仅供参考。这<strong>不是</strong>财务建议，在做出投资决策时不应作为您唯一的信息来源。',
        'about.section5.text2': '市场情绪可能会迅速变化，过去的情绪并不能预测未来的市场走势。在做出任何投资决策之前，请始终进行自己的研究，咨询财务专业人士，并考虑您的个人财务状况。',

        // News Page
        'news.title': '最新新闻',
        'news.filter.all': '全部',
        'news.filter.most-impactful': '最具影响力',
        'news.stat.total': '文章总数',
        'news.loading': '正在加载新闻文章...',
        'news.no-articles': '未找到新闻文章',
        'news.no-articles.subtitle': '稍后回来查看最新的NASDAQ新闻',
        'news.article.read-more': '阅读完整文章 →',

        // Dashboard
        'dashboard.score.label': '综合情绪得分',
        'dashboard.drivers.title': '情绪驱动因素',
        'dashboard.driver.indicators': '指标',
        'dashboard.driver.social': '社交媒体',
        'dashboard.driver.news': '新闻情绪',
        'dashboard.driver.recommendations': '推荐',
        'dashboard.driver.breadth': '市场广度',
        'dashboard.driver.vix': 'VIX',
        'dashboard.chart.title': 'NASDAQ',
        'dashboard.chart.timeframe.1m': '1分钟',
        'dashboard.chart.timeframe.5m': '5分钟',
        'dashboard.chart.timeframe.15m': '15分钟',
        'dashboard.chart.timeframe.30m': '30分钟',
        'dashboard.chart.timeframe.1h': '1小时',
        'dashboard.chart.timeframe.2h': '2小时',
        'dashboard.chart.timeframe.4h': '4小时',
        'dashboard.chart.timeframe.6h': '时段',
        'dashboard.chart.timeframe.2d': '2天',
        'dashboard.chart.timeframe.3d': '3天',
        'dashboard.status.bullish': '看涨',
        'dashboard.status.neutral': '中性',
        'dashboard.status.bearish': '看跌',

        // Common
        'common.app-name': 'NASDAQ情绪跟踪器',
        'common.app-name-short': 'NASDAQ',
        'common.app-name-subtitle': 'Sentiment Tracker',
    },

    ja: {
        // Navigation
        'nav.dashboard': 'ダッシュボード',
        'nav.about': '概要',
        'nav.indices': '指数',
        'nav.news': 'ニュース',
        'nav.trading': '取引',
        'nav.language': '言語',
        'nav.logout': 'ログアウト',

        // Onboarding Modal
        'onboarding.title.language': '言語を選択',
        'onboarding.subtitle.language': 'ダッシュボードの言語を選択してください',
        'onboarding.button.continue': '続ける',
        'onboarding.title.disclaimer': '重要な免責事項',
        'onboarding.disclaimer.heading': 'リスク警告',
        'onboarding.disclaimer.text': '先物、外国為替、CFD、株式の取引には損失のリスクが伴います。このような取引があなたに適しているかどうか慎重に検討してください。過去のパフォーマンスは将来の結果を示すものではありません。PhoenixBinary および/または Phoenix Algo, LLC によって提供されるすべてのシグナルまたは教育的アドバイス、および前述によって提供されるすべてのインジケーターは、教育目的のみであり、投資の推奨やアドバイスを構成するものではありません。',
        'onboarding.disclaimer.checkbox': '取引に関連するリスクを理解し、認識します',

        // Legal Notice
        'legal.title': 'リスク警告',
        'legal.text': '先物、外国為替、CFD、株式の取引には損失のリスクが伴います。このような取引があなたに適しているかどうか慎重に検討してください。過去のパフォーマンスは将来の結果を示すものではありません。PhoenixBinary および/または Phoenix Algo, LLC によって提供されるすべてのシグナルまたは教育的アドバイス、および前述によって提供されるすべてのインジケーターは、教育目的のみであり、投資の推奨やアドバイスを構成するものではありません。',

        // About Page
        'about.page.title': 'NASDAQセンチメントトラッカーについて',
        'about.section1.title': 'NASDAQセンチメントトラッカーとは？',
        'about.section1.text1': 'NASDAQセンチメントトラッカーは、NASDAQ株式市場に対して市場がどのように「感じている」かを理解するのに役立つリアルタイムダッシュボードです。価格の上下だけを見るのではなく、複数の情報源を分析して、市場センチメントの完全な画像を提供します。',
        'about.section1.text2': '市場の温度を測ることと考えてください。私たちのツールは、ニュース記事、ソーシャルメディアの議論、テクニカル指標、アナリストの推奨、市場の広がりデータを処理して、全体的な雰囲気が前向き、否定的、または中立的かを示す単一で理解しやすいスコアを作成します。',
        'about.section2.title': '総合スコアの理解',
        'about.section2.text1': '総合センチメントスコアは、ダッシュボードの中心です。これは-100から+100の間の数字で、全体的な市場センチメントを表します：',
        'about.section2.bullish': '強気',
        'about.section2.bullish.text': '前向きな市場センチメント',
        'about.section2.neutral': '中立',
        'about.section2.neutral.text': '混合または均衡したセンチメント',
        'about.section2.bearish': '弱気',
        'about.section2.bearish.text': '否定的な市場センチメント',
        'about.section2.important': '重要：',
        'about.section2.important.text': 'スコアは市場時間中（午前9時30分 - 午後4時00分 ET）に自動的に更新され、新しいデータが入ってくると市場センチメントのリアルタイムの変化を反映します。',
        'about.section3.title': 'スコアの計算方法',
        'about.section3.text1': '私たちの総合スコアは、市場センチメントの5つの主要な「ドライバー」を組み合わせています。各ドライバーは独立して分析され、最終スコアを作成するために重み付けされます：',
        'about.section3.driver1': '<strong>ニュースセンチメント（40%）</strong> - NASDAQに関する見出しが前向き、否定的、または中立的かを判断するために、主要なソースからの金融ニュースを分析します。',
        'about.section3.driver2': '<strong>ソーシャルメディア（30%）</strong> - TwitterやRedditなどのプラットフォームでの議論を監視して、個人投資家のセンチメントとトレンドトピックを測定します。',
        'about.section3.driver3': '<strong>テクニカル指標（30%）</strong> - プロのトレーダーが注目する価格動向、取引量、テクニカルパターンを調査します。',
        'about.section3.driver4': '<strong>アナリストの推奨</strong> - 金融アナリストからのアップグレード、ダウングレード、目標価格の変更を追跡します。',
        'about.section3.driver5': '<strong>市場の広がり</strong> - 上昇している株と下落している株の数を測定して、全体的な市場の強さを理解します。',
        'about.section3.text2': 'これらのドライバーは協力して、単なる価格動向を超えた包括的なビューを提供します。',
        'about.section4.title': 'このツールの使い方',
        'about.section4.item1': '<strong>総合スコアを確認</strong> - メインのセンチメントスコア（ダッシュボードの左側）から始めて、市場の雰囲気を即座に読み取ります。',
        'about.section4.item2': '<strong>センチメントドライバーを確認</strong> - 個々のドライバーを見て、全体的なスコアに何が影響しているかを確認します。すべてのドライバーが一致していますか、それとも一部は前向きで他は否定的ですか？',
        'about.section4.item3': '<strong>履歴トレンドを調べる</strong> - 下部のチャートを使用して、過去数時間でセンチメントがどのように変化したかを確認します。改善していますか、それとも悪化していますか？',
        'about.section4.item4': '<strong>時間枠を調整</strong> - 時間枠ボタン（1m、5m、15m、30m、1h）をクリックして、さまざまな期間のセンチメントトレンドを確認します。',
        'about.section4.item5': '<strong>任意のタイムゾーンを使用</strong> - 右上の時刻表示をクリックして、便利なようにさまざまなタイムゾーンを切り替えます。',
        'about.section4.protip': 'プロのヒント：',
        'about.section4.protip.text': 'このツールは、他の調査と組み合わせると最も有用です。取引のアイデアを確認したり、センチメントの変化を発見したり、市場の雰囲気が方向を変える可能性がある時期を特定したりするために使用してください。',
        'about.section5.title': '重要な免責事項',
        'about.section5.text1': 'このツールは情報提供のみを目的とした市場センチメント分析を提供します。これは<strong>金融アドバイスではなく</strong>、投資決定を行う際の唯一の情報源とすべきではありません。',
        'about.section5.text2': '市場センチメントは急速に変化する可能性があり、過去のセンチメントは将来の市場動向を予測しません。投資決定を行う前に、常に独自の調査を行い、金融専門家に相談し、個人的な財務状況を考慮してください。',

        // News Page
        'news.title': '最新ニュースフィード',
        'news.filter.all': 'すべて',
        'news.filter.most-impactful': '最も影響力のある',
        'news.stat.total': '記事総数',
        'news.loading': 'ニュース記事を読み込み中...',
        'news.no-articles': 'ニュース記事が見つかりません',
        'news.no-articles.subtitle': '最新のNASDAQニュースは後でご確認ください',
        'news.article.read-more': '完全な記事を読む →',

        // Dashboard
        'dashboard.score.label': '総合センチメントスコア',
        'dashboard.drivers.title': 'センチメントドライバー',
        'dashboard.driver.indicators': '指標',
        'dashboard.driver.social': 'ソーシャルメディア',
        'dashboard.driver.news': 'ニュースセンチメント',
        'dashboard.driver.recommendations': '推奨',
        'dashboard.driver.breadth': '市場の広がり',
        'dashboard.driver.vix': 'VIX',
        'dashboard.chart.title': 'NASDAQ',
        'dashboard.chart.timeframe.1m': '1分',
        'dashboard.chart.timeframe.5m': '5分',
        'dashboard.chart.timeframe.15m': '15分',
        'dashboard.chart.timeframe.30m': '30分',
        'dashboard.chart.timeframe.1h': '1時間',
        'dashboard.chart.timeframe.2h': '2時間',
        'dashboard.chart.timeframe.4h': '4時間',
        'dashboard.chart.timeframe.6h': 'セッション',
        'dashboard.chart.timeframe.2d': '2日',
        'dashboard.chart.timeframe.3d': '3日',
        'dashboard.status.bullish': '強気',
        'dashboard.status.neutral': '中立',
        'dashboard.status.bearish': '弱気',

        // Common
        'common.app-name': 'NASDAQセンチメントトラッカー',
        'common.app-name-short': 'NASDAQ',
        'common.app-name-subtitle': 'Sentiment Tracker',
    }
};

/**
 * Get translation for a key in the current language
 * @param {string} key - Translation key (e.g., 'nav.dashboard')
 * @param {string} lang - Language code (default: current language)
 * @returns {string} - Translated text or key if not found
 */
function t(key, lang = null) {
    const currentLang = lang || getCurrentLanguage();
    return translations[currentLang]?.[key] || translations['en'][key] || key;
}

/**
 * Get the current language from localStorage
 * @returns {string} - Language code (default: 'en')
 */
function getCurrentLanguage() {
    try {
        // Try to get user-specific language if Clerk is available
        if (window.Clerk && window.Clerk.user) {
            const userId = window.Clerk.user.id;
            const userLang = localStorage.getItem(`user_language_${userId}`);
            if (userLang && translations[userLang]) {
                return userLang;
            }
        }
    } catch (error) {
        console.error('Error getting current language:', error);
    }

    // Fallback to default language
    return localStorage.getItem('app_language') || 'en';
}

/**
 * Set the language and update all translatable elements
 * @param {string} lang - Language code
 */
function setLanguage(lang) {
    if (!translations[lang]) {
        console.error(`Language '${lang}' not supported`);
        return;
    }

    // Save language preference
    try {
        if (window.Clerk && window.Clerk.user) {
            const userId = window.Clerk.user.id;
            localStorage.setItem(`user_language_${userId}`, lang);
        }
        localStorage.setItem('app_language', lang);
    } catch (error) {
        console.error('Error saving language preference:', error);
    }

    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key, lang);

        // Check if element should use innerHTML (for translations with HTML tags)
        if (element.hasAttribute('data-i18n-html')) {
            element.innerHTML = translation;
        } else {
            element.textContent = translation;
        }
    });

    // Dispatch event for custom language change handlers
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
}

/**
 * Initialize translations on page load
 */
function initTranslations() {
    const currentLang = getCurrentLanguage();

    // Apply translations to all elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        const translation = t(key, currentLang);

        // Check if element should use innerHTML (for translations with HTML tags)
        if (element.hasAttribute('data-i18n-html')) {
            element.innerHTML = translation;
        } else {
            element.textContent = translation;
        }
    });
}

// Auto-initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTranslations);
} else {
    initTranslations();
}
