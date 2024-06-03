// this custom hook is to use avoid being always using session.data?.user in pages to get the current user
//reusable hook to use with ssessions and users
import { useSession } from "next-auth/react";

export const useCurrentRole = () => {
  const session = useSession();
  return session.data?.user?.role;
};
