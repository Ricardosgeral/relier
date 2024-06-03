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
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
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

  const [isDialogOpen, setIsDialogOpen] = useState(false);

  const router = useRouter();

  return (
    <div
      className={
        isPhotoLeft
          ? "flex flex-row-reverse justify-end gap-x-2 px-2"
          : "flex gap-x-3"
      }
    >
      {justPhoto ? (
        <div>
          <Avatar className="ring-1 ring-foreground/80 hover:ring-2 hover:ring-yellow-500 hover:ring-offset-2">
            <AvatarImage className="object-cover" src={avatarUrl} />
            <AvatarFallback className="bg-yellow-500 text-white shadow-xl">
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
              <h1 className="truncate overflow-ellipsis text-sm text-foreground/80">
                {user?.name.trim().split(/\s+/)[0]}
              </h1>
            )}
          </div>
          <DropdownMenu>
            <DropdownMenuTrigger>
              <div>
                <Avatar className="ring-1 ring-foreground/80 hover:ring-2 hover:ring-yellow-500 hover:ring-offset-2">
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
              <p className="px-1 text-xs font-semibold text-yellow-600">
                {user?.email?.toString()}
              </p>
              <DropdownMenuItem>
                <Button
                  variant="ghost"
                  className="flex h-8 w-full items-center justify-start pl-2"
                  onClick={() => setIsDialogOpen(true)}
                >
                  <LuSettings className="mr-1 h-4 w-4" />
                  Account
                </Button>
              </DropdownMenuItem>
              <DropdownMenuItem>
                <Button variant="ghost" className="h-8 w-full pl-2">
                  <LogoutButton className="flex w-full items-center justify-start">
                    <ExitIcon className="mr-1 h-4 w-4" />
                    Logout
                  </LogoutButton>
                </Button>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogContent className="scrollbar-hide h-screen overflow-y-auto sm:max-w-md">
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
