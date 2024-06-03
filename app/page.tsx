"use client";
import { Poppins } from "next/font/google";

import { Button } from "@/components/ui/button";
import { LoginButton } from "@/components/auth/login-button";
import LogoApp from "@/components/logo-app";
import Link from "next/link";
import { Card } from "@/components/ui/card";
import Image from "next/image";
import { ModeToggle } from "@/components/theme-toggle";
import { useRouter } from "next/navigation";

const font = Poppins({
  subsets: ["latin"],
  weight: ["600"],
});

export default function Home() {
  const currentYear = new Date().getFullYear();

  return (
    <div className="flex min-h-screen min-w-[350px] flex-col">
      <header className="w-full">
        <div className="flex justify-center">
          <LogoApp />
        </div>
        <div className="flex justify-center space-x-4 bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-black to-slate-700 py-3 shadow-xl dark:bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] dark:from-yellow-500 dark:to-yellow-400">
          <LoginButton mode="modal" type="login" asChild>
            <Button
              variant="primary"
              size="lg"
              className="font-semibold dark:bg-slate-100 dark:text-black dark:hover:bg-slate-200"
            >
              Login
            </Button>
          </LoginButton>
          <LoginButton mode="modal" type="register" asChild>
            <Button variant="outline" size="lg">
              Getting started
            </Button>
          </LoginButton>
          <ModeToggle />
        </div>
      </header>

      <div className="flex w-full flex-grow flex-col items-center justify-evenly gap-4 p-4 lg:flex-row lg:gap-x-8 lg:px-8">
        <div className="w-full sm:w-4/5 md:w-3/4 lg:w-1/2">
          <Card className="flex h-full flex-row rounded-2xl shadow-xl">
            <div className="relative h-[200px] w-full sm:h-[380px]">
              <Image
                alt="dams"
                className="w-1/2 rounded-l-2xl object-cover"
                fill
                src="/images/dams_vertical.jpg"
                sizes="(max-width: 200px) 100vw, (max-width: 400px) 50vw"
              />
            </div>

            <div className="itens-center flex flex-col justify-evenly gap-4 p-4">
              <div className="lg:space-y-4">
                <h3 className="text-xl font-bold tracking-tighter md:text-3xl">
                  Dams database
                </h3>
                <p className="flex-1 text-pretty text-sm text-gray-500 dark:text-gray-400 sm:text-lg">
                  Discover main features and characteristics of dams
                </p>
              </div>
              <Link href={"/dams"}>
                <Button variant="default" size="sm" className="h-8 w-1/3">
                  Go
                </Button>
              </Link>
            </div>
          </Card>
        </div>
        <div className="w-full sm:w-4/5 md:w-3/4 lg:w-1/2">
          <Card className="flex h-full flex-row rounded-2xl shadow-xl">
            <div className="relative h-[200px] w-full sm:h-[380px]">
              <Image
                alt="dams"
                className="w-1/2 rounded-l-2xl object-cover"
                fill
                src="/images/regulations.png"
                sizes="(max-width: 200px) 100vw, (max-width: 400px) 100vw"
              />
            </div>
            <div className="itens-center flex flex-col justify-evenly gap-4 p-4">
              <div className="lg:space-y-4">
                <h3 className="text-xl font-bold tracking-tighter lg:text-3xl">
                  Dams regulations
                </h3>
                <p className="flex-1 text-pretty text-sm text-gray-500 dark:text-gray-400 sm:text-lg">
                  Find articles on regulations related to dam safety
                </p>
              </div>
              <Link href={"/regulations"}>
                <Button variant="default" size="sm" className="h-8 w-1/3">
                  Go
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </div>
      <footer className="w-full border-t bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] px-4 py-2 dark:from-yellow-500 dark:to-yellow-400">
        <div className="flex flex-col-reverse items-end justify-between gap-2 sm:flex-row">
          <div className="text-sm font-medium text-gray-900 dark:text-slate-600">
            © 2024-{currentYear} Ricardos Inc. All rights reserved.
          </div>
          <nav className="flex gap-4">
            <Link
              className="text-sm font-medium hover:underline dark:text-slate-600"
              href="#"
            >
              Privacy
            </Link>
            <Link
              className="text-sm font-medium hover:underline dark:text-slate-600"
              href="#"
            >
              Terms
            </Link>
            <Link
              className="text-sm font-medium hover:underline dark:text-slate-600"
              href="/Contact"
            >
              <Button variant="default" size="sm" className="">
                Contact
              </Button>
            </Link>
          </nav>
        </div>
      </footer>
    </div>
  );
}
