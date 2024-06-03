// just to simplify and get the user without always writting session?.user
// reusable libs to use with authJs in server side
// in actions, in server components and in API routes (all server side)
import { auth } from "@/auth";

export const currentUser = async () => {
  const session = await auth();
  return session?.user;
};
export const currentRole = async () => {
  const session = await auth();
  return session?.user?.role;
};
