"use client";

import NavLinks from "./nav-links";
import LogoApp from "./logo-app";
import { ModeToggle } from "./theme-toggle";

export const Sidebar = () => {
  const currentYear = new Date().getFullYear();

  return (
    <section className="sticky left-0 top-0 flex h-screen flex-col flex-wrap items-center justify-between border-r border-gray-300 py-4 text-black dark:dark:text-slate-200 max-md:hidden">
      <LogoApp square={true} />
      <NavLinks />
      <ModeToggle />
      <div className="p-2 text-xs text-gray-900 dark:text-slate-200">
        © {currentYear} Ricardos
      </div>
    </section>
  );
};
