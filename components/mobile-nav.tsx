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

const MobileNav = () => {
  const pathname = usePathname();

  return (
    <Sheet>
      <SheetTrigger>
        <HamburgerMenuIcon width={30} height={30} className="cursor-pointer" />
      </SheetTrigger>
      <SheetContent
        side="left"
        className="border-none bg-white flex flex-col justify-between pl-0 pr-1 w-1/4 max-w-[250px] min-w-[130px]"
      >
        <LogoApp square={true} />
        <div className="flex flex-col space-y-2 w-full">
          {sidebarLinks.map((item) => {
            const isActive =
              pathname === item.route || pathname.startsWith(`${item.route}/`);

            return (
              <Link href={item.route} key={item.label}>
                <SheetClose asChild key={item.route}>
                  <div
                    className={cn(
                      "flex font-semibold w-full items-center rounded-r-full p-2 justify-end space-x-2 xl:justify-end hover:text-yellow-500",
                      { "bg-black text-white": isActive }
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
        <div className="overflow-hidden py-2">
          <UserAvatar isPhotoLeft={true} />
        </div>
      </SheetContent>
    </Sheet>
  );
};

export default MobileNav;
