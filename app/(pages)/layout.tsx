import Image from "next/image";
import { currentUser } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Sidebar } from "@/components/sidebar";
import MobileNav from "@/components/mobile-nav";
import Link from "next/link";
import LogoApp from "@/components/logo-app";

interface PagesLayoutProps {
  children: React.ReactNode;
}

export default async function PagesLayout({ children }: PagesLayoutProps) {
  const user = await currentUser(); // uses auth from lib for rendering in server components

  if (!user) redirect("/auth/login"); //middleware should avoid this, but...

  return (
    <main className="font-inter flex h-screen w-full">
      <Sidebar />

      <div className="flex size-full flex-col p-2">
        <div className="flex h-16 items-center justify-between p-2 md:hidden">
          <div className="h-16 w-16">
            <LogoApp />
          </div>
          <div>
            <MobileNav />
          </div>
        </div>
        {children}
      </div>
    </main>
  );
}
