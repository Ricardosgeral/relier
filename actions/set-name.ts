"use server"; //server action

import { z } from "zod";
import { db } from "@/lib/db";
import { currentUser } from "@/lib/auth";
import { getUserById } from "@/data/user";
import { NameSchema } from "@/schemas";

export const setName = async (values: z.infer<typeof NameSchema>) => {
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
    data: { ...values },
  });

  return { success: "Updated" };
};
