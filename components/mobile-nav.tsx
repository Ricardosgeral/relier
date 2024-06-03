"use client";

import {
  Sheet,
  SheetClose,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";
import { sidebarLinks } from "@/app/constants";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { HamburgerMenuIcon } from "@radix-ui/react-icons";
import { UserAvatar } from "./auth/user-avatar";
import LogoApp from "./logo-app";
import { ModeToggle } from "./theme-toggle";
import useDarkMode from "@/hooks/use-dark-mode";

const MobileNav = () => {
  const pathname = usePathname();
  const isDarkModeOn = useDarkMode();

  return (
    <Sheet>
      <SheetTrigger>
        <HamburgerMenuIcon width={30} height={30} className="cursor-pointer" />
      </SheetTrigger>
      <SheetContent
        side="left"
        className="flex w-1/4 min-w-[150px] max-w-[250px] flex-col justify-between border-none bg-background pl-0 pr-1"
      >
        <LogoApp square={true} negative={isDarkModeOn} />
        <div className="flex w-full flex-col space-y-2">
          {sidebarLinks.map((item) => {
            const isActive =
              pathname === item.route || pathname.startsWith(`${item.route}/`);

            return (
              <Link href={item.route} key={item.label}>
                <SheetClose asChild key={item.route}>
                  <div
                    className={cn(
                      "flex w-full items-center justify-end space-x-2 rounded-r-full p-2 font-semibold hover:text-yellow-500 xl:justify-end",
                      { "bg-black text-white dark:bg-yellow-500": isActive },
                    )}
                  >
                    <p
                      className={cn("sidebar-label", {
                        "text-white": isActive,
                      })}
                    >
                      {item.label}
                    </p>
                    <div className="relative">
                      {
                        <item.icon
                          className={cn({
                            "invert-0": isActive,
                          })}
                          height={20}
                          width={20}
                        />
                      }
                    </div>
                  </div>
                </SheetClose>
              </Link>
            );
          })}
        </div>
        <div className="flex justify-center">
          <ModeToggle />
        </div>
        <div className="overflow-hidden py-2">
          <UserAvatar isPhotoLeft={true} />
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default MobileNav;
