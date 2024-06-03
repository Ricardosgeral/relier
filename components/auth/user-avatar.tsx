"use client";
import { FaUser } from "react-icons/fa";
import { ExitIcon } from "@radix-ui/react-icons";
import { useState, useEffect } from "react";

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { LogoutButton } from "@/components/auth/logout-button";
import { LuSettings } from "react-icons/lu";
import { useCurrentUser } from "@/hooks/use-current-user";
import { Button } from "@/components/ui/button";
import AccountSettings from "@/components/account-settings";
import { useRouter } from "next/navigation";

declare interface UserAvatarProps {
  isPhotoLeft?: boolean;
  justPhoto?: boolean;
}

export function UserAvatar({
  isPhotoLeft = false,
  justPhoto = false,
}: UserAvatarProps) {
  const user = useCurrentUser();
  const [avatarUrl, setAvatarUrl] = useState(user?.image || undefined);

  useEffect(() => {
    setAvatarUrl(user?.image || undefined);
  }, [user?.image]);

  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const router = useRouter();

  const handleDialogClose = () => {
    // Do something after the dialog is closed
    router.refresh();
    // Perform any action here
  };

  return (
    <div
      className={
        isPhotoLeft
          ? "flex flex-row-reverse gap-x-2 px-2 justify-end"
          : "flex gap-x-3"
      }
    >
      {justPhoto ? (
        <div>
          <Avatar>
            <AvatarImage className="object-cover" src={avatarUrl} />
            <AvatarFallback className="bg-yellow-500 text-white shadow-xl ">
              {!user?.name ? (
                <FaUser />
              ) : (
                <p className="text-xl font-bold">
                  {user?.name?.slice(0, 1).toUpperCase()}
                </p>
              )}
            </AvatarFallback>
          </Avatar>
        </div>
      ) : (
        <>
          <div className="flex items-center overflow-hidden">
            {user?.name && (
              <h1 className="truncate overflow-ellipsis text-sm text-slate-600">
                {user?.name.trim().split(/\s+/)[0]}
              </h1>
            )}
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger>
              <div>
                <Avatar className="hover:ring-2 hover:ring-offset-2 hover:ring-yellow-500">
                  <AvatarImage className="object-cover" src={avatarUrl} />
                  <AvatarFallback className="bg-yellow-500 text-white shadow-xl hover:bg-yellow-500/80">
                    {!user?.name ? (
                      <FaUser />
                    ) : (
                      <p className="text-xl font-bold">
                        {user?.name?.slice(0, 1).toUpperCase()}
                      </p>
                    )}
                  </AvatarFallback>
                </Avatar>
              </div>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="min-w-[110px]" align="end">
              <p className="text-yellow-600 text-xs px-1 font-semibold">
                {user?.email?.toString()}
              </p>
              <DropdownMenuItem>
                <Button
                  variant="ghost"
                  className="flex w-full items-center justify-start pl-2 h-8"
                  onClick={() => setIsDialogOpen(true)}
                >
                  <LuSettings className="h-4 w-4 mr-1" />
                  Account
                </Button>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Button variant="ghost" className="w-full h-8 pl-2">
                  <LogoutButton className="flex w-full items-center justify-start ">
                    <ExitIcon className="h-4 w-4 mr-1" />
                    Logout
                  </LogoutButton>
                </Button>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogContent className="sm:max-w-md h-screen overflow-y-auto scrollbar-hide">
              <DialogHeader>
                <DialogTitle>Account settings</DialogTitle>
                <DialogDescription>
                  Update your account definitions
                </DialogDescription>
              </DialogHeader>
              <div className="flex items-center space-x-2">
                <AccountSettings />
              </div>
            </DialogContent>
          </Dialog>
        </>
      )}
    </div>
  );
}
