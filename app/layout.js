export const metadata = {
  title: 'Agentic Workflow Control Console',
  description: 'Private Control Dashboard for Colab CrewAI Runner',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, padding: 0, backgroundColor: '#0f172a' }}>
        {children}
      </body>
    </html>
  );
}