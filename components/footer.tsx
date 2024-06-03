import { logout } from "@/actions/logout";
import { ExtendedUser } from "@/auth";
import { useRouter } from "next/navigation";
import React from "react";
import IconLogout from "./icons/logout";

declare interface FooterProps {
  user: ExtendedUser;
  type?: "mobile" | "desktop";
}

const Footer = ({ user, type = "desktop" }: FooterProps) => {
  const router = useRouter();

  const handleLogOut = async () => {
    const loggedOut = await logout();
  };

  return (
    <footer className="flex overflow-hidden cursor-pointer items-center justify-between space-x-2">
      <div
        className={
          type === "mobile"
            ? "flex size-10 items-center justify-center rounded-full bg-gray-200"
            : "flex size-10 items-center justify-center rounded-full bg-gray-200 max-xl:hidden"
        }
      >
        <p className="text-xl font-bold text-gray-700">
          {user?.name?.slice(0, 1)}
        </p>
      </div>

      <div
        className={
          type === "mobile"
            ? "flex flex-1 flex-col overflow-hidden justify-start"
            : "flex flex-1 flex-col overflow-hidden justify-start max-xl:hidden"
        }
      >
        <h1 className="text-sm truncate overflow-ellipsis whitespace-nowrap text-gray-700 font-semibold">
          {user?.name}
        </h1>
        {/* <p className="text-sm truncate  font-normal text-gray-600">
          {user?.email}
        </p> */}
      </div>
      <div
        className="relative max-xl:w-full max-xl:flex max-xl:justify-center max-xl:items-center"
        onClick={handleLogOut}
      >
        <IconLogout className="hover:opacity-50" fill="none" stroke="black" />
      </div>
    </footer>
  );
};

export default Footer;
