"use server";

import { signOut } from "@/auth";

export const logout = async () => {
  //some server stuff if needed
  await signOut({ redirectTo: "/auth/login", redirect: true });
};
