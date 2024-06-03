"use client";

import { UserAvatar } from "@/components/auth/user-avatar";
import LogoApp from "@/components/logo-app";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { usePathname } from "next/navigation";

export const NavBar = () => {
  const pathname = usePathname();
  return (
    <nav className=" bg-slate-50 flex w-full justify-between px-2 pb-2 items-center shadow-md">
      <div className="">
        <Link href="/">
          <LogoApp square={true}></LogoApp>
        </Link>
      </div>
      <div>
        <div className="flex gap-x-2">
          <Button
            asChild
            variant={pathname === "/server" ? "default" : "outline"}
          >
            <Link href="/server">Server</Link>
          </Button>
          <Button
            asChild
            variant={pathname === "/client" ? "default" : "outline"}
          >
            <Link href="/client">Client</Link>
          </Button>

          <Button
            asChild
            variant={pathname === "/admin" ? "default" : "outline"}
          >
            <Link href="/admin">Admin</Link>
          </Button>
          <Button
            asChild
            variant={pathname === "/settings" ? "default" : "outline"}
          >
            <Link href="/settings">Settings</Link>
          </Button>
        </div>
      </div>
      <div className="overflow-hidden pl-6 p-2 items-end">
        <UserAvatar />
      </div>
    </nav>
  );
};
