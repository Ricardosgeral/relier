"use server"; //server action

import { db } from "@/lib/db";
import { currentUser } from "@/lib/auth";
import { getUserById } from "@/data/user";

export const deleteProfilePhoto = async (imageUrl: string) => {
  const user = await currentUser();

  if (!user) {
    return { error: "unauthorized" };
  }

  const dbUser = await getUserById(user.id);

  if (!dbUser) {
    return { error: "unauthorized" };
  }

  await db.user.update({
    where: { id: dbUser.id },
    data: { image: "" },
  });

  return { success: "Removed" };
};
