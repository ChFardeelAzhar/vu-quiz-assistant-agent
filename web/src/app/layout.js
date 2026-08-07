import "./globals.css";

export const metadata = {
  title: "VU Quiz Agent | Automate Your VU LMS",
  description: "An AI-powered SaaS to automate and monitor your Virtual University quizzes effortlessly.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {/* Background Ambient Orbs */}
        <div className="bg-glow-orb" style={{ top: '-100px', left: '-100px' }}></div>
        <div className="bg-glow-orb bg-glow-orb-purple" style={{ bottom: '-100px', right: '-100px' }}></div>
        
        {/* Main Content */}
        {children}
      </body>
    </html>
  );
}
