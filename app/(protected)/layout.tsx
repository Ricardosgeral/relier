import { NavBar } from "@/app/(protected)/_components/navbar";

interface ProtectLayoutProps {
  children: React.ReactNode;
}

export default function ProtectedLayout({ children }: ProtectLayoutProps) {
  return (
    <div className="w-full min-h-screen flex flex-col gap-y-2">
      <NavBar />
      {children}
    </div>
  );
}
// bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-yellow-400 to-yellow-600"
