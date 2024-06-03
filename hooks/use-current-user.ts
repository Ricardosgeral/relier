"use client";

// this custom hook is to use avoid being always using session.data?.user in pages to get the current user

import { useSession } from "next-auth/react";
export const useCurrentUser = () => {
  const session = useSession();
  return session.data?.user;
};
