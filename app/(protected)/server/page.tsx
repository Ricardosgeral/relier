import UserInfo from "@/components/user-info";
import { currentUser } from "@/lib/auth";

export default async function ServerPage() {
  const user = await currentUser(); // uses auth from lib for rendering in server components
  return <UserInfo user={user} label="💻 Server component" />;
}
