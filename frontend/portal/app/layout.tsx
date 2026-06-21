import "./styles.css";

export const metadata = {
  title: "AI Registration Agent Portal",
  description: "AI-powered business registration and approval portal",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="topbar">
          <a href="/" className="brand">AI Registration Portal</a>
          <nav>
            <a href="/register">Register</a>
            <a href="/status">Status</a>
            <a href="/reviewer">Reviewer</a>
          </nav>
        </header>
        <main className="page">{children}</main>
      </body>
    </html>
  );
}
