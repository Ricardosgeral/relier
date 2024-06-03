import { cn } from "@/lib/utils";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { sidebarLinks } from "@/app/constants";

export default function NavLinks() {
  const pathname = usePathname();
  //console.log(pathname);

  return (
    <div className="flex flex-col justify-center items-center space-y-2 pr-1">
      {sidebarLinks.map((item) => {
        const isActive =
          pathname === item.route || pathname.startsWith(`${item.route}/`);

        return (
          <Link className="w-full" href={item.route} key={item.label}>
            <div
              className={cn(
                "flex font-semibold w-full items-center rounded-r-full p-2 justify-end space-x-2 xl:justify-end hover:text-yellow-500",
                { "bg-black text-white": isActive }
              )}
            >
              <p className={cn("sidebar-label", { "text-white": isActive })}>
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
          </Link>
        );
      })}
    </div>
  );
}
