"use client";

import { redirect, useRouter } from "next/navigation";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import { LoginForm } from "./login-form";
import { RegisterForm } from "./register-form";

//This is the name of the interface that
// defines the type of props accepted by the LoginButton component.
interface LoginButtonProps {
  children: React.ReactNode; //any type of content that can be rendered in react
  mode?: "modal" | "redirect";
  type?: "login" | "register";
  asChild?: boolean;
}

export const LoginButton = ({
  children,
  mode = "redirect",
  type = "login",
  asChild,
}: LoginButtonProps) => {
  //This hook allows you to programmatically change routes inside Client Component
  const router = useRouter();

  const onClick = () => {
    if ((type = "register")) {
      router.push("/auth/register");
    } else {
      router.push("/auth/login");
    }
  };

  if (mode === "modal") {
    return (
      <Dialog>
        <DialogTrigger asChild={asChild}>{children}</DialogTrigger>
        <DialogContent className="p-0 w-auto bg-transparent">
          {type === "register" ? <RegisterForm /> : <LoginForm />}
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <span onClick={onClick} className="cursor-pointer">
      {children}
    </span>
  );
};
