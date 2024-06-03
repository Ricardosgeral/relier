import { UserAvatar } from "./auth/user-avatar";
import SearchInput from "./search-input";

interface HeaderBoxProps {
  type?: "title" | "greeting";
  title: string;
  subtext: string;
  user?: string;
}

const HeaderBox = ({
  type = "title",
  title,
  subtext,
  user,
}: HeaderBoxProps) => {
  return (
    <div className="flex items-stretch justify-between">
      <div className="flex flex-row items-baseline justify-between gap-x-3 gap-y-1 md:flex-col">
        <h1 className="text-xl font-semibold text-foreground/90 md:text-xl">
          {title}
          {type === "greeting" && (
            <span className="text-20 lg:text-32 font-sans font-semibold text-yellow-500">
              &nbsp;{user}
            </span>
          )}
        </h1>
        <p className="md:text-md text-sm font-semibold text-foreground/70">
          {subtext}
        </p>
      </div>
      <SearchInput />
      <div className="hidden md:block">
        <UserAvatar isPhotoLeft={false} />
      </div>
    </div>
  );
};

export default HeaderBox;
