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

  const router = useRouter();

  return (
    <div className="flex flex-col min-w-[350px] min-h-screen">
      <header className="w-full">
        <div className="flex justify-center ">
          <LogoApp />
        </div>
        <div
          className="flex justify-center space-x-4 py-3 shadow-xl 
        bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] from-black to-slate-700
        dark:bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] dark:from-yellow-500 dark:to-yellow-400"
        >
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

      <div className="flex flex-col flex-grow w-full items-center justify-evenly p-4 gap-4 lg:flex-row lg:px-8 lg:gap-x-8">
        <div className="w-full sm:w-4/5 md:w-3/4 lg:w-1/2">
          <Card className="flex  flex-row h-full rounded-2xl shadow-xl">
            <div className="relative w-full h-[200px] sm:h-[380px]">
              <Image
                alt="dams"
                className="w-1/2 rounded-l-2xl object-cover"
                fill
                src="/images/dams_vertical.jpg"
                sizes="(max-width: 200px) 100vw, (max-width: 400px) 50vw"
              />
            </div>

            <div className="flex flex-col justify-evenly itens-center gap-4 p-4">
              <div className="lg:space-y-4">
                <h3 className="text-xl md:text-3xl font-bold tracking-tighter">
                  Dams database
                </h3>
                <p className="text-sm sm:text-lg text-gray-500 text-pretty dark:text-gray-400 flex-1">
                  Discover main features and characteristics of dams
                </p>
              </div>
              <Link href={"/dams"}>
                <Button variant="default" size="sm" className="w-1/3 h-8">
                  Go
                </Button>
              </Link>
            </div>
          </Card>
        </div>
        <div className="w-full sm:w-4/5 md:w-3/4 lg:w-1/2">
          <Card className="flex flex-row h-full  rounded-2xl shadow-xl">
            <div className="relative w-full h-[200px] sm:h-[380px]">
              <Image
                alt="dams"
                className="w-1/2 rounded-l-2xl object-cover"
                fill
                src="/images/regulations.png"
                sizes="(max-width: 200px) 100vw, (max-width: 400px) 100vw"
              />
            </div>
            <div className="flex flex-col justify-evenly itens-center gap-4 p-4">
              <div className="lg:space-y-4">
                <h3 className="text-xl lg:text-3xl font-bold tracking-tighter">
                  Dams regulations
                </h3>
                <p className="text-sm sm:text-lg text-gray-500 text-pretty dark:text-gray-400 flex-1">
                  Find articles on regulations related to dam safety
                </p>
              </div>
              <Link href={"/regulations"}>
                <Button variant="default" size="sm" className="w-1/3 h-8">
                  Go
                </Button>
              </Link>
            </div>
          </Card>
        </div>
      </div>
      <footer className="w-full px-4 py-2 bg-[radial-gradient(ellipse_at_bottom,_var(--tw-gradient-stops))] dark:from-yellow-500 dark:to-yellow-400 border-t">
        <div className="flex flex-col-reverse items-end justify-between gap-2  sm:flex-row">
          <div className="text-sm text-gray-900 dark:text-slate-600 font-medium">
            © 2024-{currentYear} Ricardos Inc. All rights reserved.
          </div>
          <nav className="flex gap-4">
            <Link
              className="text-sm dark:text-slate-600 font-medium hover:underline"
              href="#"
            >
              Privacy
            </Link>
            <Link
              className="text-sm dark:text-slate-600 font-medium  hover:underline"
              href="#"
            >
              Terms
            </Link>
            <Link
              className="text-sm font-medium dark:text-slate-600 hover:underline"
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
