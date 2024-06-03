"use client";

import { cn } from "@/lib/utils";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { UserAvatar } from "./auth/user-avatar";
import NavLinks from "./nav-links";
import LogoApp from "./logo-app";
import { ModeToggle } from "./theme-toggle";

export const Sidebar = () => {
  const currentYear = new Date().getFullYear();

  return (
    <section className="sticky left-0 top-0 flex flex-col h-screen items-center justify-between py-4 max-md:hidden border-r border-gray-300 text-black">
      <LogoApp square={true} />
      <NavLinks />
      <ModeToggle />
      <div className="text-xs text-gray-900 dark:text-gray-200 p-2">
        © {currentYear} Ricardos
      </div>
    </section>
  );
};
