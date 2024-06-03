"use client";

import UserInfo from "@/components/user-info";
import { useCurrentUser } from "@/hooks/use-current-user";

export default function ClientPage() {
  const user = useCurrentUser(); // uses the custom hook to be rendered in client components
  return <UserInfo user={user} label=" 🕶️ Client component" />;
}
