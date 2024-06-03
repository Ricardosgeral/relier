import authConfig from "@/auth.config";
import NextAuth, { type DefaultSession } from "next-auth";

import { UserRole } from "@prisma/client";
import { PrismaAdapter } from "@auth/prisma-adapter";

import { db } from "./lib/db";
import { getUserById } from "@/data/user";
import { getAccountByUserId } from "@/data/account";
import { getTwoFactorConfirmationByUserId } from "./data/two-factor-confirmation";

export type ExtendedUser = DefaultSession["user"] & {
  role: UserRole;
  isTwoFactorEnabled: boolean;
  isOAuth: boolean;
};

declare module "next-auth" {
  interface Session {
    user: ExtendedUser;
  }
}

export const {
  handlers: { GET, POST },
  auth,
  signIn,
  signOut,
} = NextAuth({
  pages: {
    signIn: "/auth/login", // redirects here if something went wrong during signin. like using the same email in github and google
    error: "/auth/error",
  },
  events: {
    // events are async funcs that do not return a response, tyeu are useful for audit logs/reporting or handle any other side effects
    async linkAccount({ user }) {
      await db.user.update({
        where: { id: user.id },
        data: { emailVerified: new Date() },
      });
    },
  },

  callbacks: {
    // async funcs to control what happens when an action is performed. better than do the logic in the actions
    // good for tokens and for sessions
    async signIn({ user, account }) {
      // Allow OAUth without email verification

      if (account?.provider !== "credentials") return true;

      const existingUser = await getUserById(user?.id as string);

      // prevent sign in without email verification
      if (!existingUser?.emailVerified) return false;

      if (existingUser.isTwoFactorEnabled) {
        const twoFactorConfirmation = await getTwoFactorConfirmationByUserId(
          existingUser.id,
        );
        if (!twoFactorConfirmation) return false;

        //delete two factor confirmation for nect sign in
        await db.twoFactorConfirmation.delete({
          where: { id: twoFactorConfirmation.id },
        });
      }

      return true;
    },
    async session({ session, user, token }) {
      if (token.sub && session.user) {
        session.user.id = token.sub; //defined the field id
      }
      if (token.role && session.user) {
        session.user.role = token.role as UserRole;
      }

      if (session.user) {
        session.user.name = token.name;
        session.user.image = token.image as string;

        session.user.email = token.email as string;
        session.user.isTwoFactorEnabled = token.isTwoFactorEnabled as boolean;
        session.user.isOAuth = token.isOAuth as boolean;
      }
      return session;
    },
    async jwt({ token }) {
      if (!token.sub) return token; // not logged in

      const existingUser = await getUserById(token.sub);

      if (!existingUser) return token; //not logged in

      const existingAccount = await getAccountByUserId(existingUser.id);

      token.isOAuth = !!existingAccount;
      token.name = existingUser.name;

      token.image = existingUser.image;
      token.email = existingUser.email;
      token.role = existingUser.role;
      token.isTwoFactorEnabled = existingUser.isTwoFactorEnabled;
      token.accountProvider = existingAccount?.provider;
      return token;
    },
  },
  adapter: PrismaAdapter(db),

  session: { strategy: "jwt" },

  ...authConfig,
});
